"""Check OpenVLA-OFT-style UAV JSONL debug files."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean
from typing import Any


ACTION_NAMES = ("vx", "vy", "vz", "yaw_rate")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _check_vector(row_id: int, row: dict[str, Any], key: str, size: int) -> list[float]:
    value = row.get(key)
    if not isinstance(value, list) or len(value) != size:
        raise ValueError(f"line {row_id}: `{key}` must be a {size}D list")
    if not all(_is_number(v) for v in value):
        raise ValueError(f"line {row_id}: `{key}` contains non-numeric or NaN values")
    return [float(v) for v in value]


def _check_action_chunk(row_id: int, row: dict[str, Any]) -> None:
    chunk = row.get("action_chunk")
    if not isinstance(chunk, list) or not chunk:
        raise ValueError(f"line {row_id}: `action_chunk` must be a non-empty list")
    for idx, action in enumerate(chunk):
        if not isinstance(action, list) or len(action) != 4 or not all(_is_number(v) for v in action):
            raise ValueError(f"line {row_id}: `action_chunk[{idx}]` must be a numeric 4D list")


def check_jsonl(jsonl: Path, image_root: Path | None, max_show: int) -> None:
    if not jsonl.exists():
        raise ValueError(f"{jsonl} does not exist")

    rows: list[dict[str, Any]] = []
    actions: list[list[float]] = []
    missing_image_files = 0

    with jsonl.open("r", encoding="utf-8") as f:
        for line_id, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {line_id}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"line {line_id}: row must be a JSON object")
            image = row.get("image")
            if not isinstance(image, str) or not image:
                raise ValueError(f"line {line_id}: missing non-empty `image`")
            instruction = row.get("instruction")
            if not isinstance(instruction, str):
                raise ValueError(f"line {line_id}: `instruction` must be a string")
            _check_vector(line_id, row, "state", 4)
            action = _check_vector(line_id, row, "action", 4)
            _check_action_chunk(line_id, row)
            if image_root is not None:
                image_path = Path(image)
                if not image_path.is_absolute():
                    image_path = image_root / image_path
                if not image_path.exists():
                    missing_image_files += 1
            rows.append(row)
            actions.append(action)

    if not rows:
        raise ValueError("JSONL contains no rows")

    print(f"Rows: {len(rows)}")
    if missing_image_files:
        print(f"WARNING: {missing_image_files} image path(s) do not exist under image-root")
    for dim, name in enumerate(ACTION_NAMES):
        values = [action[dim] for action in actions]
        print(f"{name}: min={min(values):.6f}, max={max(values):.6f}, mean={mean(values):.6f}")
    print("Samples:")
    for row in rows[:max_show]:
        print(json.dumps(row, ensure_ascii=False))
    print("CHECK_PASS: traveluav_debug.jsonl format looks valid.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", default="data/debug/traveluav_debug.jsonl")
    parser.add_argument("--image-root", default=None)
    parser.add_argument("--max-show", type=int, default=5)
    args = parser.parse_args()
    try:
        check_jsonl(Path(args.jsonl), Path(args.image_root) if args.image_root else None, args.max_show)
    except Exception as exc:
        print(f"CHECK_FAIL: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
