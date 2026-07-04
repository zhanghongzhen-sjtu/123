import argparse
import json
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from transformers import AutoProcessor


def load_first_row(jsonl):
    with Path(jsonl).open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                return json.loads(line)
    raise RuntimeError("empty jsonl")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", default="data/processed/clean_train_timestamp_maps.jsonl")
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--model-id", default="openvla/openvla-7b")
    ap.add_argument("--cache-dir", default="/root/autodl-tmp/hf-cache")
    ap.add_argument("--out", default="docs/openvla_processor_smoke_report.md")
    args = ap.parse_args()

    row = load_first_row(args.jsonl)

    image_path = Path(row["image"])
    if not image_path.is_absolute():
        image_path = Path(args.image_root) / image_path
    if not image_path.exists():
        raise FileNotFoundError(image_path)

    instruction = row["instruction"]
    prompt = f"What action should the robot take to {instruction}?"

    state = np.asarray(row["state"], dtype=np.float32)
    actions = np.asarray(row["action_chunk"], dtype=np.float32)

    assert state.shape == (4,)
    assert actions.shape == (8, 4)

    image = Image.open(image_path).convert("RGB")

    processor = AutoProcessor.from_pretrained(
        args.model_id,
        trust_remote_code=True,
        cache_dir=args.cache_dir,
    )

    tokenizer_ok = hasattr(processor, "tokenizer")
    image_processor_ok = hasattr(processor, "image_processor")

    token_shapes = {}
    pixel_shapes = {}

    if tokenizer_ok:
        tok = processor.tokenizer(prompt, return_tensors="pt")
        token_shapes = {k: list(v.shape) for k, v in tok.items() if hasattr(v, "shape")}

    if image_processor_ok:
        pix = processor.image_processor(images=image, return_tensors="pt")
        pixel_shapes = {k: list(v.shape) for k, v in pix.items() if hasattr(v, "shape")}

    # Some processors expose a combined call instead.
    combined_shapes = {}
    try:
        combined = processor(text=prompt, images=image, return_tensors="pt")
        combined_shapes = {k: list(v.shape) for k, v in combined.items() if hasattr(v, "shape")}
    except Exception as exc:
        combined_shapes = {"combined_call_error": str(exc)[:300]}

    report = {
        "status": "OPENVLA_PROCESSOR_SMOKE_PASS",
        "model_id": args.model_id,
        "model_weights_loaded": False,
        "training_started": False,
        "jsonl": args.jsonl,
        "image_path": str(image_path),
        "instruction_chars": len(instruction),
        "state_shape": list(state.shape),
        "actions_shape": list(actions.shape),
        "processor_class": processor.__class__.__name__,
        "has_tokenizer": tokenizer_ok,
        "has_image_processor": image_processor_ok,
        "token_shapes": token_shapes,
        "pixel_shapes": pixel_shapes,
        "combined_shapes": combined_shapes,
    }

    lines = [
        "# OpenVLA Processor Smoke Report",
        "",
        "## Status",
        "",
        "- OPENVLA_PROCESSOR_SMOKE_PASS",
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
        "This smoke test loads the OpenVLA processor/tokenizer/image processor only.",
        "It does not load openvla-7b model weights and does not start training.",
    ]

    Path(args.out).write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {args.out}")
    print("OPENVLA_PROCESSOR_SMOKE_PASS")
    print("MODEL_WEIGHTS_NOT_LOADED")
    print("TRAINING_NOT_STARTED")


if __name__ == "__main__":
    main()
