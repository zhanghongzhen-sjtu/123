"""Smoke-test the CPU-only UAV JSONL dataset loader."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean
from typing import Any

from src.openvla_uav_transfer.datasets import UavJsonlDataset


def _max_abs(values: list[float]) -> float:
    return max(abs(value) for value in values) if values else 0.0


def _vector_ok(value: Any, size: int) -> bool:
    return (
        isinstance(value, list)
        and len(value) == size
        and all(isinstance(item, (int, float)) and not isinstance(item, bool) and math.isfinite(float(item)) for item in value)
    )


def smoke_test(args: argparse.Namespace) -> None:
    dataset = UavJsonlDataset(
        jsonl_paths=[Path(path) for path in args.jsonl],
        image_root=Path(args.image_root) if args.image_root else None,
        stats_path=Path(args.stats) if args.stats else None,
        require_image_exists=args.check_images,
        normalize=args.normalize,
        max_rows=args.max_rows,
    )
    summary = dataset.summary()
    print("Dataset summary:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    dt_values = [row["dt"] for row in dataset.rows]
    print(f"dt: min={min(dt_values):.6f}, max={max(dt_values):.6f}, mean={mean(dt_values):.6f}")

    first = dataset[0]
    required = ("image_path", "instruction", "state", "action", "action_chunk", "dt", "source")
    missing = [key for key in required if key not in first]
    if missing:
        raise ValueError(f"first sample missing fields: {missing}")
    if not _vector_ok(first["state"], 4):
        raise ValueError("first sample state is not 4D numeric")
    if not _vector_ok(first["action"], 4):
        raise ValueError("first sample action is not 4D numeric")
    if not first["action_chunk"] or not all(_vector_ok(action, 4) for action in first["action_chunk"]):
        raise ValueError("first sample action_chunk is invalid")

    print("First sample preview:")
    preview = {
        "episode_id": first["episode_id"],
        "step_id": first["step_id"],
        "map": first.get("source", {}).get("map"),
        "image_path": first["image_path"],
        "instruction_chars": len(first["instruction"]),
        "state": first["state"],
        "action": first["action"],
        "action_chunk_len": len(first["action_chunk"]),
        "dt": first["dt"],
    }
    if args.normalize:
        preview["state_normalized_max_abs"] = _max_abs(first["state_normalized"])
        preview["action_normalized_max_abs"] = _max_abs(first["action_normalized"])
        preview["action_chunk_normalized_len"] = len(first["action_chunk_normalized"])
    print(json.dumps(preview, ensure_ascii=False, indent=2))
    print("SMOKE_PASS: UAV JSONL dataset loader works without model loading.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--jsonl",
        nargs="+",
        default=["data/debug/traveluav_3maps_debug.jsonl"],
        help="One or more UAV JSONL files.",
    )
    parser.add_argument("--image-root", default=".", help="Root used to resolve relative image paths.")
    parser.add_argument("--stats", default=None, help="Optional stats JSON with normalization vectors.")
    parser.add_argument("--normalize", action="store_true", help="Attach normalized state/action fields.")
    parser.add_argument("--check-images", action="store_true", help="Require image files to exist.")
    parser.add_argument("--max-rows", type=int, default=None, help="Optional row limit for quick smoke tests.")
    args = parser.parse_args()
    try:
        smoke_test(args)
    except Exception as exc:
        print(f"SMOKE_FAIL: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
