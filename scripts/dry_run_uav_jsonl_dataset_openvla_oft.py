import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
from pathlib import Path

import numpy as np
import torch
from torch.nn.utils.rnn import pad_sequence
from transformers import AutoProcessor

from src.openvla_uav_transfer.openvla_oft.uav_jsonl_dataset import (
    IGNORE_INDEX,
    UAVJsonlDatasetForOpenVLAOFT,
)


def collate_like_openvla(items, pad_token_id, model_max_length):
    input_ids = pad_sequence([x["input_ids"] for x in items], batch_first=True, padding_value=pad_token_id)
    labels = pad_sequence([x["labels"] for x in items], batch_first=True, padding_value=IGNORE_INDEX)

    input_ids = input_ids[:, :model_max_length]
    labels = labels[:, :model_max_length]
    attention_mask = input_ids.ne(pad_token_id)

    pixel_values = torch.stack([x["pixel_values"] for x in items])
    actions = torch.stack([torch.from_numpy(np.copy(x["actions"])) for x in items])
    proprio = torch.tensor(np.stack([x["proprio"] for x in items]), dtype=torch.float32)
    dataset_names = [x["dataset_name"] for x in items]

    return {
        "pixel_values": pixel_values,
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels,
        "actions": actions,
        "proprio": proprio,
        "dataset_names": dataset_names,
    }


def run_split(name, jsonl, processor, image_root, batch_size, max_rows):
    ds = UAVJsonlDatasetForOpenVLAOFT(
        jsonl,
        processor=processor,
        image_root=image_root,
        max_rows=max_rows,
    )

    items = [ds[i] for i in range(min(batch_size, len(ds)))]

    pad_token_id = processor.tokenizer.pad_token_id
    if pad_token_id is None:
        pad_token_id = processor.tokenizer.eos_token_id
    if pad_token_id is None:
        pad_token_id = 0

    model_max_length = getattr(processor.tokenizer, "model_max_length", 2048)
    if model_max_length is None or model_max_length > 100000:
        model_max_length = 2048

    batch = collate_like_openvla(items, pad_token_id, model_max_length)

    shapes = {k: list(v.shape) for k, v in batch.items() if torch.is_tensor(v)}
    assert shapes["actions"] == [len(items), 8, 4]
    assert shapes["proprio"] == [len(items), 4]
    assert shapes["pixel_values"][0] == len(items)

    return {
        "split": name,
        "jsonl": str(jsonl),
        "dataset_len": len(ds),
        "batch_size": len(items),
        "batch_shapes": shapes,
        "dataset_names": sorted(set(batch["dataset_names"])),
        "first_metadata": items[0]["metadata"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-jsonl", required=True)
    ap.add_argument("--val-jsonl", required=True)
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--model-id", default="openvla/openvla-7b")
    ap.add_argument("--cache-dir", default="/root/autodl-tmp/hf-cache")
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--max-rows", type=int, default=16)
    ap.add_argument("--out", default="docs/uav_jsonl_dataset_openvla_oft_dry_run_report.md")
    args = ap.parse_args()

    processor = AutoProcessor.from_pretrained(
        args.model_id,
        trust_remote_code=True,
        cache_dir=args.cache_dir,
    )

    train = run_split("train", args.train_jsonl, processor, args.image_root, args.batch_size, args.max_rows)
    val = run_split("val", args.val_jsonl, processor, args.image_root, args.batch_size, args.max_rows)

    report = {
        "status": "UAV_JSONL_DATASET_OPENVLA_OFT_DRY_RUN_PASS",
        "model_id": args.model_id,
        "processor_class": processor.__class__.__name__,
        "model_weights_loaded": False,
        "training_started": False,
        "train": train,
        "val": val,
    }

    lines = [
        "# UAVJsonlDataset For OpenVLA-OFT Dry Run Report",
        "",
        "## Status",
        "",
        "- UAV_JSONL_DATASET_OPENVLA_OFT_DRY_RUN_PASS",
        "- MODEL_WEIGHTS_NOT_LOADED",
        "- TRAINING_NOT_STARTED",
        "",
        "## Result",
        "",
        "```json",
        json.dumps(report, ensure_ascii=False, indent=2),
        "```",
    ]
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {args.out}")
    print("UAV_JSONL_DATASET_OPENVLA_OFT_DRY_RUN_PASS")
    print("MODEL_WEIGHTS_NOT_LOADED")
    print("TRAINING_NOT_STARTED")


if __name__ == "__main__":
    main()
