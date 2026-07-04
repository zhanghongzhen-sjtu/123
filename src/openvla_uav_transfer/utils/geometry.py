"""Geometry helpers used by the lightweight UAV data pipeline."""

from __future__ import annotations

import math
from typing import Any


def safe_float(value: Any, default: float | None = None) -> float | None:
    """Convert a value to a finite float, returning default on failure."""
    if value is None or isinstance(value, bool):
        return default
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(result):
        return default
    return result


def wrap_angle(angle: float) -> float:
    """Wrap an angle in radians to [-pi, pi]."""
    value = safe_float(angle)
    if value is None:
        raise ValueError(f"Cannot wrap non-numeric angle: {angle!r}")
    return (value + math.pi) % (2.0 * math.pi) - math.pi


def maybe_deg_to_rad(yaw: Any, assume_degrees: bool = False) -> float | None:
    """Convert yaw to radians when requested or when the magnitude looks degree-like."""
    value = safe_float(yaw)
    if value is None:
        return None
    if assume_degrees or abs(value) > (2.0 * math.pi + 1e-6):
        return math.radians(value)
    return value
