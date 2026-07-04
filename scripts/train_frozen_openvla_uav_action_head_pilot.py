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
        out = model(**inputs, output_hidden_states=True, return_dict=True)
        if getattr(out, "hidden_states", None) is None:
            emb = model.get_input_embeddings()(inputs["input_ids"]).mean(dim=1)
            feat = emb.float()
            source = "text_embedding_fallback"
        else:
            feat = out.hidden_states[-1][:, -1, :].float()
            source = "openvla_last_hidden_state"
    proprio = batch["proprio"].to(device).float()
    return torch.cat([feat, proprio], dim=-1), source

def eval_loop(model, head, loader, device, max_batches):
    head.eval()
    losses = []
    src = None
    with torch.no_grad():
        for i, batch in enumerate(loader, 1):
            if i > max_batches:
                break
            feat, src = extract_feature(model, batch, device)
            pred = head(feat)
            target = batch["actions"].to(device)
            loss = F.mse_loss(pred, target)
            losses.append(float(loss.cpu()))
    head.train()
    return sum(losses) / max(1, len(losses)), src, len(losses)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-jsonl", default="data/processed/clean_train_timestamp_maps.jsonl")
    ap.add_argument("--val-jsonl", default="data/processed/clean_val_timestamp_maps.jsonl")
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--model-id", default="openvla/openvla-7b")
    ap.add_argument("--cache-dir", default="/root/autodl-tmp/hf-cache")
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--max-train-rows", type=int, default=120)
    ap.add_argument("--max-val-rows", type=int, default=64)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--hidden-dim", type=int, default=256)
    ap.add_argument("--val-max-batches", type=int, default=32)
    ap.add_argument("--out-json", default="logs/pilot/frozen_openvla_uav_action_head_pilot_report.json")
    ap.add_argument("--out-md", default="docs/frozen_openvla_uav_action_head_pilot_report.md")
    ap.add_argument("--ckpt", default="checkpoints/uav_action_head/frozen_openvla_uav_action_head_pilot.pt")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    assert device == "cuda"

    processor, model = load_model(args.model_id, args.cache_dir, device)
    pad = processor.tokenizer.pad_token_id or processor.tokenizer.eos_token_id or 0

    train_ds = UAVJsonlDatasetForOpenVLAOFT(args.train_jsonl, processor, image_root=args.image_root, max_rows=args.max_train_rows)
    val_ds = UAVJsonlDatasetForOpenVLAOFT(args.val_jsonl, processor, image_root=args.image_root, max_rows=args.max_val_rows)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, collate_fn=lambda x: collate(x, pad))
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, collate_fn=lambda x: collate(x, pad))

    first_batch = next(iter(train_loader))
    feat, feature_source = extract_feature(model, first_batch, device)

    head = UAVActionHead(feat.shape[-1], hidden_dim=args.hidden_dim).to(device)
    opt = torch.optim.AdamW(head.parameters(), lr=args.lr)

    history = []
    initial_val, _, initial_val_batches = eval_loop(model, head, val_loader, device, args.val_max_batches)

    for epoch in range(1, args.epochs + 1):
        losses = []
        for batch in train_loader:
            feat, feature_source = extract_feature(model, batch, device)
            target = batch["actions"].to(device)
            pred = head(feat)
            loss = F.smooth_l1_loss(pred, target)

            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(float(loss.detach().cpu()))

        train_loss = sum(losses) / max(1, len(losses))
        val_loss, _, val_batches = eval_loop(model, head, val_loader, device, args.val_max_batches)
        history.append({"epoch": epoch, "train_loss": train_loss, "val_loss": val_loss, "train_steps": len(losses), "val_batches": val_batches})
        print(f"epoch={epoch} train_loss={train_loss:.6f} val_loss={val_loss:.6f}")

    Path(args.ckpt).parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "head_state_dict": head.state_dict(),
        "feature_dim": feat.shape[-1],
        "hidden_dim": args.hidden_dim,
        "action_chunk_size": 8,
        "action_dim": 4,
        "model_id": args.model_id,
        "feature_source": feature_source,
    }, args.ckpt)

    report = {
        "status": "FROZEN_OPENVLA_UAV_ACTION_HEAD_PILOT_PASS",
        "openvla_frozen": True,
        "trained_component": "uav_action_head_only",
        "lora_oft_started": False,
        "full_training_started": False,
        "closed_loop_eval_started": False,
        "model_id": args.model_id,
        "feature_source": feature_source,
        "train_rows": len(train_ds),
        "val_rows": len(val_ds),
        "batch_size": args.batch_size,
        "epochs": args.epochs,
        "lr": args.lr,
        "initial_val_loss": initial_val,
        "history": history,
        "checkpoint": args.ckpt,
        "cuda_max_memory_gb": round(torch.cuda.max_memory_allocated() / 1024**3, 3),
    }

    Path(args.out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_md).write_text(
        "# Frozen OpenVLA UAV Action-Head Pilot Report\n\n```json\n"
        + json.dumps(report, ensure_ascii=False, indent=2)
        + "\n```\n",
        encoding="utf-8",
    )

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {args.out_json}")
    print(f"WROTE {args.out_md}")
    print(f"WROTE {args.ckpt}")
    print("FROZEN_OPENVLA_UAV_ACTION_HEAD_PILOT_PASS")
    print("LORA_OFT_NOT_STARTED")
    print("FULL_TRAINING_NOT_STARTED")

if __name__ == "__main__":
    main()
