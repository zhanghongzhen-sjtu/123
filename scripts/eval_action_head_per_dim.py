import argparse
import json
import math
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch.nn.utils.rnn import pad_sequence
from transformers import AutoProcessor, AutoModelForVision2Seq

from src.openvla_uav_transfer.openvla_oft.uav_jsonl_dataset import (
    IGNORE_INDEX,
    UAVJsonlDatasetForOpenVLAOFT,
)

ACTION_NAMES = ["vx", "vy", "vz", "yaw_rate"]


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def vec(x, n, name):
    if not isinstance(x, list) or len(x) != n:
        raise ValueError(f"{name} must be length {n}")
    if not all(is_num(v) for v in x):
        raise ValueError(f"{name} invalid numeric values")
    return torch.tensor(x, dtype=torch.float32)


class StateActionChunkDataset(Dataset):
    def __init__(self, jsonl, max_rows=None):
        self.rows = []
        with Path(jsonl).open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                state = vec(r["state"], 4, "state")
                actions = torch.stack([vec(a, 4, "action_chunk step") for a in r["action_chunk"]])
                self.rows.append({"state": state, "actions": actions, "source": r.get("source", {})})
                if max_rows is not None and len(self.rows) >= max_rows:
                    break

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        return self.rows[idx]


class StateOnlyActionHead(nn.Module):
    def __init__(self, hidden_dim=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.LayerNorm(4),
            nn.Linear(4, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 32),
        )

    def forward(self, state):
        return self.net(state).reshape(state.shape[0], 8, 4)


class UAVActionHead(nn.Module):
    def __init__(self, in_dim, hidden_dim=256, dropout=0.05):
        super().__init__()
        self.net = nn.Sequential(
            nn.LayerNorm(in_dim),
            nn.Linear(in_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 32),
        )

    def forward(self, x):
        return self.net(x).reshape(x.shape[0], 8, 4)


def metrics(pred, target):
    err = pred - target
    abs_err = err.abs()
    sq_err = err.pow(2)

    per_dim_mae = abs_err.mean(dim=(0, 1)).detach().cpu().numpy()
    per_dim_rmse = sq_err.mean(dim=(0, 1)).sqrt().detach().cpu().numpy()
    overall_mae = abs_err.mean().item()
    overall_rmse = sq_err.mean().sqrt().item()

    return {
        "overall_mae": overall_mae,
        "overall_rmse": overall_rmse,
        "per_dim_mae": {name: float(per_dim_mae[i]) for i, name in enumerate(ACTION_NAMES)},
        "per_dim_rmse": {name: float(per_dim_rmse[i]) for i, name in enumerate(ACTION_NAMES)},
    }


def eval_state_only(jsonl, ckpt, max_rows, batch_size, device):
    ds = StateActionChunkDataset(jsonl, max_rows=max_rows)
    dl = DataLoader(ds, batch_size=batch_size, shuffle=False)

    state = torch.load(ckpt, map_location=device)
    hidden_dim = state.get("hidden_dim", 256)
    model = StateOnlyActionHead(hidden_dim=hidden_dim).to(device)
    model.load_state_dict(state["model_state_dict"])
    model.eval()

    preds, targets = [], []
    with torch.no_grad():
        for batch in dl:
            s = batch["state"].to(device)
            t = batch["actions"].to(device)
            p = model(s)
            preds.append(p.cpu())
            targets.append(t.cpu())

    pred = torch.cat(preds, dim=0)
    target = torch.cat(targets, dim=0)
    out = metrics(pred, target)
    out["rows"] = len(ds)
    return out


def collate_openvla(items, pad_token_id, max_len=2048):
    input_ids = pad_sequence([x["input_ids"] for x in items], batch_first=True, padding_value=pad_token_id)[:, :max_len]
    labels = pad_sequence([x["labels"] for x in items], batch_first=True, padding_value=IGNORE_INDEX)[:, :max_len]
    return {
        "pixel_values": torch.stack([x["pixel_values"] for x in items]),
        "input_ids": input_ids,
        "attention_mask": input_ids.ne(pad_token_id),
        "labels": labels,
        "actions": torch.stack([torch.tensor(x["actions"]) for x in items]).float(),
        "proprio": torch.stack([torch.tensor(x["proprio"]) for x in items]).float(),
    }


