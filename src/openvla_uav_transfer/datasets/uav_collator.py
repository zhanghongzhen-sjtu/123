"""CPU-only OpenVLA-OFT-style UAV batch collator.

The collator returns plain Python lists and metadata. It is a shape/interface
prototype for later OpenVLA-OFT integration, not a training dataloader.
"""

from __future__ import annotations

import math
from typing import Any


STATE_DIM = 4
ACTION_DIM = 4
SCHEMA_VERSION = "uav_openvla_jsonl_v0.1"


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _check_vector(value: Any, size: int, name: str) -> list[float]:
    if not isinstance(value, list) or len(value) != size:
        raise ValueError(f"{name} must be a {size}D list")
    if not all(_is_number(item) for item in value):
        raise ValueError(f"{name} contains non-numeric or non-finite values")
    return [float(item) for item in value]


def _check_action_chunk(value: Any, expected_chunk_size: int | None, name: str) -> list[list[float]]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{name} must be a non-empty list")
    if expected_chunk_size is not None and len(value) != expected_chunk_size:
        raise ValueError(f"{name} must have chunk size {expected_chunk_size}, got {len(value)}")
    return [_check_vector(action, ACTION_DIM, f"{name}[{idx}]") for idx, action in enumerate(value)]


def _shape_2d(values: list[list[float]]) -> list[int]:
    width = len(values[0]) if values else 0
    return [len(values), width]


def _shape_3d(values: list[list[list[float]]]) -> list[int]:
    depth = len(values[0]) if values else 0
    width = len(values[0][0]) if values and values[0] else 0
    return [len(values), depth, width]


class OpenVLAOFTUavCollator:
    """Prepare a CPU-only batch matching the future UAV OpenVLA-OFT interface."""

    def __init__(
        self,
        expected_action_chunk_size: int | None = 8,
        require_normalized: bool = False,
    ) -> None:
        self.expected_action_chunk_size = expected_action_chunk_size
        self.require_normalized = require_normalized

    def __call__(self, samples: list[dict[str, Any]]) -> dict[str, Any]:
        if not samples:
            raise ValueError("Cannot collate an empty sample list")

        image_paths: list[str] = []
        instructions: list[str] = []
        states: list[list[float]] = []
        actions: list[list[float]] = []
        action_chunks: list[list[list[float]]] = []
        dts: list[float] = []
        episode_ids: list[str] = []
        step_ids: list[int] = []
        sources: list[dict[str, Any]] = []
        jsonl_refs: list[dict[str, Any]] = []
        states_normalized: list[list[float]] = []
        actions_normalized: list[list[float]] = []
        action_chunks_normalized: list[list[list[float]]] = []

        for sample_id, sample in enumerate(samples):
            image_path = sample.get("image_path")
            if not isinstance(image_path, str) or not image_path:
                raise ValueError(f"sample {sample_id}: missing image_path")
            instruction = sample.get("instruction")
            if not isinstance(instruction, str) or not instruction.strip():
                raise ValueError(f"sample {sample_id}: missing instruction")
            episode_id = sample.get("episode_id")
            if not isinstance(episode_id, str) or not episode_id:
                raise ValueError(f"sample {sample_id}: missing episode_id")
            step_id = sample.get("step_id")
            if not isinstance(step_id, int) or isinstance(step_id, bool) or step_id < 0:
                raise ValueError(f"sample {sample_id}: bad step_id")
            dt = sample.get("dt")
            if not _is_number(dt) or float(dt) <= 0:
                raise ValueError(f"sample {sample_id}: dt must be positive")

            state = _check_vector(sample.get("state"), STATE_DIM, f"sample {sample_id} state")
            action = _check_vector(sample.get("action"), ACTION_DIM, f"sample {sample_id} action")
            action_chunk = _check_action_chunk(
                sample.get("action_chunk"),
                self.expected_action_chunk_size,
                f"sample {sample_id} action_chunk",
            )

            image_paths.append(image_path)
            instructions.append(instruction)
            states.append(state)
            actions.append(action)
            action_chunks.append(action_chunk)
            dts.append(float(dt))
            episode_ids.append(episode_id)
            step_ids.append(step_id)
            source = sample.get("source")
            sources.append(source if isinstance(source, dict) else {})
            jsonl_refs.append({"jsonl_path": sample.get("jsonl_path"), "line_id": sample.get("line_id")})

            if self.require_normalized or "state_normalized" in sample:
                states_normalized.append(_check_vector(sample.get("state_normalized"), STATE_DIM, f"sample {sample_id} state_normalized"))
                actions_normalized.append(_check_vector(sample.get("action_normalized"), ACTION_DIM, f"sample {sample_id} action_normalized"))
                action_chunks_normalized.append(
                    _check_action_chunk(
                        sample.get("action_chunk_normalized"),
                        self.expected_action_chunk_size,
                        f"sample {sample_id} action_chunk_normalized",
                    )
                )

        batch: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "task": "traveluav_uav_vln_openvla_oft_debug",
            "batch_size": len(samples),
            "image_paths": image_paths,
            "instructions": instructions,
            "states": states,
            "actions": actions,
            "action_chunks": action_chunks,
            "dts": dts,
            "episode_ids": episode_ids,
            "step_ids": step_ids,
            "sources": sources,
            "jsonl_refs": jsonl_refs,
            "shapes": {
                "states": _shape_2d(states),
                "actions": _shape_2d(actions),
                "action_chunks": _shape_3d(action_chunks),
                "dts": [len(dts)],
            },
            "openvla_oft_mapping": {
                "vision": "image_paths",
                "language": "instructions",
                "proprio": "states",
                "action_target": "action_chunks",
                "single_step_action": "actions",
                "metadata": "sources",
            },
        }

        if states_normalized:
            batch["states_normalized"] = states_normalized
            batch["actions_normalized"] = actions_normalized
            batch["action_chunks_normalized"] = action_chunks_normalized
            batch["shapes"]["states_normalized"] = _shape_2d(states_normalized)
            batch["shapes"]["actions_normalized"] = _shape_2d(actions_normalized)
            batch["shapes"]["action_chunks_normalized"] = _shape_3d(action_chunks_normalized)

        return batch
