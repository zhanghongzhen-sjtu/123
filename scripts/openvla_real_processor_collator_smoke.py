import argparse
import json
import math
from pathlib import Path
from collections import Counter

import numpy as np
import torch
from PIL import Image
from torch.nn.utils.rnn import pad_sequence
from transformers import AutoProcessor

IGNORE_INDEX = -100


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def vec(x, n, name):
    if not isinstance(x, list) or len(x) != n:
        raise ValueError(f"{name} must be length {n}")
    if not all(is_num(v) for v in x):
        raise ValueError(f"{name} has invalid value")
    return np.asarray(x, dtype=np.float32)


def make_prompt(instruction):
    return f"What action should the robot take to {instruction}?"


def load_rows(jsonl, max_rows):
    rows = []
    with Path(jsonl).open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
                if len(rows) >= max_rows:
                    break
    return rows


def image_path(row, image_root):
    p = Path(row["image"])
    return p if p.is_absolute() else Path(image_root) / p


def make_item(row, image_root, processor):
    img_path = image_path(row, image_root)
    if not img_path.exists():
        raise FileNotFoundError(img_path)

    image = Image.open(img_path).convert("RGB")
    prompt = make_prompt(row["instruction"])

    tok = processor.tokenizer(prompt, add_special_tokens=True, return_tensors=None)
    input_ids = torch.tensor(tok["input_ids"], dtype=torch.long)
    labels = input_ids.clone()

    # Stub masking policy: keep only final token supervised.
    # This validates tensor plumbing, not final OpenVLA label policy.
    labels[:-1] = IGNORE_INDEX

    pix = processor.image_processor(images=image, return_tensors="pt")
    pixel_values = pix["pixel_values"][0]

    state = vec(row["state"], 4, "state")
    chunk = row["action_chunk"]
    if not isinstance(chunk, list) or len(chunk) != 8:
        raise ValueError("action_chunk must be [8,4]")
    actions = np.stack([vec(a, 4, "action_chunk step") for a in chunk], axis=0)

    return {
        "pixel_values": pixel_values,
        "input_ids": input_ids,
        "labels": labels,
        "actions": actions,
        "proprio": state,
        "dataset_name": "TravelUAV",
        "source": row.get("source", {}),
    }


def collate(items, pad_token_id, model_max_length):
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


def run_split(name, jsonl, image_root, processor, batch_size, max_rows):
    rows = load_rows(jsonl, max_rows)
    items = []
    maps = Counter()

    for i, row in enumerate(rows, 1):
        try:
            item = make_item(row, image_root, processor)
        except Exception as exc:
            raise SystemExit(f"REAL_PROCESSOR_COLLATOR_FAIL {jsonl}:{i}: {exc}")
        items.append(item)
        maps[item["source"].get("map", "unknown")] += 1

    if not items:
        raise SystemExit(f"REAL_PROCESSOR_COLLATOR_FAIL {name}: no items")

    pad_token_id = processor.tokenizer.pad_token_id
    if pad_token_id is None:
        pad_token_id = processor.tokenizer.eos_token_id
    if pad_token_id is None:
        pad_token_id = 0

    model_max_length = getattr(processor.tokenizer, "model_max_length", 2048)
    if model_max_length is None or model_max_length > 100000:
        model_max_length = 2048

    batch = collate(items[:batch_size], pad_token_id, model_max_length)

    shapes = {
        "pixel_values": list(batch["pixel_values"].shape),
        "input_ids": list(batch["input_ids"].shape),
        "attention_mask": list(batch["attention_mask"].shape),
        "labels": list(batch["labels"].shape),
        "actions": list(batch["actions"].shape),
        "proprio": list(batch["proprio"].shape),
    }

    b = min(batch_size, len(items))
    assert shapes["actions"] == [b, 8, 4]
    assert shapes["proprio"] == [b, 4]
    assert shapes["input_ids"][0] == b
    assert shapes["labels"][0] == b
    assert shapes["pixel_values"][0] == b

    return {
        "split": name,
        "jsonl": jsonl,
        "rows_loaded": len(items),
        "maps": dict(maps),
        "batch_shapes": shapes,
        "dataset_names": sorted(set(batch["dataset_names"])),
        "pad_token_id": int(pad_token_id),
        "model_max_length_used": int(model_max_length),
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
    ap.add_argument("--out", default="docs/openvla_real_processor_collator_smoke_report.md")
    args = ap.parse_args()

    processor = AutoProcessor.from_pretrained(
        args.model_id,
        trust_remote_code=True,
        cache_dir=args.cache_dir,
    )

    train = run_split("train", args.train_jsonl, args.image_root, processor, args.batch_size, args.max_rows)
    val = run_split("val", args.val_jsonl, args.image_root, processor, args.batch_size, args.max_rows)

    report = {
        "status": "OPENVLA_REAL_PROCESSOR_COLLATOR_SMOKE_PASS",
        "model_id": args.model_id,
        "processor_class": processor.__class__.__name__,
        "model_weights_loaded": False,
        "training_started": False,
        "train": train,
        "val": val,
    }

    lines = [
        "# OpenVLA Real Processor Collator Smoke Report",
        "",
        "## Status",
        "",
        "- OPENVLA_REAL_PROCESSOR_COLLATOR_SMOKE_PASS",
        "- MODEL_WEIGHTS_NOT_LOADED",
        "- TRAINING_NOT_STARTED",
        "",
        "## Result",
        "",
        "```json",
        json.dumps(report, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Interpretation",
        "",
        "This smoke test uses the real OpenVLA processor/tokenizer/image processor to create collator-ready tensors from TravelUAV JSONL.",
        "",
        "It does not load OpenVLA/openvla-7b model weights and does not start training.",
    ]

    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {args.out}")
    print("OPENVLA_REAL_PROCESSOR_COLLATOR_SMOKE_PASS")
    print("MODEL_WEIGHTS_NOT_LOADED")
    print("TRAINING_NOT_STARTED")


if __name__ == "__main__":
    main()
