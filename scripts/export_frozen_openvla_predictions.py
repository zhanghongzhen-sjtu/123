import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from transformers import AutoProcessor, AutoModelForVision2Seq

from src.openvla_uav_transfer.openvla_oft.uav_jsonl_dataset import (
    IGNORE_INDEX,
    UAVJsonlDatasetForOpenVLAOFT,
)

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
        "metadata": [x["metadata"] for x in items],
    }

def load_model(model_id, cache_dir, device):
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", default="data/processed/clean_val_timestamp_maps.jsonl")
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--model-id", default="openvla/openvla-7b")
    ap.add_argument("--cache-dir", default="/root/autodl-tmp/hf-cache")
    ap.add_argument("--ckpt", default="checkpoints/uav_action_head/frozen_openvla_uav_action_head_pilot.pt")
    ap.add_argument("--max-rows", type=int, default=64)
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--out", default="data/debug/predictions/frozen_openvla_val_predictions.jsonl")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    assert device == "cuda"

    processor, model = load_model(args.model_id, args.cache_dir, device)
    pad = processor.tokenizer.pad_token_id or processor.tokenizer.eos_token_id or 0

    ds = UAVJsonlDatasetForOpenVLAOFT(args.jsonl, processor, image_root=args.image_root, max_rows=args.max_rows)
    dl = DataLoader(ds, batch_size=args.batch_size, shuffle=False, collate_fn=lambda x: collate(x, pad))

    ck = torch.load(args.ckpt, map_location=device)
    head = UAVActionHead(ck["feature_dim"], hidden_dim=ck["hidden_dim"]).to(device)
    head.load_state_dict(ck["head_state_dict"])
    head.eval()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    feature_source = None
    with out.open("w", encoding="utf-8") as w, torch.no_grad():
        for batch in dl:
            feat, feature_source = extract_feature(model, batch, device)
            pred = head(feat).cpu().numpy()
            target = batch["actions"].cpu().numpy()

            for i, meta in enumerate(batch["metadata"]):
                rec = {
                    "dataset": "TravelUAV",
                    "episode_id": meta.get("episode_id"),
                    "step_id": meta.get("step_id"),
                    "source": meta.get("source", {}),
                    "target_action_chunk": target[i].tolist(),
                    "pred_action_chunk": pred[i].tolist(),
                    "abs_error": np.abs(pred[i] - target[i]).tolist(),
                    "feature_source": feature_source,
                }
                w.write(json.dumps(rec, ensure_ascii=False) + "\n")
                count += 1

    print(f"WROTE {out}")
    print(f"ROWS {count}")
    print(f"feature_source={feature_source}")
    print("FROZEN_OPENVLA_PREDICTION_EXPORT_PASS")

if __name__ == "__main__":
    main()
