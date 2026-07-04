import argparse, json, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from transformers import AutoProcessor, AutoModelForVision2Seq

from src.openvla_uav_transfer.openvla_oft.uav_jsonl_dataset import (
    IGNORE_INDEX,
    UAVJsonlDatasetForOpenVLAOFT,
)

ACTION_NAMES = ["vx", "vy", "vz", "yaw_rate"]

def load_stats(path):
    s = json.loads(Path(path).read_text(encoding="utf-8"))
    mean = np.asarray(s["mean"], dtype=np.float32)
    std = np.asarray(s["std"], dtype=np.float32)
    return mean, std, s

def collate(items, pad_token_id, mean, std, max_len=2048):
    input_ids = pad_sequence([x["input_ids"] for x in items], batch_first=True, padding_value=pad_token_id)[:, :max_len]
    labels = pad_sequence([x["labels"] for x in items], batch_first=True, padding_value=IGNORE_INDEX)[:, :max_len]
    actions = np.stack([x["actions"] for x in items], axis=0).astype(np.float32)
    actions_norm = (actions - mean.reshape(1,1,4)) / std.reshape(1,1,4)
    return {
        "pixel_values": torch.stack([x["pixel_values"] for x in items]),
        "input_ids": input_ids,
        "attention_mask": input_ids.ne(pad_token_id),
        "labels": labels,
        "actions": torch.tensor(actions).float(),
        "actions_norm": torch.tensor(actions_norm).float(),
        "proprio": torch.stack([torch.tensor(x["proprio"]) for x in items]).float(),
    }

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

def load_model(model_id, cache_dir, device):
    processor = AutoProcessor.from_pretrained(
        model_id, trust_remote_code=True, cache_dir=cache_dir, local_files_only=True
    )
    kwargs = dict(
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        cache_dir=cache_dir,
        local_files_only=True,
    )
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

def collect_metrics(pred, target):
    err = pred - target
    mae = err.abs().mean(dim=(0,1)).detach().cpu().numpy()
    rmse = err.pow(2).mean(dim=(0,1)).sqrt().detach().cpu().numpy()
    return {
        "overall_mae": float(err.abs().mean().detach().cpu()),
        "overall_rmse": float(err.pow(2).mean().sqrt().detach().cpu()),
        "per_dim_mae": {n: float(mae[i]) for i, n in enumerate(ACTION_NAMES)},
        "per_dim_rmse": {n: float(rmse[i]) for i, n in enumerate(ACTION_NAMES)},
    }

