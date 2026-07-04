"""Strict validation report for TravelUAV OpenVLA-style debug JSONL files."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from src.openvla_uav_transfer.utils.geometry import wrap_angle


REQUIRED_FIELDS = (
    "dataset",
    "episode_id",
    "step_id",
    "image",
    "instruction",
    "state",
    "action",
    "action_chunk",
    "dt",
    "source",
)
ACTION_NAMES = ("vx", "vy", "vz", "yaw_rate")
DEFAULT_CANDIDATES = (
    "data/debug/traveluav_real_debug.jsonl",
    "data/debug/traveluav_BrushifyCountryRoads_debug.jsonl",
    "data/debug/traveluav_3maps_debug.jsonl",
)
EPS = 1e-9
ACTION_TOL = 1e-6


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _vector(value: Any, size: int) -> list[float] | None:
    if not isinstance(value, list) or len(value) != size:
        return None
    if not all(_is_number(item) for item in value):
        return None
    return [float(item) for item in value]


def _same_vector(left: list[float], right: list[float], tol: float = ACTION_TOL) -> bool:
    return len(left) == len(right) and all(abs(a - b) <= tol for a, b in zip(left, right))


def _resolve_image(image: str, image_root: Path | None) -> Path:
    path = Path(image)
    if path.is_absolute():
        return path
    if image_root is not None:
        return image_root / path
    return path


def _load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_id, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                row = {"_json_error": str(exc)}
            if not isinstance(row, dict):
                row = {"_row_error": "row is not a JSON object"}
            row["_line_id"] = line_id
            rows.append(row)
    return rows


def _select_jsonl(candidates: list[Path]) -> tuple[Path, list[str]]:
    notes: list[str] = []
    for path in candidates:
        if path.exists():
            notes.append(f"Selected `{path.as_posix()}`.")
            return path, notes
        notes.append(f"Candidate missing: `{path.as_posix()}`.")
    raise FileNotFoundError("No candidate JSONL file exists")


def _recompute_action(state: list[float], next_state: list[float], dt: float) -> list[float]:
    return [
        (next_state[0] - state[0]) / dt,
        (next_state[1] - state[1]) / dt,
        (next_state[2] - state[2]) / dt,
        wrap_angle(next_state[3] - state[3]) / dt,
    ]


def _stats(values: list[float]) -> dict[str, float] | None:
    if not values:
        return None
    return {
        "min": min(values),
        "max": max(values),
        "mean": mean(values),
    }


def _fmt_stats(values: list[float]) -> str:
    stats = _stats(values)
    if stats is None:
        return "n/a"
    return f"min={stats['min']:.9f}, max={stats['max']:.9f}, mean={stats['mean']:.9f}"


def _fmt_error(errors: list[float]) -> str:
    if not errors:
        return "n/a"
    return f"max={max(errors):.12g}, mean={mean(errors):.12g}"


def _is_zero_vector(values: list[float], tol: float = EPS) -> bool:
    return all(abs(value) <= tol for value in values)


def _detect_toy(path: Path, rows: list[dict[str, Any]], image_existing_count: int) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    name = path.name.lower()
    if "toy" in name or name == "traveluav_debug.jsonl":
        reasons.append("filename suggests toy/debug placeholder data")
    raw_markers = 0
    real_source_markers = 0
    for row in rows:
        image = str(row.get("image") or "")
        source = row.get("source") if isinstance(row.get("source"), dict) else {}
        raw_file = str(source.get("raw_file") or "")
        raw_episode_dir = str(source.get("raw_episode_dir") or "")
        if "data/raw/traveluav" in image.lower() or "data/raw/traveluav" in raw_file.lower():
            raw_markers += 1
        if raw_file and Path(raw_file).exists():
            real_source_markers += 1
        elif raw_episode_dir and Path(raw_episode_dir).exists():
            real_source_markers += 1
    if raw_markers == 0:
        reasons.append("no row points to data/raw/TravelUAV")
    if image_existing_count == 0:
        reasons.append("no image file exists locally")
    if real_source_markers == 0:
        reasons.append("no raw source file or raw episode directory exists locally")
    return bool(reasons), reasons


def validate_jsonl(path: Path, image_root: Path | None) -> dict[str, Any]:
    rows = _load_rows(path)
    issues = Counter()
    required_missing = Counter()
    image_existing_count = 0
    instruction_missing = 0
    action_values: dict[str, list[float]] = {name: [] for name in ACTION_NAMES}
    state_zero_count = 0
    action_zero_count = 0
    chunk_zero_count = 0
    linear_action_extreme_count = 0
    yaw_rate_extreme_count = 0
    parsed_rows: list[dict[str, Any]] = []

    for row in rows:
        line_id = row.get("_line_id")
        if "_json_error" in row or "_row_error" in row:
            issues["json_or_row_error"] += 1
            continue
        for field in REQUIRED_FIELDS:
            if field not in row:
                required_missing[field] += 1
                issues["missing_required_field"] += 1

        image = row.get("image")
        if isinstance(image, str) and image:
            if _resolve_image(image, image_root).exists():
                image_existing_count += 1
            else:
                issues["missing_image_file"] += 1
        else:
            issues["bad_image_field"] += 1

        instruction = row.get("instruction")
        if not isinstance(instruction, str) or not instruction.strip():
            instruction_missing += 1
            issues["missing_instruction"] += 1

        state = _vector(row.get("state"), 4)
        action = _vector(row.get("action"), 4)
        if state is None:
            issues["bad_state_format"] += 1
        if action is None:
            issues["bad_action_format"] += 1
        chunk = row.get("action_chunk")
        parsed_chunk: list[list[float]] | None = None
        if not isinstance(chunk, list) or not chunk:
            issues["bad_action_chunk_format"] += 1
        else:
            parsed_chunk = []
            for item in chunk:
                action_item = _vector(item, 4)
                if action_item is None:
                    issues["bad_action_chunk_format"] += 1
                    parsed_chunk = None
                    break
                parsed_chunk.append(action_item)

        dt = row.get("dt")
        if not _is_number(dt) or float(dt) <= 0:
            issues["bad_dt"] += 1

        source = row.get("source")
        if not isinstance(source, dict):
            issues["bad_source_format"] += 1

        episode_id = row.get("episode_id")
        step_id = row.get("step_id")
        if not isinstance(episode_id, str) or not episode_id:
            issues["bad_episode_id"] += 1
        if not isinstance(step_id, int) or isinstance(step_id, bool) or step_id < 0:
            issues["bad_step_id"] += 1

        if state is not None and _is_zero_vector(state):
            state_zero_count += 1
        if action is not None:
            if _is_zero_vector(action):
                action_zero_count += 1
            if any(abs(value) > 20.0 for value in action[:3]):
                linear_action_extreme_count += 1
            if abs(action[3]) > math.pi:
                yaw_rate_extreme_count += 1
            for idx, name in enumerate(ACTION_NAMES):
                action_values[name].append(action[idx])
        if parsed_chunk is not None and all(_is_zero_vector(item) for item in parsed_chunk):
            chunk_zero_count += 1

        if (
            state is not None
            and action is not None
            and parsed_chunk is not None
            and _is_number(dt)
            and float(dt) > 0
            and isinstance(episode_id, str)
            and isinstance(step_id, int)
            and not isinstance(step_id, bool)
        ):
            parsed_rows.append(
                {
                    "line_id": line_id,
                    "episode_id": episode_id,
                    "step_id": step_id,
                    "state": state,
                    "action": action,
                    "action_chunk": parsed_chunk,
                    "dt": float(dt),
                    "source": source if isinstance(source, dict) else {},
                }
            )

    by_episode: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in parsed_rows:
        by_episode[row["episode_id"]].append(row)

    continuity_gaps = 0
    duplicate_steps = 0
    action_errors: dict[str, list[float]] = {name: [] for name in ACTION_NAMES}
    action_recompute_rows = 0
    action_recompute_failures = 0
    uncheckable_terminal_rows = 0
    chunk_first_mismatch = 0
    chunk_known_checks = 0
    chunk_known_mismatches = 0
    chunk_unknown_future_items = 0
    chunk_cross_episode_detected = 0

    for episode_id, episode_rows in by_episode.items():
        episode_rows.sort(key=lambda item: item["step_id"])
        seen_steps: set[int] = set()
        step_to_row = {}
        recomputed_in_episode = 0
        for row in episode_rows:
            step_id = row["step_id"]
            if step_id in seen_steps:
                duplicate_steps += 1
            seen_steps.add(step_id)
            step_to_row[step_id] = row
        for current, nxt in zip(episode_rows, episode_rows[1:]):
            if nxt["step_id"] != current["step_id"] + 1:
                continuity_gaps += 1
                continue
            expected = _recompute_action(current["state"], nxt["state"], current["dt"])
            action_recompute_rows += 1
            recomputed_in_episode += 1
            row_failed = False
            for idx, name in enumerate(ACTION_NAMES):
                err = abs(expected[idx] - current["action"][idx])
                action_errors[name].append(err)
                if err > ACTION_TOL:
                    row_failed = True
            if row_failed:
                action_recompute_failures += 1
        uncheckable_terminal_rows += max(0, len(episode_rows) - recomputed_in_episode)

        first_steps_by_other_episode = set()
        for other_id, other_rows in by_episode.items():
            if other_id == episode_id or not other_rows:
                continue
            other_rows.sort(key=lambda item: item["step_id"])
            first_steps_by_other_episode.add(tuple(round(v, 12) for v in other_rows[0]["action"]))

        for row in episode_rows:
            chunk = row["action_chunk"]
            if not _same_vector(chunk[0], row["action"]):
                chunk_first_mismatch += 1
            for offset, chunk_action in enumerate(chunk):
                expected_row = step_to_row.get(row["step_id"] + offset)
                if expected_row is None:
                    chunk_unknown_future_items += 1
                    rounded_chunk = tuple(round(v, 12) for v in chunk_action)
                    if rounded_chunk in first_steps_by_other_episode:
                        chunk_cross_episode_detected += 1
                    continue
                chunk_known_checks += 1
                if not _same_vector(chunk_action, expected_row["action"]):
                    chunk_known_mismatches += 1

    toy_detected, toy_reasons = _detect_toy(path, rows, image_existing_count)
    image_rate = image_existing_count / len(rows) if rows else 0.0
    format_fail_count = (
        issues["json_or_row_error"]
        + issues["missing_required_field"]
        + issues["bad_image_field"]
        + issues["missing_instruction"]
        + issues["bad_state_format"]
        + issues["bad_action_format"]
        + issues["bad_action_chunk_format"]
        + issues["bad_dt"]
        + issues["bad_source_format"]
        + issues["bad_episode_id"]
        + issues["bad_step_id"]
        + issues["missing_image_file"]
    )
    format_pass = format_fail_count == 0 and not toy_detected
    action_error_values = [err for values in action_errors.values() for err in values]
    action_pass = (
        action_recompute_rows > 0
        and action_recompute_failures == 0
        and continuity_gaps == 0
        and duplicate_steps == 0
        and chunk_first_mismatch == 0
        and chunk_known_mismatches == 0
        and chunk_cross_episode_detected == 0
        and (max(action_error_values) if action_error_values else 0.0) <= ACTION_TOL
    )
    training_ready = False

    return {
        "path": path.as_posix(),
        "row_count": len(rows),
        "parsed_row_count": len(parsed_rows),
        "episode_count": len(by_episode),
        "image_existing_count": image_existing_count,
        "image_existing_rate": image_rate,
        "instruction_missing": instruction_missing,
        "issues": dict(issues),
        "required_missing": dict(required_missing),
        "state_format_errors": issues["bad_state_format"],
        "action_format_errors": issues["bad_action_format"],
        "action_chunk_format_errors": issues["bad_action_chunk_format"],
        "state_zero_count": state_zero_count,
        "action_zero_count": action_zero_count,
        "chunk_zero_count": chunk_zero_count,
        "linear_action_extreme_count": linear_action_extreme_count,
        "yaw_rate_extreme_count": yaw_rate_extreme_count,
        "action_values": action_values,
        "action_errors": action_errors,
        "action_recompute_rows": action_recompute_rows,
        "action_recompute_failures": action_recompute_failures,
        "uncheckable_terminal_rows": uncheckable_terminal_rows,
        "continuity_gaps": continuity_gaps,
        "duplicate_steps": duplicate_steps,
        "chunk_first_mismatch": chunk_first_mismatch,
        "chunk_known_checks": chunk_known_checks,
        "chunk_known_mismatches": chunk_known_mismatches,
        "chunk_unknown_future_items": chunk_unknown_future_items,
        "chunk_cross_episode_detected": chunk_cross_episode_detected,
        "toy_detected": toy_detected,
        "toy_reasons": toy_reasons,
        "format_status": "FORMAT_PASS" if format_pass else "FORMAT_FAIL",
        "action_status": "ACTION_PASS" if action_pass else "ACTION_FAIL",
        "training_status": "TRAINING_READY" if training_ready else "NOT_TRAINING_READY",
    }


def write_report(result: dict[str, Any], notes: list[str], out: Path) -> None:
    action_values = result["action_values"]
    action_errors = result["action_errors"]
    lines = [
        "# JSONL Validation Report",
        "",
        "## Checked File",
        "",
    ]
    lines.extend(f"- {note}" for note in notes)
    lines.extend(
        [
            f"- Checked JSONL: `{result['path']}`",
            "",
            "## Summary",
            "",
            f"- Total samples: `{result['row_count']}`",
            f"- Parsed valid samples for episode/action checks: `{result['parsed_row_count']}`",
            f"- Episodes: `{result['episode_count']}`",
            f"- Image path exists: `{result['image_existing_count']}/{result['row_count']}` "
            f"({result['image_existing_rate'] * 100.0:.2f}%)",
            f"- Missing instruction count: `{result['instruction_missing']}`",
            f"- State format errors: `{result['state_format_errors']}`",
            f"- Action format errors: `{result['action_format_errors']}`",
            f"- Action chunk format errors: `{result['action_chunk_format_errors']}`",
            f"- Required field missing counts: `{result['required_missing']}`",
            f"- Other issue counts: `{result['issues']}`",
            "",
            "## Toy Data Check",
            "",
            f"- Toy data detected: `{result['toy_detected']}`",
        ]
    )
    if result["toy_reasons"]:
        lines.append(f"- Toy/reality check notes: `{result['toy_reasons']}`")
    else:
        lines.append("- Evidence: rows point to local `data/raw/TravelUAV`, raw source files or episode directories exist, and image files exist.")

    lines.extend(
        [
            "",
            "## Action Recompute Check",
            "",
            "Actions were recomputed from adjacent rows inside each `episode_id`, sorted by `step_id`:",
            "",
            "```text",
            "vx = (x_next - x) / dt",
            "vy = (y_next - y) / dt",
            "vz = (z_next - z) / dt",
            "yaw_rate = wrap_angle(yaw_next - yaw) / dt",
            "```",
            "",
            f"- Recomputed adjacent rows: `{result['action_recompute_rows']}`",
            f"- Rows failing tolerance `{ACTION_TOL}`: `{result['action_recompute_failures']}`",
            f"- Terminal/truncated rows without next state in this JSONL: `{result['uncheckable_terminal_rows']}`",
            "",
            "| Dimension | Error |",
            "| --- | --- |",
        ]
    )
    for name in ACTION_NAMES:
        lines.append(f"| {name} | {_fmt_error(action_errors[name])} |")

    lines.extend(
        [
            "",
            "## Action Numeric Range",
            "",
            "| Dimension | min/max/mean |",
            "| --- | --- |",
        ]
    )
    for name in ACTION_NAMES:
        lines.append(f"| {name} | {_fmt_stats(action_values[name])} |")

    lines.extend(
        [
            "",
            "Extreme action heuristic:",
            "",
            f"- Rows with any `|vx|`, `|vy|`, or `|vz|` > 20.0: `{result['linear_action_extreme_count']}`",
            f"- Rows with `|yaw_rate|` > pi: `{result['yaw_rate_extreme_count']}`",
            "",
            "## Zero-Vector Check",
            "",
            f"- All-zero state rows: `{result['state_zero_count']}`",
            f"- All-zero action rows: `{result['action_zero_count']}`",
            f"- All-zero action_chunk rows: `{result['chunk_zero_count']}`",
            "",
            "## Episode And Chunk Checks",
            "",
            f"- Step continuity gaps inside episode: `{result['continuity_gaps']}`",
            f"- Duplicate step ids inside episode: `{result['duplicate_steps']}`",
            f"- action_chunk first action mismatches current action: `{result['chunk_first_mismatch']}`",
            f"- action_chunk known same-episode comparisons: `{result['chunk_known_checks']}`",
            f"- action_chunk known same-episode mismatches: `{result['chunk_known_mismatches']}`",
            f"- action_chunk future items beyond this debug JSONL: `{result['chunk_unknown_future_items']}`",
            f"- Detected cross-episode action_chunk evidence: `{result['chunk_cross_episode_detected']}`",
            "",
            "Note: because debug JSONL files are truncated, some future `action_chunk` entries near the end of an episode cannot be fully verified from the JSONL alone. Available same-episode positions are checked exactly, and no cross-episode evidence is accepted as a pass condition.",
            "",
            "## Training Usability",
            "",
            "- Can be used as real data-path validation: `yes`, if `FORMAT_PASS` and `ACTION_PASS` are both reported.",
            "- Can be used directly for final OpenVLA-OFT migration training: `no`.",
            "- Reason: this is a small debug subset, not a full train/val split; full normalization, full dataset coverage, OpenVLA-OFT dataset adapter integration, model loading, and training must still be done later.",
            "",
            "## Final Status",
            "",
            f"- `{result['format_status']}`",
            f"- `{result['action_status']}`",
            f"- `{result['training_status']}`",
            "",
            "## Next Work",
            "",
            "- Keep this JSONL as a real TravelUAV data-path validation artifact.",
            "- Expand validation to the intended train/val split before training.",
            "- Recompute normalization statistics on the actual training split.",
            "- Implement the OpenVLA-OFT UAV dataset adapter/collator without loading weights first.",
            "- Move model loading, LoRA/OFT, action-head training, closed-loop evaluation, Diffusion Policy training, and RL expert generation to the 5090 stage.",
        ]
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", default=None, help="JSONL file to validate. If omitted, use priority candidates.")
    parser.add_argument("--image-root", default=".")
    parser.add_argument("--out", default="docs/jsonl_validation_report.md")
    args = parser.parse_args()

    notes: list[str]
    if args.jsonl:
        path = Path(args.jsonl)
        notes = [f"User-specified JSONL: `{path.as_posix()}`."]
        if not path.exists():
            raise SystemExit(f"FORMAT_FAIL: {path} does not exist")
    else:
        path, notes = _select_jsonl([Path(item) for item in DEFAULT_CANDIDATES])

    result = validate_jsonl(path, Path(args.image_root) if args.image_root else None)
    write_report(result, notes, Path(args.out))
    print(f"Checked: {result['path']}")
    print(f"Rows: {result['row_count']}")
    print(f"Episodes: {result['episode_count']}")
    print(f"Image exists rate: {result['image_existing_rate'] * 100.0:.2f}%")
    print(result["format_status"])
    print(result["action_status"])
    print(result["training_status"])
    print(f"Wrote report: {args.out}")
    if result["format_status"] != "FORMAT_PASS" or result["action_status"] != "ACTION_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
