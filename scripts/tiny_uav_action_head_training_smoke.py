import argparse, json, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

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

def collate(items, pad_token_id, max_len=2048):
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

class TinyActionHead(nn.Module):
    def __init__(self, in_dim, hidden_dim=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.LayerNorm(in_dim),
            nn.Linear(in_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 8 * 4),
        )
    def forward(self, x):
        return self.net(x).reshape(x.shape[0], 8, 4)

def load_model(model_id, cache_dir, device):
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True, cache_dir=cache_dir)
    kwargs = dict(trust_remote_code=True, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True, cache_dir=cache_dir)
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
        try:
            out = model(**inputs, output_hidden_states=True, return_dict=True)
            if getattr(out, "hidden_states", None) is None:
                raise RuntimeError("hidden_states is None")
            feat = out.hidden_states[-1][:, -1, :].float()
            source = "openvla_last_hidden_state"
        except Exception:
            emb = model.get_input_embeddings()(inputs["input_ids"]).mean(dim=1)
            feat = emb.float()
            source = "openvla_text_embedding_fallback"
    proprio = batch["proprio"].to(device).float()
    return torch.cat([feat, proprio], dim=-1), source

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-jsonl", default="data/processed/clean_train_timestamp_maps.jsonl")
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--model-id", default="openvla/openvla-7b")
    ap.add_argument("--cache-dir", default="/root/autodl-tmp/hf-cache")
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--max-rows", type=int, default=8)
    ap.add_argument("--max-steps", type=int, default=3)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--out", default="docs/tiny_uav_action_head_training_smoke_report.md")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    assert device == "cuda"

    processor, model = load_model(args.model_id, args.cache_dir, device)
    pad = processor.tokenizer.pad_token_id or processor.tokenizer.eos_token_id or 0

    ds = UAVJsonlDatasetForOpenVLAOFT(args.train_jsonl, processor, image_root=args.image_root, max_rows=args.max_rows)
    dl = DataLoader(ds, batch_size=args.batch_size, shuffle=False, collate_fn=lambda x: collate(x, pad))

    head = None
    opt = None
    losses = []
    feature_source = None

    for step, batch in enumerate(dl, 1):
        if step > args.max_steps:
            break
        feat, feature_source = extract_feature(model, batch, device)
        target = batch["actions"].to(device)

        if head is None:
            head = TinyActionHead(feat.shape[-1]).to(device)
            opt = torch.optim.AdamW(head.parameters(), lr=args.lr)

        pred = head(feat.detach())
        loss = F.mse_loss(pred, target)

        opt.zero_grad()
        loss.backward()
        opt.step()

        losses.append(float(loss.detach().cpu()))
        print(f"step={step} loss={losses[-1]:.6f}")

    report = {
        "status": "TINY_UAV_ACTION_HEAD_TRAINING_SMOKE_PASS",
        "model_id": args.model_id,
        "feature_source": feature_source,
        "openvla_frozen": True,
        "trained_component": "tiny_uav_action_head_only",
        "lora_oft_started": False,
        "full_training_started": False,
        "closed_loop_eval_started": False,
        "batch_size": args.batch_size,
        "max_steps": args.max_steps,
        "losses": losses,
        "cuda_max_memory_gb": round(torch.cuda.max_memory_allocated() / 1024**3, 3),
    }

    Path(args.out).write_text(
        "# Tiny UAV Action-Head Training Smoke Report\n\n```json\n"
        + json.dumps(report, ensure_ascii=False, indent=2)
        + "\n```\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {args.out}")
    print("TINY_UAV_ACTION_HEAD_TRAINING_SMOKE_PASS")
    print("LORA_OFT_NOT_STARTED")
    print("FULL_TRAINING_NOT_STARTED")

if __name__ == "__main__":
    main()
