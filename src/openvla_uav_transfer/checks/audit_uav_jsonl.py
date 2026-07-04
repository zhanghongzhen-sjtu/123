"""Audit UAV JSONL files and write a lightweight Markdown report."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


ACTION_NAMES = ("vx", "vy", "vz", "yaw_rate")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _stats(values: list[float]) -> dict[str, float] | None:
    if not values:
        return None
    return {
        "min": min(values),
        "max": max(values),
        "mean": mean(values),
        "median": median(values),
    }


def _fmt_stats(values: list[float]) -> str:
    stats = _stats(values)
    if stats is None:
        return "n/a"
    return (
        f"min={stats['min']:.6f}, max={stats['max']:.6f}, "
        f"mean={stats['mean']:.6f}, median={stats['median']:.6f}"
    )


def _fmt_mean(values: list[float]) -> str:
    stats = _stats(values)
    return f"{stats['mean']:.6f}" if stats else "n/a"


def _vector(value: Any, size: int) -> list[float] | None:
    if not isinstance(value, list) or len(value) < size:
        return None
    if not all(_is_number(item) for item in value[:size]):
        return None
    return [float(item) for item in value[:size]]


def _load_rows(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line_id, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_id}: invalid JSON: {exc}") from exc
                if not isinstance(row, dict):
                    raise ValueError(f"{path}:{line_id}: row is not an object")
                row["_audit_file"] = path.as_posix()
                row["_audit_line"] = line_id
                rows.append(row)
    return rows


def _image_exists(image: str, image_root: Path | None) -> bool:
    image_path = Path(image)
    if not image_path.is_absolute() and image_root is not None:
        image_path = image_root / image_path
    return image_path.exists()


def audit(paths: list[Path], out: Path, image_root: Path | None) -> None:
    rows = _load_rows(paths)
    if not rows:
        raise ValueError("No rows found")

    maps: dict[str, list[dict[str, Any]]] = defaultdict(list)
    episodes_by_map: dict[str, set[str]] = defaultdict(set)
    dt_values: list[float] = []
    frame_deltas: list[float] = []
    action_values: dict[str, list[float]] = {name: [] for name in ACTION_NAMES}
    raw_linear_abs_errors: dict[str, list[float]] = {name: [] for name in ACTION_NAMES[:3]}
    raw_yaw_abs_errors: list[float] = []
    raw_linear_abs_errors_nonzero: dict[str, list[float]] = {name: [] for name in ACTION_NAMES[:3]}
    raw_yaw_abs_errors_nonzero: list[float] = []
    dt_sources: Counter[str] = Counter()
    issues: Counter[str] = Counter()

    for row in rows:
        source = row.get("source") if isinstance(row.get("source"), dict) else {}
        map_name = str(source.get("map") or row.get("map") or "unknown")
        episode_id = str(row.get("episode_id") or "unknown")
        maps[map_name].append(row)
        episodes_by_map[map_name].add(episode_id)

        image = row.get("image")
        if not isinstance(image, str) or not image:
            issues["missing_image_field"] += 1
        elif image_root is not None and not _image_exists(image, image_root):
            issues["missing_image_file"] += 1

        instruction = row.get("instruction")
        if not isinstance(instruction, str) or not instruction.strip():
            issues["missing_instruction"] += 1

        state = _vector(row.get("state"), 4)
        action = _vector(row.get("action"), 4)
        if state is None:
            issues["bad_state"] += 1
        if action is None:
            issues["bad_action"] += 1
            continue

        chunk = row.get("action_chunk")
        if not isinstance(chunk, list) or not chunk or any(_vector(item, 4) is None for item in chunk):
            issues["bad_action_chunk"] += 1

        dt = row.get("dt")
        if _is_number(dt) and float(dt) > 0:
            dt_values.append(float(dt))
        else:
            issues["bad_dt"] += 1

        dt_sources[str(source.get("dt_source") or "unknown")] += 1
        frame = source.get("frame")
        next_frame = source.get("next_frame")
        if _is_number(frame) and _is_number(next_frame):
            frame_deltas.append(float(next_frame) - float(frame))

        for idx, name in enumerate(ACTION_NAMES):
            action_values[name].append(action[idx])

        raw_linear = _vector(source.get("raw_linear_velocity"), 3)
        if raw_linear is not None:
            raw_speed = math.sqrt(sum(v * v for v in raw_linear))
            for idx, name in enumerate(ACTION_NAMES[:3]):
                err = abs(action[idx] - raw_linear[idx])
                raw_linear_abs_errors[name].append(err)
                if raw_speed > 1e-6:
                    raw_linear_abs_errors_nonzero[name].append(err)

        raw_angular = _vector(source.get("raw_angular_velocity"), 3)
        if raw_angular is not None:
            err = abs(action[3] - raw_angular[2])
            raw_yaw_abs_errors.append(err)
            if abs(raw_angular[2]) > 1e-6:
                raw_yaw_abs_errors_nonzero.append(err)

    lines = [
        "# TravelUAV 3-Map JSONL Audit",
        "",
        "## Inputs",
    ]
    for path in paths:
        lines.append(f"- `{path.as_posix()}`")
    lines.extend(
        [
            "",
            "## Summary",
            f"- Rows: `{len(rows)}`",
            f"- Maps: `{len(maps)}`",
            f"- Episodes: `{sum(len(v) for v in episodes_by_map.values())}`",
            f"- Image root checked: `{image_root.as_posix() if image_root else 'not checked'}`",
            f"- Issues: `{dict(issues) if issues else 'none'}`",
            "",
            "## Per-Map Counts",
            "",
            "| Map | Rows | Episodes |",
            "| --- | ---: | ---: |",
        ]
    )
    for map_name in sorted(maps):
        lines.append(f"| {map_name} | {len(maps[map_name])} | {len(episodes_by_map[map_name])} |")

    lines.extend(
        [
            "",
            "## Timing",
            f"- `dt`: {_fmt_stats(dt_values)}",
            f"- frame delta: {_fmt_stats(frame_deltas)}",
            f"- dt sources: `{dict(dt_sources)}`",
            "",
            "## Action Statistics",
            "",
            "| Dimension | Stats |",
            "| --- | --- |",
        ]
    )
    for name in ACTION_NAMES:
        lines.append(f"| {name} | {_fmt_stats(action_values[name])} |")

    lines.extend(
        [
            "",
            "## Raw Velocity Consistency",
            "",
            "The converted action velocity is compared with the current raw log `linear_velocity` and `angular_velocity[2]`. "
            "The first frame of an episode often has zero raw velocity, so nonzero-only errors are also reported.",
            "",
            "| Quantity | All rows mean abs error | Nonzero raw rows mean abs error |",
            "| --- | ---: | ---: |",
        ]
    )
    for name in ACTION_NAMES[:3]:
        lines.append(
            f"| {name} vs raw linear | "
            f"{_fmt_mean(raw_linear_abs_errors[name])} | "
            f"{_fmt_mean(raw_linear_abs_errors_nonzero[name])} |"
        )
    lines.append(
        f"| yaw_rate vs raw angular z | "
        f"{_fmt_mean(raw_yaw_abs_errors)} | "
        f"{_fmt_mean(raw_yaw_abs_errors_nonzero)} |"
    )

    lines.extend(
        [
            "",
            "## Sample Rows",
            "",
        ]
    )
    for row in rows[:3]:
        compact = {
            "map": row.get("source", {}).get("map"),
            "episode_id": row.get("episode_id"),
            "step_id": row.get("step_id"),
            "frame": row.get("source", {}).get("frame"),
            "next_frame": row.get("source", {}).get("next_frame"),
            "dt": row.get("dt"),
            "dt_source": row.get("source", {}).get("dt_source"),
            "state": row.get("state"),
            "action": row.get("action"),
            "image": row.get("image"),
        }
        lines.append("```json")
        lines.append(json.dumps(compact, ensure_ascii=False, indent=2))
        lines.append("```")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote audit report to {out}")
    print(f"Rows: {len(rows)}")
    print(f"Issues: {dict(issues) if issues else 'none'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", nargs="+", required=True)
    parser.add_argument("--out", default="docs/traveluav_3maps_audit.md")
    parser.add_argument("--image-root", default=None)
    args = parser.parse_args()
    audit(
        paths=[Path(path) for path in args.jsonl],
        out=Path(args.out),
        image_root=Path(args.image_root) if args.image_root else None,
    )


if __name__ == "__main__":
    main()
