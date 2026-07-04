"""CPU-only smoke test for the OpenVLA-OFT UAV dataset adapter interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.openvla_uav_transfer.datasets import OpenVLAOFTUavCollator, UavJsonlDataset


def _shape_ok(actual: list[int], expected: list[int]) -> bool:
    return actual == expected


def _assert_shape(name: str, actual: list[int], expected: list[int]) -> None:
    if not _shape_ok(actual, expected):
        raise ValueError(f"{name} shape mismatch: expected {expected}, got {actual}")


def _batch_has_cross_episode_shuffle(batch: dict[str, Any]) -> bool:
    pairs = list(zip(batch["episode_ids"], batch["step_ids"]))
    return any(left[0] == right[0] and right[1] < left[1] for left, right in zip(pairs, pairs[1:]))


def run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    dataset = UavJsonlDataset(
        jsonl_paths=[Path(path) for path in args.jsonl],
        image_root=Path(args.image_root) if args.image_root else None,
        stats_path=Path(args.stats) if args.stats else None,
        require_image_exists=args.check_images,
        normalize=args.normalize,
        max_rows=args.max_rows,
    )
    batch_size = min(args.batch_size, len(dataset))
    samples = [dataset[idx] for idx in range(batch_size)]
    collator = OpenVLAOFTUavCollator(
        expected_action_chunk_size=args.action_chunk_size,
        require_normalized=args.normalize,
    )
    batch = collator(samples)

    _assert_shape("states", batch["shapes"]["states"], [batch_size, 4])
    _assert_shape("actions", batch["shapes"]["actions"], [batch_size, 4])
    _assert_shape("action_chunks", batch["shapes"]["action_chunks"], [batch_size, args.action_chunk_size, 4])
    _assert_shape("dts", batch["shapes"]["dts"], [batch_size])
    if args.normalize:
        _assert_shape("states_normalized", batch["shapes"]["states_normalized"], [batch_size, 4])
        _assert_shape("actions_normalized", batch["shapes"]["actions_normalized"], [batch_size, 4])
        _assert_shape("action_chunks_normalized", batch["shapes"]["action_chunks_normalized"], [batch_size, args.action_chunk_size, 4])

    if len(batch["image_paths"]) != batch_size:
        raise ValueError("image path batch length mismatch")
    if len(batch["instructions"]) != batch_size:
        raise ValueError("instruction batch length mismatch")
    if not all(isinstance(text, str) and text.strip() for text in batch["instructions"]):
        raise ValueError("batch contains empty instruction")
    if _batch_has_cross_episode_shuffle(batch):
        raise ValueError("batch step order appears shuffled inside an episode")

    result = {
        "jsonl": [Path(path).as_posix() for path in args.jsonl],
        "dataset_summary": dataset.summary(),
        "batch_size": batch_size,
        "batch_shapes": batch["shapes"],
        "openvla_oft_mapping": batch["openvla_oft_mapping"],
        "first_batch_ref": {
            "episode_id": batch["episode_ids"][0],
            "step_id": batch["step_ids"][0],
            "image_path": batch["image_paths"][0],
            "instruction_chars": len(batch["instructions"][0]),
            "state": batch["states"][0],
            "action": batch["actions"][0],
            "action_chunk_len": len(batch["action_chunks"][0]),
            "dt": batch["dts"][0],
            "map": batch["sources"][0].get("map"),
        },
        "status": "ADAPTER_SMOKE_PASS",
    }
    return result


def write_report(result: dict[str, Any], out: Path) -> None:
    lines = [
        "# OpenVLA-OFT UAV Adapter Smoke Report",
        "",
        "This report validates only the CPU-side dataset adapter shape contract. It does not load OpenVLA-OFT, does not train a model, and does not run simulator evaluation.",
        "",
        "## Inputs",
    ]
    for path in result["jsonl"]:
        lines.append(f"- `{path}`")
    lines.extend(
        [
            "",
            "## Dataset Summary",
            "",
            f"- Rows loaded: `{result['dataset_summary']['rows']}`",
            f"- Maps: `{result['dataset_summary']['maps']}`",
            f"- action chunk lengths: `{result['dataset_summary']['action_chunk_lengths']}`",
            f"- dt sources: `{result['dataset_summary']['dt_sources']}`",
            f"- normalized: `{result['dataset_summary']['normalized']}`",
            f"- stats path: `{result['dataset_summary']['stats_path']}`",
            "",
            "## Batch Contract",
            "",
            f"- Batch size: `{result['batch_size']}`",
            f"- Shapes: `{result['batch_shapes']}`",
            "",
            "## OpenVLA-OFT Field Mapping",
            "",
        ]
    )
    for key, value in result["openvla_oft_mapping"].items():
        lines.append(f"- `{key}` <- `{value}`")
    lines.extend(
        [
            "",
            "## First Sample",
            "",
            "```json",
            json.dumps(result["first_batch_ref"], ensure_ascii=False, indent=2),
            "```",
            "",
            "## Status",
            "",
            f"- `{result['status']}`",
            "- `NOT_TRAINING_READY`: this remains a debug subset and an interface smoke test, not a final OpenVLA-OFT training dataset.",
        ]
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", nargs="+", default=["data/debug/traveluav_BrushifyCountryRoads_debug.jsonl"])
    parser.add_argument("--image-root", default=".")
    parser.add_argument("--stats", default="data/debug/traveluav_3maps_stats.json")
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--check-images", action="store_true")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--action-chunk-size", type=int, default=8)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--out", default="docs/openvla_oft_adapter_smoke_report.md")
    args = parser.parse_args()
    try:
        result = run_smoke(args)
        write_report(result, Path(args.out))
    except Exception as exc:
        print(f"ADAPTER_SMOKE_FAIL: {exc}")
        raise SystemExit(1) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("ADAPTER_SMOKE_PASS: OpenVLA-OFT UAV adapter batch contract is valid without model loading.")


if __name__ == "__main__":
    main()
