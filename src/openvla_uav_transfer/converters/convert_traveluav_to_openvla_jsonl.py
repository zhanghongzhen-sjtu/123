"""Convert a small TravelUAV sample to OpenVLA-OFT-style JSONL.

This script is intentionally lightweight: it does not load images, models, simulators,
or any training dependencies.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.openvla_uav_transfer.adapters.uav_action_adapter import (
    build_action_chunk,
    trajectory_to_state_action_pairs,
)
from src.openvla_uav_transfer.utils.geometry import safe_float


CAMERA_DIR = "frontcamera"


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _clean_instruction(value: Any) -> str:
    if isinstance(value, str):
        text = value
    elif isinstance(value, list) and value and isinstance(value[0], dict):
        text = str(value[0].get("value", ""))
    else:
        text = ""
    return text.replace("<image>", "").strip()


def _extract_instruction(data: dict[str, Any], warnings: list[str], raw_file: Path) -> str:
    if isinstance(data.get("instruction"), str):
        return _clean_instruction(data["instruction"])
    conversations = data.get("conversations")
    if isinstance(conversations, list):
        for msg in conversations:
            if isinstance(msg, dict) and msg.get("from") in {"human", "user"}:
                text = _clean_instruction(msg.get("value", ""))
                if text:
                    return text
    warnings.append(f"{raw_file}: missing instruction; using empty string")
    return ""


def _extract_trajectory(data: dict[str, Any]) -> list[Any]:
    for key in ("trajectory_raw_detailed", "trajectory_raw", "trajectory", "poses", "states"):
        value = data.get(key)
        if isinstance(value, list) and len(value) >= 2:
            return value
    return []


def _episode_id(raw_file: Path) -> str:
    if raw_file.parent.name:
        return raw_file.parent.name
    return raw_file.stem


def _map_name(raw_file: Path) -> str | None:
    try:
        return raw_file.parents[1].name
    except IndexError:
        return None


def _map_name_from_episode_dir(episode_dir: Path) -> str | None:
    try:
        return episode_dir.parent.name
    except IndexError:
        return None


def _image_path(raw_file: Path, data: dict[str, Any], step_id: int) -> str:
    indices = data.get("index")
    frame = None
    if isinstance(indices, list) and step_id < len(indices):
        frame = indices[step_id]
    if frame is None:
        frame = step_id
    try:
        frame_int = int(frame)
        filename = f"{frame_int:06d}.png"
    except (TypeError, ValueError):
        filename = f"{frame}.png"
    return (raw_file.parent / CAMERA_DIR / filename).as_posix()


def _image_path_from_log_path(log_path: Path) -> str:
    return (log_path.parent.parent / CAMERA_DIR / f"{log_path.stem}.png").as_posix()


def _timestamp_value(log_data: dict[str, Any]) -> float | None:
    if not isinstance(log_data, dict):
        return None
    state = log_data.get("sensors", {}).get("state")
    if isinstance(state, dict):
        value = safe_float(state.get("timestamp"))
        if value is not None:
            return value
    return safe_float(log_data.get("timestamp"))


def _timestamp_delta_seconds(current_ts: float | None, next_ts: float | None) -> float | None:
    if current_ts is None or next_ts is None:
        return None
    delta = next_ts - current_ts
    if delta <= 0:
        return None
    if delta > 1e8:
        return delta / 1e9
    if delta > 1e5:
        return delta / 1e6
    if delta > 100:
        return delta / 1e3
    return delta


def _compute_raw_dts(
    log_records: list[dict[str, Any]],
    default_dt: float,
    warnings: list[str],
    episode_dir: Path,
) -> tuple[list[float], list[str]]:
    dts: list[float] = []
    sources: list[str] = []
    for idx in range(max(0, len(log_records) - 1)):
        current_ts = _timestamp_value(log_records[idx])
        next_ts = _timestamp_value(log_records[idx + 1])
        dt_seconds = _timestamp_delta_seconds(current_ts, next_ts)
        if dt_seconds is None:
            dts.append(default_dt)
            sources.append("fallback_arg")
            warnings.append(f"{episode_dir}: missing/non-positive timestamp delta at local step {idx}; using dt={default_dt}")
        else:
            dts.append(dt_seconds)
            sources.append("timestamp")
    return dts, sources


def _convert_episode(
    raw_file: Path,
    dt: float,
    action_chunk_size: int,
    max_steps_per_episode: int,
    warnings: list[str],
) -> list[dict[str, Any]]:
    data = _read_json(raw_file)
    if not isinstance(data, dict):
        warnings.append(f"{raw_file}: top-level JSON is not an object")
        return []
    instruction = _extract_instruction(data, warnings, raw_file)
    trajectory = _extract_trajectory(data)
    if len(trajectory) < 2:
        warnings.append(f"{raw_file}: missing usable trajectory with at least 2 poses")
        return []
    try:
        pairs = trajectory_to_state_action_pairs(trajectory, dt=dt)
    except Exception as exc:
        warnings.append(f"{raw_file}: failed to parse trajectory: {exc}")
        return []
    actions = [pair["action"] for pair in pairs]
    rows: list[dict[str, Any]] = []
    for pair in pairs[:max_steps_per_episode]:
        step_id = int(pair["step_id"])
        image = _image_path(raw_file, data, step_id)
        if not image:
            warnings.append(f"{raw_file}: step {step_id} missing image path")
        if not instruction:
            warnings.append(f"{raw_file}: step {step_id} missing instruction")
        rows.append(
            {
                "dataset": "TravelUAV",
                "episode_id": _episode_id(raw_file),
                "step_id": step_id,
                "image": image,
                "instruction": instruction,
                "state": pair["state"],
                "action": pair["action"],
                "action_chunk": build_action_chunk(actions, step_id, chunk_size=action_chunk_size),
                "dt": pair.get("dt", dt),
                "source": {
                    "raw_file": raw_file.as_posix(),
                    "map": _map_name(raw_file),
                    "target": data.get("target") or data.get("object_name"),
                },
            }
        )
    return rows


def _load_raw_instruction(episode_dir: Path, warnings: list[str]) -> str:
    object_desc_path = episode_dir / "object_description.json"
    mark_path = episode_dir / "mark.json"
    desc = ""
    target_name = ""
    if object_desc_path.exists():
        try:
            obj = _read_json(object_desc_path)
            if isinstance(obj, list) and obj:
                desc = str(obj[0]).strip()
            elif isinstance(obj, str):
                desc = obj.strip()
        except Exception as exc:
            warnings.append(f"{episode_dir}: failed to read object_description.json: {exc}")
    if mark_path.exists():
        try:
            mark = _read_json(mark_path)
            if isinstance(mark, dict):
                target_name = str(mark.get("object_name") or "").strip()
        except Exception as exc:
            warnings.append(f"{episode_dir}: failed to read mark.json: {exc}")
    if desc:
        prefix = f"Find the target object {target_name}. " if target_name else "Find the target object. "
        return prefix + desc + " Please control the drone and find the target."
    warnings.append(f"{episode_dir}: missing instruction text; using generic raw-data instruction")
    return "Please control the drone and find the target."


def _load_raw_target(episode_dir: Path) -> Any:
    mark_path = episode_dir / "mark.json"
    if not mark_path.exists():
        return None
    try:
        mark = _read_json(mark_path)
    except Exception:
        return None
    if not isinstance(mark, dict):
        return None
    return {
        "object_name": mark.get("object_name"),
        "target": mark.get("target"),
        "end": mark.get("end"),
    }


def _convert_raw_episode(
    episode_dir: Path,
    dt: float,
    action_chunk_size: int,
    max_steps_per_episode: int,
    warnings: list[str],
) -> list[dict[str, Any]]:
    log_dir = episode_dir / "log"
    if not log_dir.is_dir():
        return []
    log_paths = sorted(log_dir.glob("*.json"), key=lambda p: int(p.stem) if p.stem.isdigit() else p.stem)
    usable_log_paths: list[Path] = []
    log_records: list[dict[str, Any]] = []
    trajectory: list[Any] = []
    for log_path in log_paths:
        image_path = Path(_image_path_from_log_path(log_path))
        if not image_path.exists():
            continue
        try:
            data = _read_json(log_path)
        except Exception as exc:
            warnings.append(f"{log_path}: failed to read raw log: {exc}")
            continue
        state = data.get("sensors", {}).get("state") if isinstance(data, dict) else None
        if isinstance(state, dict):
            usable_log_paths.append(log_path)
            log_records.append(data)
            trajectory.append(state)
        if len(trajectory) >= max_steps_per_episode + 1:
            break
    if len(trajectory) < 2:
        warnings.append(f"{episode_dir}: less than 2 image-aligned raw states found")
        return []
    dts, dt_sources = _compute_raw_dts(log_records, default_dt=dt, warnings=warnings, episode_dir=episode_dir)
    try:
        pairs = trajectory_to_state_action_pairs(trajectory, dt=dts)
    except Exception as exc:
        warnings.append(f"{episode_dir}: failed to convert raw trajectory: {exc}")
        return []
    instruction = _load_raw_instruction(episode_dir, warnings)
    actions = [pair["action"] for pair in pairs]
    target = _load_raw_target(episode_dir)
    rows: list[dict[str, Any]] = []
    for local_idx, pair in enumerate(pairs[:max_steps_per_episode]):
        log_path = usable_log_paths[local_idx]
        next_log_path = usable_log_paths[min(local_idx + 1, len(usable_log_paths) - 1)]
        log_record = log_records[local_idx]
        next_log_record = log_records[min(local_idx + 1, len(log_records) - 1)]
        state_record = log_record.get("sensors", {}).get("state") if isinstance(log_record, dict) else {}
        frame_id = int(log_path.stem) if log_path.stem.isdigit() else local_idx
        next_frame_id = int(next_log_path.stem) if next_log_path.stem.isdigit() else local_idx + 1
        rows.append(
            {
                "dataset": "TravelUAV",
                "episode_id": episode_dir.name,
                "step_id": local_idx,
                "image": _image_path_from_log_path(log_path),
                "instruction": instruction,
                "state": pair["state"],
                "action": pair["action"],
                "action_chunk": build_action_chunk(actions, local_idx, chunk_size=action_chunk_size),
                "dt": pair.get("dt", dts[local_idx]),
                "source": {
                    "raw_file": log_path.as_posix(),
                    "next_raw_file": next_log_path.as_posix(),
                    "raw_episode_dir": episode_dir.as_posix(),
                    "map": _map_name_from_episode_dir(episode_dir),
                    "frame": frame_id,
                    "next_frame": next_frame_id,
                    "timestamp": _timestamp_value(log_record),
                    "next_timestamp": _timestamp_value(next_log_record),
                    "dt_source": dt_sources[local_idx],
                    "raw_linear_velocity": state_record.get("linear_velocity") if isinstance(state_record, dict) else None,
                    "raw_angular_velocity": state_record.get("angular_velocity") if isinstance(state_record, dict) else None,
                    "target": target,
                },
            }
        )
    return rows


def _find_merged_files(dataset_root: Path, traveluav_root: Path, max_episodes: int) -> list[Path]:
    roots = []
    if dataset_root.exists():
        roots.append(dataset_root)
    repo_dataset = traveluav_root / "dataset_raw"
    if repo_dataset.exists() and repo_dataset not in roots:
        roots.append(repo_dataset)
    files: list[Path] = []
    for root in roots:
        for path in root.rglob("merged_data.json"):
            files.append(path)
            if len(files) >= max_episodes:
                break
        if len(files) >= max_episodes:
            break
    return files[:max_episodes]


def _find_raw_episode_dirs(dataset_root: Path, max_episodes: int) -> list[Path]:
    if not dataset_root.exists():
        return []
    episodes: list[Path] = []
    for child in sorted(dataset_root.iterdir()):
        if child.is_dir() and (child / "log").is_dir() and (child / CAMERA_DIR).is_dir():
            episodes.append(child)
            if len(episodes) >= max_episodes:
                break
    return episodes


def _toy_rows(dt: float, action_chunk_size: int) -> list[dict[str, Any]]:
    trajectory = [
        {"position": [0.0, 0.0, -2.0], "orientation": [0.0, 0.0, 0.0, 1.0]},
        {"position": [1.0, 0.0, -2.1], "orientation": [0.0, 0.0, 0.05, 0.9987492178]},
        {"position": [2.0, 0.2, -2.2], "orientation": [0.0, 0.0, 0.0998334166, 0.9950041653]},
        {"position": [3.0, 0.5, -2.2], "orientation": [0.0, 0.0, 0.1494381325, 0.9887710779]},
    ]
    pairs = trajectory_to_state_action_pairs(trajectory, dt=dt)
    actions = [pair["action"] for pair in pairs]
    rows = []
    for pair in pairs:
        step_id = int(pair["step_id"])
        rows.append(
            {
                "dataset": "TravelUAV",
                "episode_id": "toy_debug_episode_000",
                "step_id": step_id,
                "image": f"toy/frontcamera/{step_id:06d}.png",
                "instruction": "Fly forward and find the target building.",
                "state": pair["state"],
                "action": pair["action"],
                "action_chunk": build_action_chunk(actions, step_id, chunk_size=action_chunk_size),
                "dt": dt,
                "source": {
                    "raw_file": "toy_debug_generated",
                    "map": "toy_map",
                    "target": "toy_target",
                },
            }
        )
    return rows


def _write_jsonl(rows: list[dict[str, Any]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _write_toy_readme(out: Path) -> None:
    readme = out.parent / "README.md"
    readme.write_text(
        "# Debug Data\n\n"
        "这是 toy debug 数据，仅用于测试 JSONL 格式，不可作为论文实验数据。\n\n"
        "当真实 TravelUAV `dataset_raw` 下载完成后，请放到 `data/raw/TravelUAV` "
        "或 `external/TravelUAV/dataset_raw`，再重新运行转换脚本。\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traveluav-root", default="external/TravelUAV")
    parser.add_argument("--dataset-root", default="data/raw/TravelUAV")
    parser.add_argument("--out", default="data/debug/traveluav_debug.jsonl")
    parser.add_argument("--max-episodes", type=int, default=3)
    parser.add_argument("--max-steps-per-episode", type=int, default=20)
    parser.add_argument("--dt", type=float, default=1.0)
    parser.add_argument("--action-chunk-size", type=int, default=8)
    args = parser.parse_args()

    traveluav_root = Path(args.traveluav_root)
    dataset_root = Path(args.dataset_root)
    out = Path(args.out)
    warnings: list[str] = []

    rows: list[dict[str, Any]] = []
    merged_files = _find_merged_files(dataset_root, traveluav_root, args.max_episodes)
    for raw_file in merged_files:
        rows.extend(
            _convert_episode(
                raw_file=raw_file,
                dt=args.dt,
                action_chunk_size=args.action_chunk_size,
                max_steps_per_episode=args.max_steps_per_episode,
                warnings=warnings,
            )
        )

    if not rows:
        raw_episode_dirs = _find_raw_episode_dirs(dataset_root, args.max_episodes)
        for episode_dir in raw_episode_dirs:
            rows.extend(
                _convert_raw_episode(
                    episode_dir=episode_dir,
                    dt=args.dt,
                    action_chunk_size=args.action_chunk_size,
                    max_steps_per_episode=args.max_steps_per_episode,
                    warnings=warnings,
                )
            )

    used_toy = False
    if not rows:
        used_toy = True
        warnings.append("No usable TravelUAV dataset_raw/merged_data.json found; generated toy debug JSONL.")
        rows = _toy_rows(dt=args.dt, action_chunk_size=args.action_chunk_size)
        _write_toy_readme(out)

    _write_jsonl(rows, out)
    for warning in warnings:
        print(f"WARNING: {warning}")
    print(f"Wrote {len(rows)} rows to {out}")
    print(f"USED_TOY_DATA={str(used_toy).lower()}")


if __name__ == "__main__":
    main()