def load_openvla(model_id, cache_dir, device):
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True, cache_dir=cache_dir, local_files_only=True)
    kwargs = dict(trust_remote_code=True, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True, cache_dir=cache_dir, local_files_only=True)
    try:
        model = AutoModelForVision2Seq.from_pretrained(model_id, attn_implementation="eager", **kwargs)
    except TypeError:
        model = AutoModelForVision2Seq.from_pretrained(model_id, **kwargs)
    model.to(device).eval()
    for p in model.parameters():
        p.requires_grad_(False)
    return processor, model


def extract_feature(model, batch, device):
    inputs = {
        "input_ids": batch["input_ids"].to(device),
        "attention_mask": batch["attention_mask"].to(device),
        "pixel_values": batch["pixel_values"].to(device=device, dtype=torch.bfloat16),
    }
    with torch.no_grad():
        out = model(**inputs, output_hidden_states=True, return_dict=True)
        if getattr(out, "hidden_states", None) is None:
            feat = model.get_input_embeddings()(inputs["input_ids"]).mean(dim=1).float()
            source = "text_embedding_fallback"
        else:
            feat = out.hidden_states[-1][:, -1, :].float()
            source = "openvla_last_hidden_state"
    proprio = batch["proprio"].to(device).float()
    return torch.cat([feat, proprio], dim=-1), source


def eval_frozen_openvla(jsonl, ckpt, model_id, cache_dir, image_root, max_rows, batch_size, device):
    processor, model = load_openvla(model_id, cache_dir, device)
    pad = processor.tokenizer.pad_token_id or processor.tokenizer.eos_token_id or 0

    ds = UAVJsonlDatasetForOpenVLAOFT(jsonl, processor, image_root=image_root, max_rows=max_rows)
    dl = DataLoader(ds, batch_size=batch_size, shuffle=False, collate_fn=lambda x: collate_openvla(x, pad))

    ck = torch.load(ckpt, map_location=device)
    head = UAVActionHead(ck["feature_dim"], hidden_dim=ck["hidden_dim"]).to(device)
    head.load_state_dict(ck["head_state_dict"])
    head.eval()

    preds, targets = [], []
    feature_source = None
    with torch.no_grad():
        for batch in dl:
            feat, feature_source = extract_feature(model, batch, device)
            pred = head(feat)
            preds.append(pred.cpu())
            targets.append(batch["actions"].cpu())

    pred = torch.cat(preds, dim=0)
    target = torch.cat(targets, dim=0)
    out = metrics(pred, target)
    out["rows"] = len(ds)
    out["feature_source"] = feature_source
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--val-jsonl", default="data/processed/clean_val_timestamp_maps.jsonl")
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--max-rows", type=int, default=64)
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--model-id", default="openvla/openvla-7b")
    ap.add_argument("--cache-dir", default="/root/autodl-tmp/hf-cache")
    ap.add_argument("--state-ckpt", default="checkpoints/uav_action_head/state_only_action_head_baseline.pt")
    ap.add_argument("--openvla-ckpt", default="checkpoints/uav_action_head/frozen_openvla_uav_action_head_pilot.pt")
    ap.add_argument("--out-json", default="logs/pilot/action_head_per_dim_eval.json")
    ap.add_argument("--out-md", default="docs/action_head_per_dim_eval.md")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"

    state_metrics = eval_state_only(args.val_jsonl, args.state_ckpt, args.max_rows, args.batch_size, device)
    openvla_metrics = eval_frozen_openvla(
        args.val_jsonl,
        args.openvla_ckpt,
        args.model_id,
        args.cache_dir,
        args.image_root,
        args.max_rows,
        args.batch_size,
        device,
    )

    report = {
        "status": "ACTION_HEAD_PER_DIM_EVAL_PASS",
        "val_jsonl": args.val_jsonl,
        "max_rows": args.max_rows,
        "state_only": state_metrics,
        "frozen_openvla_plus_state": openvla_metrics,
        "lora_oft_started": False,
        "full_training_started": False,
        "closed_loop_eval_started": False,
    }

    Path(args.out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Action Head Per-Dimension Evaluation",
        "",
        "## Status",
        "",
        "- ACTION_HEAD_PER_DIM_EVAL_PASS",
        "- LORA_OFT_NOT_STARTED",
        "- FULL_TRAINING_NOT_STARTED",
        "- CLOSED_LOOP_EVAL_NOT_STARTED",
        "",
        "## Result",
        "",
        "```json",
        json.dumps(report, ensure_ascii=False, indent=2),
        "```",
    ]
    Path(args.out_md).write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {args.out_json}")
    print(f"WROTE {args.out_md}")
    print("ACTION_HEAD_PER_DIM_EVAL_PASS")


if __name__ == "__main__":
    main()
