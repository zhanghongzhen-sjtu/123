"""CPU-only UAV JSONL dataset loader.

This module intentionally avoids torch, transformers, model weights, simulators,
and image decoding. It only validates and packages JSONL rows for later
OpenVLA-OFT dataset integration work.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


STATE_SIZE = 4
ACTION_SIZE = 4
STATE_NAMES = ("x", "y", "z", "yaw")
ACTION_NAMES = ("vx", "vy", "vz", "yaw_rate")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _validate_vector(value: Any, size: int, field_name: str, row_ref: str) -> list[float]:
    if not isinstance(value, list) or len(value) != size:
        raise ValueError(f"{row_ref}: `{field_name}` must be a {size}D list")
    if not all(_is_number(item) for item in value):
        raise ValueError(f"{row_ref}: `{field_name}` contains non-numeric or non-finite values")
    return [float(item) for item in value]


def _validate_action_chunk(value: Any, row_ref: str) -> list[list[float]]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{row_ref}: `action_chunk` must be a non-empty list")
    return [_validate_vector(item, ACTION_SIZE, f"action_chunk[{idx}]", row_ref) for idx, item in enumerate(value)]


def _as_paths(paths: str | Path | Iterable[str | Path]) -> list[Path]:
    if isinstance(paths, (str, Path)):
        return [Path(paths)]
    return [Path(path) for path in paths]


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected top-level JSON object")
    return data


def _normalization_from_stats(stats_path: Path | None) -> dict[str, dict[str, list[float]]]:
    if stats_path is None:
        return {}
    stats = _load_json(stats_path)
    normalization: dict[str, dict[str, list[float]]] = {}
    for key, size in (("state", STATE_SIZE), ("action", ACTION_SIZE)):
        section = stats.get(key)
        if not isinstance(section, dict):
            raise ValueError(f"{stats_path}: missing `{key}` section")
        norm = section.get("normalization")
        if not isinstance(norm, dict):
            raise ValueError(f"{stats_path}: missing `{key}.normalization` section")
        normalization[key] = {
            "mean": _validate_vector(norm.get("mean"), size, f"{key}.normalization.mean", str(stats_path)),
            "std": _validate_vector(norm.get("std"), size, f"{key}.normalization.std", str(stats_path)),
            "min": _validate_vector(norm.get("min"), size, f"{key}.normalization.min", str(stats_path)),
            "max": _validate_vector(norm.get("max"), size, f"{key}.normalization.max", str(stats_path)),
        }
    return normalization


def _normalize(values: list[float], mean: list[float], std: list[float]) -> list[float]:
    return [(value - avg) / scale if abs(scale) > 1e-12 else 0.0 for value, avg, scale in zip(values, mean, std)]


class UavJsonlDataset:
    """Validated in-memory view of UAV OpenVLA-style JSONL rows.

    The returned samples are plain Python dictionaries. This keeps the loader
    useful for CPU-only smoke tests before any torch/OpenVLA-OFT integration.
    """

    def __init__(
        self,
        jsonl_paths: str | Path | Iterable[str | Path],
        image_root: str | Path | None = None,
        stats_path: str | Path | None = None,
        require_image_exists: bool = False,
        normalize: bool = False,
        max_rows: int | None = None,
    ) -> None:
        self.jsonl_paths = _as_paths(jsonl_paths)
        self.image_root = Path(image_root) if image_root is not None else None
        self.stats_path = Path(stats_path) if stats_path is not None else None
        self.require_image_exists = require_image_exists
        self.normalize = normalize
        self.normalization = _normalization_from_stats(self.stats_path)
        if normalize and not self.normalization:
            raise ValueError("normalize=True requires a stats_path")

        self.rows: list[dict[str, Any]] = []
        self._load(max_rows=max_rows)
        if not self.rows:
            raise ValueError("No rows loaded from JSONL input")

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict[str, Any]:
        return self.rows[index]

    def _load(self, max_rows: int | None) -> None:
        for jsonl_path in self.jsonl_paths:
            if not jsonl_path.exists():
                raise ValueError(f"{jsonl_path} does not exist")
            with jsonl_path.open("r", encoding="utf-8") as f:
                for line_id, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    row_ref = f"{jsonl_path}:{line_id}"
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise ValueError(f"{row_ref}: invalid JSON: {exc}") from exc
                    if not isinstance(row, dict):
                        raise ValueError(f"{row_ref}: row must be a JSON object")
                    self.rows.append(self._build_sample(row, jsonl_path, line_id))
                    if max_rows is not None and len(self.rows) >= max_rows:
                        return

    def _build_sample(self, row: dict[str, Any], jsonl_path: Path, line_id: int) -> dict[str, Any]:
        row_ref = f"{jsonl_path}:{line_id}"
        dataset = row.get("dataset")
        if dataset != "TravelUAV":
            raise ValueError(f"{row_ref}: `dataset` must be `TravelUAV`")

        episode_id = row.get("episode_id")
        if not isinstance(episode_id, str) or not episode_id:
            raise ValueError(f"{row_ref}: `episode_id` must be a non-empty string")

        step_id = row.get("step_id")
        if not isinstance(step_id, int) or isinstance(step_id, bool) or step_id < 0:
            raise ValueError(f"{row_ref}: `step_id` must be a non-negative integer")

        image = row.get("image")
        if not isinstance(image, str) or not image:
            raise ValueError(f"{row_ref}: `image` must be a non-empty string")
        image_path = self.resolve_image_path(image)
        if self.require_image_exists and not image_path.exists():
            raise ValueError(f"{row_ref}: image path does not exist: {image_path}")

        instruction = row.get("instruction")
        if not isinstance(instruction, str) or not instruction.strip():
            raise ValueError(f"{row_ref}: `instruction` must be a non-empty string")

        state = _validate_vector(row.get("state"), STATE_SIZE, "state", row_ref)
        action = _validate_vector(row.get("action"), ACTION_SIZE, "action", row_ref)
        action_chunk = _validate_action_chunk(row.get("action_chunk"), row_ref)

        dt = row.get("dt")
        if not _is_number(dt) or float(dt) <= 0:
            raise ValueError(f"{row_ref}: `dt` must be a positive finite number")

        source = row.get("source") if isinstance(row.get("source"), dict) else {}
        sample: dict[str, Any] = {
            "dataset": dataset,
            "episode_id": episode_id,
            "step_id": step_id,
            "image": image,
            "image_path": image_path.as_posix(),
            "instruction": instruction,
            "state": state,
            "action": action,
            "action_chunk": action_chunk,
            "dt": float(dt),
            "source": source,
            "jsonl_path": jsonl_path.as_posix(),
            "line_id": line_id,
        }

        if self.normalize:
            sample["state_normalized"] = _normalize(
                state,
                self.normalization["state"]["mean"],
                self.normalization["state"]["std"],
            )
            sample["action_normalized"] = _normalize(
                action,
                self.normalization["action"]["mean"],
                self.normalization["action"]["std"],
            )
            sample["action_chunk_normalized"] = [
                _normalize(
                    chunk_action,
                    self.normalization["action"]["mean"],
                    self.normalization["action"]["std"],
                )
                for chunk_action in action_chunk
            ]

        return sample

    def resolve_image_path(self, image: str) -> Path:
        image_path = Path(image)
        if image_path.is_absolute():
            return image_path
        if self.image_root is not None:
            return self.image_root / image_path
        return image_path

    def summary(self) -> dict[str, Any]:
        maps: dict[str, list[dict[str, Any]]] = defaultdict(list)
        episodes_by_map: dict[str, set[str]] = defaultdict(set)
        chunk_lengths: Counter[int] = Counter()
        dt_sources: Counter[str] = Counter()
        for row in self.rows:
            source = row.get("source") if isinstance(row.get("source"), dict) else {}
            map_name = str(source.get("map") or "unknown")
            maps[map_name].append(row)
            episodes_by_map[map_name].add(row["episode_id"])
            chunk_lengths[len(row["action_chunk"])] += 1
            dt_sources[str(source.get("dt_source") or "unknown")] += 1
        return {
            "rows": len(self.rows),
            "maps": {
                map_name: {
                    "rows": len(rows),
                    "episodes": len(episodes_by_map[map_name]),
                }
                for map_name, rows in sorted(maps.items())
            },
            "action_chunk_lengths": dict(sorted(chunk_lengths.items())),
            "dt_sources": dict(sorted(dt_sources.items())),
            "normalized": self.normalize,
            "stats_path": self.stats_path.as_posix() if self.stats_path else None,
        }
