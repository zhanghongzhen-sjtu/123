import argparse
import json
from pathlib import Path

import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq


def first_row(jsonl):
    with Path(jsonl).open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                return json.loads(line)
    raise RuntimeError("empty jsonl")


def to_device(batch, device):
    out = {}
    for k, v in batch.items():
        if torch.is_tensor(v):
            if v.dtype.is_floating_point:
                out[k] = v.to(device=device, dtype=torch.bfloat16)
            else:
                out[k] = v.to(device=device)
        else:
            out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", default="data/processed/clean_train_timestamp_maps.jsonl")
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--model-id", default="openvla/openvla-7b")
    ap.add_argument("--cache-dir", default="/root/autodl-tmp/hf-cache")
    ap.add_argument("--out", default="docs/openvla_one_batch_forward_smoke_report.md")
    args = ap.parse_args()

    row = first_row(args.jsonl)
    img_path = Path(row["image"])
    if not img_path.is_absolute():
        img_path = Path(args.image_root) / img_path
    image = Image.open(img_path).convert("RGB")

    instruction = row["instruction"]
    prompt = f"What action should the robot take to {instruction}?"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    assert device == "cuda", "RTX 5090 CUDA device is required for this smoke"

    processor = AutoProcessor.from_pretrained(
        args.model_id,
        trust_remote_code=True,
        cache_dir=args.cache_dir,
    )

    inputs = processor(text=prompt, images=image, return_tensors="pt")
    inputs = to_device(inputs, device)

    load_kwargs = dict(
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        cache_dir=args.cache_dir,
    )

    try:
        model = AutoModelForVision2Seq.from_pretrained(
            args.model_id,
            attn_implementation="eager",
            **load_kwargs,
        )
    except TypeError:
        model = AutoModelForVision2Seq.from_pretrained(args.model_id, **load_kwargs)

    model = model.to(device)
    model.eval()

    result = {
        "status": "OPENVLA_ONE_BATCH_FORWARD_SMOKE_PASS",
        "model_id": args.model_id,
        "device": device,
        "image_path": str(img_path),
        "instruction_chars": len(instruction),
        "training_started": False,
        "lora_oft_started": False,
        "closed_loop_eval_started": False,
        "input_shapes": {k: list(v.shape) for k, v in inputs.items() if torch.is_tensor(v)},
    }

    with torch.no_grad():
        try:
            gen = model.generate(**inputs, max_new_tokens=1, do_sample=False)
            result["generate_shape"] = list(gen.shape)
            result["forward_mode"] = "generate_max_new_tokens_1"
        except Exception as gen_exc:
            result["generate_error"] = str(gen_exc)[:500]
            out = model(**inputs)
            result["forward_mode"] = "model_forward"
            if hasattr(out, "logits") and out.logits is not None:
                result["logits_shape"] = list(out.logits.shape)

    if torch.cuda.is_available():
        result["cuda_max_memory_gb"] = round(torch.cuda.max_memory_allocated() / 1024**3, 3)

    lines = [
        "# OpenVLA One-Batch Forward Smoke Report",
        "",
        "## Status",
        "",
        "- OPENVLA_ONE_BATCH_FORWARD_SMOKE_PASS",
        "- MODEL_WEIGHTS_LOADED_FOR_SMOKE",
        "- TRAINING_NOT_STARTED",
        "- LORA_OFT_NOT_STARTED",
        "",
        "## Result",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2),
        "```",
    ]

    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"WROTE {args.out}")
    print("OPENVLA_ONE_BATCH_FORWARD_SMOKE_PASS")
    print("TRAINING_NOT_STARTED")


if __name__ == "__main__":
    main()
