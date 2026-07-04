"""Compute lightweight statistics for UAV OpenVLA-style JSONL files."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


SCHEMA_VERSION = "uav_openvla_jsonl_v0.1"
STATE_NAMES = ("x", "y", "z", "yaw")
ACTION_NAMES = ("vx", "vy", "vz", "yaw_rate")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _vector(value: Any, size: int, field_name: str, row_ref: str) -> list[float]:
    if not isinstance(value, list) or len(value) != size:
        raise ValueError(f"{row_ref}: `{field_name}` must be a {size}D list")
    if not all(_is_number(item) for item in value):
        raise ValueError(f"{row_ref}: `{field_name}` contains non-numeric or non-finite values")
    return [float(item) for item in value]


def _load_rows(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        if not path.exists():
            raise ValueError(f"{path} does not exist")
        with path.open("r", encoding="utf-8") as f:
            for line_id, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                row_ref = f"{path}:{line_id}"
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{row_ref}: invalid JSON: {exc}") from exc
                if not isinstance(row, dict):
                    raise ValueError(f"{row_ref}: row must be a JSON object")
                row["_stats_file"] = path.as_posix()
                row["_stats_line"] = line_id
                rows.append(row)
    if not rows:
        raise ValueError("No JSONL rows found")
    return rows


def _quantile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        raise ValueError("Cannot compute quantile of empty values")
    if len(sorted_values) == 1:
        return sorted_values[0]
    q = min(1.0, max(0.0, q))
    pos = q * (len(sorted_values) - 1)
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return sorted_values[lo]
    weight = pos - lo
    return sorted_values[lo] * (1.0 - weight) + sorted_values[hi] * weight


def _stats(values: list[float]) -> dict[str, float]:
    if not values:
        raise ValueError("Cannot compute stats of empty values")
    ordered = sorted(values)
    avg = mean(values)
    variance = mean([(value - avg) ** 2 for value in values])
    return {
        "count": len(values),
        "min": ordered[0],
        "max": ordered[-1],
        "mean": avg,
        "std": math.sqrt(variance),
        "median": median(ordered),
        "q01": _quantile(ordered, 0.01),
        "q05": _quantile(ordered, 0.05),
        "q95": _quantile(ordered, 0.95),
        "q99": _quantile(ordered, 0.99),
    }


def _named_vector_stats(names: tuple[str, ...], values_by_dim: dict[str, list[float]]) -> dict[str, dict[str, float]]:
    return {name: _stats(values_by_dim[name]) for name in names}


def _mean_vector(names: tuple[str, ...], stats: dict[str, dict[str, float]]) -> list[float]:
    return [stats[name]["mean"] for name in names]


def _std_vector(names: tuple[str, ...], stats: dict[str, dict[str, float]]) -> list[float]:
    return [stats[name]["std"] for name in names]


def _min_vector(names: tuple[str, ...], stats: dict[str, dict[str, float]]) -> list[float]:
    return [stats[name]["min"] for name in names]


def _max_vector(names: tuple[str, ...], stats: dict[str, dict[str, float]]) -> list[float]:
    return [stats[name]["max"] for name in names]


def _check_action_chunk(row_ref: str, chunk: Any) -> int:
    if not isinstance(chunk, list) or not chunk:
        raise ValueError(f"{row_ref}: `action_chunk` must be a non-empty list")
    for idx, action in enumerate(chunk):
        _vector(action, 4, f"action_chunk[{idx}]", row_ref)
    return len(chunk)


def compute_stats(paths: list[Path]) -> dict[str, Any]:
    rows = _load_rows(paths)
    per_map: dict[str, dict[str, Any]] = defaultdict(lambda: {"rows": 0, "episodes": set()})
    dt_values: list[float] = []
    state_values: dict[str, list[float]] = {name: [] for name in STATE_NAMES}
    action_values: dict[str, list[float]] = {name: [] for name in ACTION_NAMES}
    chunk_lengths: Counter[int] = Counter()
    dt_sources: Counter[str] = Counter()
    input_files: Counter[str] = Counter()
    instruction_lengths: list[float] = []

    for row in rows:
        row_ref = f"{row['_stats_file']}:{row['_stats_line']}"
        source = row.get("source") if isinstance(row.get("source"), dict) else {}
        map_name = str(source.get("map") or row.get("map") or "unknown")
        episode_id = str(row.get("episode_id") or "unknown")
        per_map[map_name]["rows"] += 1
        per_map[map_name]["episodes"].add(episode_id)
        input_files[str(row["_stats_file"])] += 1

        instruction = row.get("instruction")
        if not isinstance(instruction, str) or not instruction.strip():
            raise ValueError(f"{row_ref}: `instruction` must be a non-empty string")
        instruction_lengths.append(float(len(instruction)))

        image = row.get("image")
        if not isinstance(image, str) or not image:
            raise ValueError(f"{row_ref}: `image` must be a non-empty string")

        state = _vector(row.get("state"), 4, "state", row_ref)
        action = _vector(row.get("action"), 4, "action", row_ref)
        for idx, name in enumerate(STATE_NAMES):
            state_values[name].append(state[idx])
        for idx, name in enumerate(ACTION_NAMES):
            action_values[name].append(action[idx])

        chunk_lengths[_check_action_chunk(row_ref, row.get("action_chunk"))] += 1

        dt = row.get("dt")
        if not _is_number(dt) or float(dt) <= 0:
            raise ValueError(f"{row_ref}: `dt` must be a positive finite number")
        dt_values.append(float(dt))
        dt_sources[str(source.get("dt_source") or "unknown")] += 1

    state_stats = _named_vector_stats(STATE_NAMES, state_values)
    action_stats = _named_vector_stats(ACTION_NAMES, action_values)
    map_summary = {
        map_name: {
            "rows": info["rows"],
            "episodes": len(info["episodes"]),
        }
        for map_name, info in sorted(per_map.items())
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "inputs": dict(sorted(input_files.items())),
        "row_count": len(rows),
        "per_map": map_summary,
        "dt": _stats(dt_values),
        "dt_sources": dict(sorted(dt_sources.items())),
        "state": {
            "names": list(STATE_NAMES),
            "by_dimension": state_stats,
            "normalization": {
                "mean": _mean_vector(STATE_NAMES, state_stats),
                "std": _std_vector(STATE_NAMES, state_stats),
                "min": _min_vector(STATE_NAMES, state_stats),
                "max": _max_vector(STATE_NAMES, state_stats),
            },
        },
        "action": {
            "names": list(ACTION_NAMES),
            "by_dimension": action_stats,
            "normalization": {
                "mean": _mean_vector(ACTION_NAMES, action_stats),
                "std": _std_vector(ACTION_NAMES, action_stats),
                "min": _min_vector(ACTION_NAMES, action_stats),
                "max": _max_vector(ACTION_NAMES, action_stats),
            },
        },
        "action_chunk_lengths": {str(length): count for length, count in sorted(chunk_lengths.items())},
        "instruction_length": _stats(instruction_lengths),
    }


def _fmt(value: float) -> str:
    return f"{value:.6f}"


def _stats_line(stats: dict[str, float]) -> str:
    return (
        f"min={_fmt(stats['min'])}, max={_fmt(stats['max'])}, mean={_fmt(stats['mean'])}, "
        f"std={_fmt(stats['std'])}, median={_fmt(stats['median'])}, "
        f"q01={_fmt(stats['q01'])}, q99={_fmt(stats['q99'])}"
    )


def write_markdown(stats: dict[str, Any], out: Path) -> None:
    lines = [
        "# TravelUAV 3-Map Statistics",
        "",
        "This report is generated from lightweight debug JSONL files. It is suitable for schema validation and future normalization planning, but it is not a final full-dataset training statistic.",
        "",
        "## Inputs",
    ]
    for path, count in stats["inputs"].items():
        lines.append(f"- `{path}`: `{count}` rows")
    lines.extend(
        [
            "",
            "## Summary",
            f"- Schema version: `{stats['schema_version']}`",
            f"- Rows: `{stats['row_count']}`",
            f"- dt sources: `{stats['dt_sources']}`",
            f"- action chunk lengths: `{stats['action_chunk_lengths']}`",
            "",
            "## Per-Map Counts",
            "",
            "| Map | Rows | Episodes |",
            "| --- | ---: | ---: |",
        ]
    )
    for map_name, info in stats["per_map"].items():
        lines.append(f"| {map_name} | {info['rows']} | {info['episodes']} |")

    lines.extend(
        [
            "",
            "## Timing",
            "",
            f"- `dt`: {_stats_line(stats['dt'])}",
            "",
            "## State Statistics",
            "",
            "| Dimension | Stats |",
            "| --- | --- |",
        ]
    )
    for name in STATE_NAMES:
        lines.append(f"| {name} | {_stats_line(stats['state']['by_dimension'][name])} |")

    lines.extend(
        [
            "",
            "State normalization vectors:",
            "",
            f"- mean: `{stats['state']['normalization']['mean']}`",
            f"- std: `{stats['state']['normalization']['std']}`",
            f"- min: `{stats['state']['normalization']['min']}`",
            f"- max: `{stats['state']['normalization']['max']}`",
            "",
            "## Action Statistics",
            "",
            "| Dimension | Stats |",
            "| --- | --- |",
        ]
    )
    for name in ACTION_NAMES:
        lines.append(f"| {name} | {_stats_line(stats['action']['by_dimension'][name])} |")

    lines.extend(
        [
            "",
            "Action normalization vectors:",
            "",
            f"- mean: `{stats['action']['normalization']['mean']}`",
            f"- std: `{stats['action']['normalization']['std']}`",
            f"- min: `{stats['action']['normalization']['min']}`",
            f"- max: `{stats['action']['normalization']['max']}`",
            "",
            "## Instruction Length",
            "",
            f"- characters: {_stats_line(stats['instruction_length'])}",
            "",
            "## Boundary",
            "",
            "These statistics come from three small debug subsets only. Full training normalization must be recomputed from the actual training split on the 5090 stage before model training.",
        ]
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", nargs="+", default=["data/debug/traveluav_3maps_debug.jsonl"])
    parser.add_argument("--out-json", default="data/debug/traveluav_3maps_stats.json")
    parser.add_argument("--out-md", default="docs/traveluav_3maps_stats.md")
    args = parser.parse_args()

    stats = compute_stats([Path(path) for path in args.jsonl])
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(stats, Path(args.out_md))

    print(f"Rows: {stats['row_count']}")
    print(f"Maps: {len(stats['per_map'])}")
    print(f"Wrote JSON stats: {out_json}")
    print(f"Wrote Markdown stats: {args.out_md}")
    print("STATS_PASS: UAV JSONL statistics computed.")


if __name__ == "__main__":
    main()