def eval_loop(model, head, loader, device, mean_t, std_t, max_batches):
    head.eval()
    norm_losses, preds, targets = [], [], []
    src = None
    with torch.no_grad():
        for i, batch in enumerate(loader, 1):
            if i > max_batches:
                break
            feat, src = extract_feature(model, batch, device)
            pred_norm = head(feat)
            target_norm = batch["actions_norm"].to(device)
            norm_losses.append(float(F.smooth_l1_loss(pred_norm, target_norm).cpu()))
            pred = pred_norm * std_t + mean_t
            preds.append(pred.cpu())
            targets.append(batch["actions"].cpu())
    head.train()
    metric = collect_metrics(torch.cat(preds), torch.cat(targets))
    metric["normalized_loss"] = sum(norm_losses) / max(1, len(norm_losses))
    metric["batches"] = len(norm_losses)
    metric["feature_source"] = src
    return metric

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-jsonl", default="data/processed/clean_train_timestamp_maps.jsonl")
    ap.add_argument("--val-jsonl", default="data/processed/clean_val_timestamp_maps.jsonl")
    ap.add_argument("--stats", default="data/processed/clean_train_action_stats.json")
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--model-id", default="openvla/openvla-7b")
    ap.add_argument("--cache-dir", default="/root/autodl-tmp/hf-cache")
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--max-train-rows", type=int, default=120)
    ap.add_argument("--max-val-rows", type=int, default=64)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--hidden-dim", type=int, default=256)
    ap.add_argument("--val-max-batches", type=int, default=64)
    ap.add_argument("--out-json", default="logs/pilot/frozen_openvla_uav_action_head_normalized_report.json")
    ap.add_argument("--out-md", default="docs/frozen_openvla_uav_action_head_normalized_report.md")
    ap.add_argument("--ckpt", default="checkpoints/uav_action_head/frozen_openvla_uav_action_head_normalized.pt")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    assert device == "cuda"

    mean, std, stats = load_stats(args.stats)
    mean_t = torch.tensor(mean, device=device).reshape(1,1,4)
    std_t = torch.tensor(std, device=device).reshape(1,1,4)

    processor, model = load_model(args.model_id, args.cache_dir, device)
    pad = processor.tokenizer.pad_token_id or processor.tokenizer.eos_token_id or 0

    train_ds = UAVJsonlDatasetForOpenVLAOFT(args.train_jsonl, processor, image_root=args.image_root, max_rows=args.max_train_rows)
    val_ds = UAVJsonlDatasetForOpenVLAOFT(args.val_jsonl, processor, image_root=args.image_root, max_rows=args.max_val_rows)

    make_collate = lambda items: collate(items, pad, mean, std)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, collate_fn=make_collate)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, collate_fn=make_collate)

    first_batch = next(iter(train_loader))
    feat, feature_source = extract_feature(model, first_batch, device)

    head = UAVActionHead(feat.shape[-1], args.hidden_dim).to(device)
    opt = torch.optim.AdamW(head.parameters(), lr=args.lr)

    initial_val = eval_loop(model, head, val_loader, device, mean_t, std_t, args.val_max_batches)
    history = []

    for epoch in range(1, args.epochs + 1):
        losses = []
        for batch in train_loader:
            feat, feature_source = extract_feature(model, batch, device)
            pred_norm = head(feat)
            target_norm = batch["actions_norm"].to(device)
            loss = F.smooth_l1_loss(pred_norm, target_norm)

            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(float(loss.detach().cpu()))

        val = eval_loop(model, head, val_loader, device, mean_t, std_t, args.val_max_batches)
        item = {
            "epoch": epoch,
            "train_normalized_loss": sum(losses) / max(1, len(losses)),
            "val_normalized_loss": val["normalized_loss"],
            "val_overall_mae": val["overall_mae"],
            "val_overall_rmse": val["overall_rmse"],
            "val_per_dim_mae": val["per_dim_mae"],
            "val_per_dim_rmse": val["per_dim_rmse"],
            "train_steps": len(losses),
            "val_batches": val["batches"],
        }
        history.append(item)
        print(json.dumps(item, ensure_ascii=False))

    Path(args.ckpt).parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "head_state_dict": head.state_dict(),
        "feature_dim": feat.shape[-1],
        "hidden_dim": args.hidden_dim,
        "stats": stats,
        "model_id": args.model_id,
        "feature_source": feature_source,
    }, args.ckpt)

    report = {
        "status": "FROZEN_OPENVLA_NORMALIZED_UAV_ACTION_HEAD_PASS",
        "openvla_frozen": True,
        "trained_component": "uav_action_head_only",
        "lora_oft_started": False,
        "full_training_started": False,
        "closed_loop_eval_started": False,
        "model_id": args.model_id,
        "feature_source": feature_source,
        "train_rows": len(train_ds),
        "val_rows": len(val_ds),
        "stats": args.stats,
        "initial_val": initial_val,
        "history": history,
        "checkpoint": args.ckpt,
        "cuda_max_memory_gb": round(torch.cuda.max_memory_allocated() / 1024**3, 3),
    }

    Path(args.out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_md).write_text("# Frozen OpenVLA Normalized UAV Action Head Report\n\n```json\n" + json.dumps(report, ensure_ascii=False, indent=2) + "\n```\n", encoding="utf-8")
    print(f"WROTE {args.out_json}")
    print(f"WROTE {args.out_md}")
    print(f"WROTE {args.ckpt}")
    print("FROZEN_OPENVLA_NORMALIZED_UAV_ACTION_HEAD_PASS")

if __name__ == "__main__":
    main()
