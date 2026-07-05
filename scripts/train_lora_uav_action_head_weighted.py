import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import torch
import torch.nn as nn
import torch.nn.functional as F
from peft import LoraConfig, get_peft_model
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

def load_model_with_lora(model_id, cache_dir, device, lora_rank, lora_dropout):
    processor = AutoProcessor.from_pretrained(
        model_id,
        trust_remote_code=True,
        cache_dir=cache_dir,
        local_files_only=True,
    )

    kwargs = dict(
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        cache_dir=cache_dir,
        local_files_only=True,
    )

    try:
        model = AutoModelForVision2Seq.from_pretrained(
            model_id,
            attn_implementation="eager",
            **kwargs,
        )
    except TypeError:
        model = AutoModelForVision2Seq.from_pretrained(model_id, **kwargs)

    model.to(device)

    # Freeze base first.
    for p in model.parameters():
        p.requires_grad_(False)

    lora_config = LoraConfig(
        r=lora_rank,
        lora_alpha=min(lora_rank, 16),
        lora_dropout=lora_dropout,
        target_modules="all-linear",
        init_lora_weights="gaussian",
    )

    model = get_peft_model(model, lora_config)
    model.train()

    return processor, model

def extract_feature_with_grad(model, batch, device):
    inputs = {
        "input_ids": batch["input_ids"].to(device),
        "attention_mask": batch["attention_mask"].to(device),
        "pixel_values": batch["pixel_values"].to(device=device, dtype=torch.bfloat16),
    }

    out = model(**inputs, output_hidden_states=True, return_dict=True)

    if getattr(out, "hidden_states", None) is None:
        feat = model.get_input_embeddings()(inputs["input_ids"]).mean(dim=1).float()
        source = "text_embedding_fallback"
    else:
        feat = out.hidden_states[-1][:, -1, :].float()
        source = "openvla_last_hidden_state"

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
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--head-lr", type=float, default=1e-4)
    ap.add_argument("--hidden-dim", type=int, default=256)
    ap.add_argument("--lora-rank", type=int, default=8)
    ap.add_argument("--lora-dropout", type=float, default=0.0)
    ap.add_argument("--action-stats", default=None, help="Optional action stats JSON with mean/std/suggested_loss_weights.")
    ap.add_argument("--loss-weights", default=None, help="Optional comma-separated per-dim loss weights, e.g. 1,1,1,1.")
    ap.add_argument("--out-json", default="logs/lora_smoke/tiny_lora_uav_action_head_smoke_report.json")
    ap.add_argument("--out-md", default="docs/tiny_lora_uav_action_head_smoke_report.md")
    ap.add_argument("--ckpt-dir", default="checkpoints/lora_smoke/tiny_lora_uav")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    assert device == "cuda"

    processor, model = load_model_with_lora(
        args.model_id,
        args.cache_dir,
        device,
        args.lora_rank,
        args.lora_dropout,
    )

    try:
        model.print_trainable_parameters()
    except Exception:
        pass

    pad = processor.tokenizer.pad_token_id or processor.tokenizer.eos_token_id or 0

    ds = UAVJsonlDatasetForOpenVLAOFT(
        args.train_jsonl,
        processor=processor,
        image_root=args.image_root,
        max_rows=args.max_rows,
    )
    dl = DataLoader(ds, batch_size=args.batch_size, shuffle=False, collate_fn=lambda x: collate(x, pad))

    first_batch = next(iter(dl))
    feat, feature_source = extract_feature_with_grad(model, first_batch, device)

    head = UAVActionHead(feat.shape[-1], hidden_dim=args.hidden_dim).to(device)
    head.train()

    params = [
        {"params": [p for p in model.parameters() if p.requires_grad], "lr": args.lr},
        {"params": head.parameters(), "lr": args.head_lr},
    ]
    opt = torch.optim.AdamW(params)

    losses = []

    for step, batch in enumerate(dl, 1):
        if step > args.max_steps:
            break

        feat, feature_source = extract_feature_with_grad(model, batch, device)
        target = batch["actions"].to(device)

        pred = head(feat)
        loss = F.smooth_l1_loss(pred, target)

        opt.zero_grad()
        loss.backward()
        opt.step()

        losses.append(float(loss.detach().cpu()))
        print(f"step={step} loss={losses[-1]:.6f}")

    ckpt_dir = Path(args.ckpt_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    # Save adapter only, not merged full model.
    model.save_pretrained(ckpt_dir / "lora_adapter")
    torch.save(
        {
            "head_state_dict": head.state_dict(),
            "feature_dim": feat.shape[-1],
            "hidden_dim": args.hidden_dim,
            "action_chunk_size": 8,
            "action_dim": 4,
            "feature_source": feature_source,
        },
        ckpt_dir / "uav_action_head.pt",
    )

    report = {
        "status": "TINY_LORA_UAV_ACTION_HEAD_SMOKE_PASS",
        "model_id": args.model_id,
        "feature_source": feature_source,
        "train_rows": len(ds),
        "batch_size": args.batch_size,
        "max_steps": args.max_steps,
        "losses": losses,
        "lora_rank": args.lora_rank,
        "lora_dropout": args.lora_dropout,
        "action_stats": args.action_stats,
        "loss_weights": None if loss_weights is None else loss_weights.detach().cpu().view(-1).tolist(),
        "loss_is_action_normalized": action_mean is not None,
        "saved_lora_adapter": str(ckpt_dir / "lora_adapter"),
        "saved_action_head": str(ckpt_dir / "uav_action_head.pt"),
        "full_training_started": False,
        "closed_loop_eval_started": False,
        "merged_full_model_saved": False,
        "cuda_max_memory_gb": round(torch.cuda.max_memory_allocated() / 1024**3, 3),
    }

    Path(args.out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_md).write_text(
        "# Tiny LoRA UAV Action-Head Smoke Report\n\n```json\n"
        + json.dumps(report, ensure_ascii=False, indent=2)
        + "\n```\n",
        encoding="utf-8",
    )

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {args.out_json}")
    print(f"WROTE {args.out_md}")
    print("TINY_LORA_UAV_ACTION_HEAD_SMOKE_PASS")

if __name__ == "__main__":
    main()
