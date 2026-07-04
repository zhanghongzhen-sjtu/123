import argparse
import json
import math
from pathlib import Path
from collections import Counter

import numpy as np
import torch
from PIL import Image
from torch.nn.utils.rnn import pad_sequence

IGNORE_INDEX = -100
PAD_TOKEN_ID = 0


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def vec(x, n, name):
    if not isinstance(x, list) or len(x) != n:
        raise ValueError(f"{name} must be length {n}")
    if not all(is_num(v) for v in x):
        raise ValueError(f"{name} contains invalid values")
    return np.asarray(x, dtype=np.float32)


def fake_tokenize(text, max_len=128):
    # Deterministic lightweight tokenizer stub. This is not OpenVLA tokenizer.
    ids = [101]
    for ch in text[: max_len - 2]:
        ids.append(1000 + (ord(ch) % 20000))
    ids.append(102)
    return torch.tensor(ids, dtype=torch.long)


def image_to_tensor(path):
    img = Image.open(path).convert("RGB").resize((224, 224))
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr = np.transpose(arr, (2, 0, 1))
    return torch.from_numpy(arr)


def make_item(row, image_root):
    image = Path(row["image"])
    image = image if image.is_absolute() else Path(image_root) / image
    if not image.exists():
        raise FileNotFoundError(image)

    instruction = row["instruction"]
    if not isinstance(instruction, str) or not instruction.strip():
        raise ValueError("empty instruction")

    state = vec(row["state"], 4, "state")
    action_chunk = row["action_chunk"]
    if not isinstance(action_chunk, list) or len(action_chunk) != 8:
        raise ValueError("action_chunk must be [8,4]")
    actions = np.stack([vec(a, 4, "action_chunk step") for a in action_chunk], axis=0)

    prompt = f"What action should the robot take to {instruction}?"
    input_ids = fake_tokenize(prompt)
    labels = input_ids.clone()
    labels[:-1] = IGNORE_INDEX

    return {
        "pixel_values": image_to_tensor(image),
        "input_ids": input_ids,
        "labels": labels,
        "actions": actions,
        "proprio": state,
        "dataset_name": "TravelUAV",
        "source": row.get("source", {}),
    }


def collate(items, model_max_length=128):
    input_ids = pad_sequence([x["input_ids"] for x in items], batch_first=True, padding_value=PAD_TOKEN_ID)
    labels = pad_sequence([x["labels"] for x in items], batch_first=True, padding_value=IGNORE_INDEX)

    input_ids = input_ids[:, :model_max_length]
    labels = labels[:, :model_max_length]
    attention_mask = input_ids.ne(PAD_TOKEN_ID)

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


def run(jsonl, image_root, batch_size, max_rows):
    rows = []
    maps = Counter()

    with Path(jsonl).open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            if len(rows) >= max_rows:
                break
            row = json.loads(line)
            try:
                item = make_item(row, image_root)
            except Exception as e:
                raise SystemExit(f"COLLATOR_READY_FAIL {jsonl}:{line_no}: {e}")
            rows.append(item)
            maps[item["source"].get("map", "unknown")] += 1

    if not rows:
        raise SystemExit("COLLATOR_READY_FAIL no rows")

    batch = collate(rows[:batch_size])
    shapes = {
        "pixel_values": list(batch["pixel_values"].shape),
        "input_ids": list(batch["input_ids"].shape),
        "attention_mask": list(batch["attention_mask"].shape),
        "labels": list(batch["labels"].shape),
        "actions": list(batch["actions"].shape),
        "proprio": list(batch["proprio"].shape),
    }

    assert shapes["pixel_values"] == [min(batch_size, len(rows)), 3, 224, 224]
    assert shapes["actions"] == [min(batch_size, len(rows)), 8, 4]
    assert shapes["proprio"] == [min(batch_size, len(rows)), 4]

    return {
        "jsonl": jsonl,
        "rows_loaded": len(rows),
        "maps": dict(maps),
        "batch_shapes": shapes,
        "dataset_names": sorted(set(batch["dataset_names"])),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-jsonl", required=True)
    ap.add_argument("--val-jsonl", required=True)
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--max-rows", type=int, default=32)
    ap.add_argument("--out", default="docs/uav_jsonl_dataset_collator_ready_stub_report.md")
    a = ap.parse_args()

    train = run(a.train_jsonl, a.image_root, a.batch_size, a.max_rows)
    val = run(a.val_jsonl, a.image_root, a.batch_size, a.max_rows)

    report = {
        "status": "UAV_JSONL_COLLATOR_READY_STUB_PASS",
        "model_loaded": False,
        "training_started": False,
        "tokenizer": "fake_tokenizer_stub",
        "image_transform": "PIL_resize_224_stub",
        "train": train,
        "val": val,
    }

    lines = [
        "# UAV JSONL Dataset Collator-Ready Stub Report",
        "",
        "## Status",
        "",
        "- UAV_JSONL_COLLATOR_READY_STUB_PASS",
        "- MODEL_NOT_LOADED",
        "- TRAINING_NOT_STARTED",
        "- OPENVLA_TOKENIZER_NOT_USED",
        "- OPENVLA_IMAGE_TRANSFORM_NOT_USED",
        "",
        "## Result",
        "",
        "```json",
        json.dumps(report, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Interpretation",
        "",
        "This confirms that TravelUAV JSONL can be mapped into OpenVLA-OFT collator-ready field names and tensor shapes using lightweight stubs.",
        "",
        "This does not confirm compatibility with the real OpenVLA tokenizer, image transform, or model forward pass.",
    ]

    Path(a.out).write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {a.out}")
    print("UAV_JSONL_COLLATOR_READY_STUB_PASS")
    print("MODEL_NOT_LOADED")
    print("TRAINING_NOT_STARTED")


if __name__ == "__main__":
    main()
