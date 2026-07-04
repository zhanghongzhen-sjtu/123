"""UAV state/action adapter for TravelUAV-style trajectories.

State convention:
    state = [x, y, z, yaw]

Action convention:
    action = [vx, vy, vz, yaw_rate]
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

from src.openvla_uav_transfer.utils.geometry import maybe_deg_to_rad, safe_float, wrap_angle


POSITION_KEYS = ("position", "pos", "translation", "location")
ORIENTATION_KEYS = ("orientation", "rotation", "quat", "quaternion")
YAW_KEYS = ("yaw", "heading", "theta", "yaw_rad", "yaw_rate")


def _get_nested(mapping: Mapping[str, Any], path: Sequence[str]) -> Any:
    cur: Any = mapping
    for key in path:
        if not isinstance(cur, Mapping) or key not in cur:
            return None
        cur = cur[key]
    return cur


def _first(mapping: Mapping[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


def _component(obj: Any, names: Sequence[str]) -> float | None:
    if isinstance(obj, Mapping):
        for name in names:
            if name in obj:
                value = safe_float(obj[name])
                if value is not None:
                    return value
        for name in names:
            alt = f"{name}_val"
            if alt in obj:
                value = safe_float(obj[alt])
                if value is not None:
                    return value
    return None


def _position_to_xyz(position: Any) -> list[float] | None:
    if isinstance(position, Mapping):
        x = _component(position, ("x", "px", "east"))
        y = _component(position, ("y", "py", "north"))
        z = _component(position, ("z", "pz", "alt", "height"))
        if None not in (x, y, z):
            return [float(x), float(y), float(z)]
    elif isinstance(position, Sequence) and not isinstance(position, (str, bytes)):
        if len(position) >= 3:
            xyz = [safe_float(position[i]) for i in range(3)]
            if all(v is not None for v in xyz):
                return [float(v) for v in xyz]
    return None


def _quaternion_to_yaw(quat: Any) -> float | None:
    if isinstance(quat, Mapping):
        x = _component(quat, ("x",))
        y = _component(quat, ("y",))
        z = _component(quat, ("z",))
        w = _component(quat, ("w",))
    elif isinstance(quat, Sequence) and not isinstance(quat, (str, bytes)) and len(quat) >= 4:
        x, y, z, w = (safe_float(quat[i]) for i in range(4))
    else:
        return None
    if None in (x, y, z, w):
        return None
    siny_cosp = 2.0 * (float(w) * float(z) + float(x) * float(y))
    cosy_cosp = 1.0 - 2.0 * (float(y) * float(y) + float(z) * float(z))
    return math.atan2(siny_cosp, cosy_cosp)


def _orientation_to_yaw(orientation: Any) -> float | None:
    if isinstance(orientation, Mapping):
        direct_yaw = _first(orientation, YAW_KEYS)
        yaw = maybe_deg_to_rad(direct_yaw)
        if yaw is not None:
            return yaw
        return _quaternion_to_yaw(orientation)
    if isinstance(orientation, Sequence) and not isinstance(orientation, (str, bytes)):
        if len(orientation) == 4:
            return _quaternion_to_yaw(orientation)
        if len(orientation) >= 3:
            yaw = maybe_deg_to_rad(orientation[2])
            if yaw is not None:
                return yaw
    return None


def pose_to_state(pose: dict | Sequence[Any]) -> list[float]:
    """Convert a flexible pose/state record to [x, y, z, yaw]."""
    if isinstance(pose, Sequence) and not isinstance(pose, (str, bytes, Mapping)):
        if len(pose) >= 6:
            values = [safe_float(pose[0]), safe_float(pose[1]), safe_float(pose[2]), maybe_deg_to_rad(pose[5])]
        elif len(pose) >= 4:
            values = [safe_float(pose[0]), safe_float(pose[1]), safe_float(pose[2]), maybe_deg_to_rad(pose[3])]
        else:
            raise ValueError(f"Pose sequence must have at least 4 values, got {len(pose)}")
        if all(v is not None for v in values):
            return [float(v) for v in values]
        raise ValueError(f"Pose sequence contains non-numeric values: {pose!r}")

    if not isinstance(pose, Mapping):
        raise ValueError(f"Pose must be a dict or sequence, got {type(pose).__name__}")

    state = _get_nested(pose, ("sensors", "state"))
    if isinstance(state, Mapping):
        return pose_to_state(state)

    position = _first(pose, POSITION_KEYS)
    xyz = _position_to_xyz(position)
    if xyz is None:
        xyz = _position_to_xyz(pose)

    yaw = maybe_deg_to_rad(_first(pose, YAW_KEYS))
    if yaw is None:
        orientation = _first(pose, ORIENTATION_KEYS)
        yaw = _orientation_to_yaw(orientation)

    if xyz is None or yaw is None:
        raise ValueError(
            "Could not parse pose into [x, y, z, yaw]. "
            f"Available keys: {sorted(pose.keys())}; pose={pose!r}"
        )
    return [float(xyz[0]), float(xyz[1]), float(xyz[2]), float(yaw)]


def _validate_state(state: Sequence[Any], name: str) -> list[float]:
    if len(state) != 4:
        raise ValueError(f"{name} must be 4D [x, y, z, yaw], got {state!r}")
    values = [safe_float(v) for v in state]
    if any(v is None for v in values):
        raise ValueError(f"{name} contains non-finite values: {state!r}")
    return [float(v) for v in values]


def state_pair_to_action(state: Sequence[Any], next_state: Sequence[Any], dt: float) -> list[float]:
    """Compute [vx, vy, vz, yaw_rate] from adjacent states."""
    dt_value = safe_float(dt)
    if dt_value is None or dt_value <= 0:
        raise ValueError(f"dt must be a positive number, got {dt!r}")
    cur = _validate_state(state, "state")
    nxt = _validate_state(next_state, "next_state")
    return [
        (nxt[0] - cur[0]) / dt_value,
        (nxt[1] - cur[1]) / dt_value,
        (nxt[2] - cur[2]) / dt_value,
        wrap_angle(nxt[3] - cur[3]) / dt_value,
    ]


def trajectory_to_state_action_pairs(trajectory: Sequence[Any], dt: float | Sequence[Any] = 1.0) -> list[dict[str, Any]]:
    """Convert a trajectory into adjacent state/action training pairs."""
    states = [pose_to_state(item) for item in trajectory]
    pairs: list[dict[str, Any]] = []
    variable_dt = isinstance(dt, Sequence) and not isinstance(dt, (str, bytes))
    for idx in range(max(0, len(states) - 1)):
        dt_value = dt[idx] if variable_dt else dt
        pairs.append(
            {
                "step_id": idx,
                "state": states[idx],
                "next_state": states[idx + 1],
                "action": state_pair_to_action(states[idx], states[idx + 1], dt_value),
                "dt": safe_float(dt_value),
            }
        )
    return pairs


def build_action_chunk(actions: Sequence[Sequence[Any]], start_idx: int, chunk_size: int = 8) -> list[list[float]]:
    """Build a fixed-size future action chunk, padding with the final action if needed."""
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")
    if not actions:
        return []
    start = max(0, int(start_idx))
    validated = [_validate_state(action, "action") for action in actions]
    chunk = [validated[min(i, len(validated) - 1)] for i in range(start, start + chunk_size)]
    return chunk


def normalize_action(action: Sequence[Any], stats: dict[str, Any] | None = None) -> list[float]:
    """Normalize an action with optional mean/std or min/max stats."""
    values = _validate_state(action, "action")
    if not stats:
        return values
    if "mean" in stats and "std" in stats:
        mean = _validate_state(stats["mean"], "stats.mean")
        std = _validate_state(stats["std"], "stats.std")
        return [(v - m) / s if abs(s) > 1e-12 else 0.0 for v, m, s in zip(values, mean, std)]
    if "min" in stats and "max" in stats:
        lo = _validate_state(stats["min"], "stats.min")
        hi = _validate_state(stats["max"], "stats.max")
        return [2.0 * (v - a) / (b - a) - 1.0 if abs(b - a) > 1e-12 else 0.0 for v, a, b in zip(values, lo, hi)]
    raise ValueError("stats must contain either mean/std or min/max")


def denormalize_action(action: Sequence[Any], stats: dict[str, Any] | None = None) -> list[float]:
    """Reverse normalize_action with optional mean/std or min/max stats."""
    values = _validate_state(action, "action")
    if not stats:
        return values
    if "mean" in stats and "std" in stats:
        mean = _validate_state(stats["mean"], "stats.mean")
        std = _validate_state(stats["std"], "stats.std")
        return [v * s + m for v, m, s in zip(values, mean, std)]
    if "min" in stats and "max" in stats:
        lo = _validate_state(stats["min"], "stats.min")
        hi = _validate_state(stats["max"], "stats.max")
        return [0.5 * (v + 1.0) * (b - a) + a for v, a, b in zip(values, lo, hi)]
    raise ValueError("stats must contain either mean/std or min/max")
