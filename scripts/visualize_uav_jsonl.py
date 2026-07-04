#!/usr/bin/env python3
"""Visualize UAV JSONL x-y trajectories and action arrows as SVG images."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _vector(value: Any, size: int) -> list[float] | None:
    if not isinstance(value, list) or len(value) != size:
        return None
    if not all(_is_number(item) for item in value):
        return None
    return [float(item) for item in value]


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")[:120] or "episode"


def _load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_id, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                continue
            state = _vector(row.get("state"), 4)
            action = _vector(row.get("action"), 4)
            if state is None or action is None:
                continue
            episode_id = row.get("episode_id")
            step_id = row.get("step_id")
            if not isinstance(episode_id, str) or not isinstance(step_id, int):
                continue
            source = row.get("source") if isinstance(row.get("source"), dict) else {}
            rows.append(
                {
                    "episode_id": episode_id,
                    "step_id": step_id,
                    "state": state,
                    "action": action,
                    "map": str(source.get("map") or "unknown"),
                }
            )
    return rows


def _scale_points(points: list[tuple[float, float]], width: int, height: int, margin: int) -> tuple[list[tuple[float, float]], dict[str, float]]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = max(max_x - min_x, 1e-9)
    span_y = max(max_y - min_y, 1e-9)
    drawable_w = width - 2 * margin
    drawable_h = height - 2 * margin
    scale = min(drawable_w / span_x, drawable_h / span_y)
    used_w = span_x * scale
    used_h = span_y * scale
    offset_x = margin + (drawable_w - used_w) / 2
    offset_y = margin + (drawable_h - used_h) / 2
    scaled = []
    for x, y in points:
        sx = offset_x + (x - min_x) * scale
        sy = height - (offset_y + (y - min_y) * scale)
        scaled.append((sx, sy))
    meta = {
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
        "scale": scale,
        "offset_x": offset_x,
        "offset_y": offset_y,
    }
    return scaled, meta


def _arrow_svg(x1: float, y1: float, x2: float, y2: float, color: str) -> str:
    angle = math.atan2(y2 - y1, x2 - x1)
    head_len = 7.0
    head_ang = 0.55
    hx1 = x2 - head_len * math.cos(angle - head_ang)
    hy1 = y2 - head_len * math.sin(angle - head_ang)
    hx2 = x2 - head_len * math.cos(angle + head_ang)
    hy2 = y2 - head_len * math.sin(angle + head_ang)
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="1.4" stroke-linecap="round" />\n'
        f'<polyline points="{hx1:.2f},{hy1:.2f} {x2:.2f},{y2:.2f} {hx2:.2f},{hy2:.2f}" '
        f'fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" />'
    )


def _write_episode_svg(
    rows: list[dict[str, Any]],
    out_path: Path,
    width: int,
    height: int,
    arrow_stride: int,
    arrow_scale: float,
) -> None:
    rows = sorted(rows, key=lambda item: item["step_id"])
    points = [(row["state"][0], row["state"][1]) for row in rows]
    scaled, meta = _scale_points(points, width, height, margin=60)
    scale = meta["scale"]
    polyline = " ".join(f"{x:.2f},{y:.2f}" for x, y in scaled)
    map_name = rows[0]["map"]
    episode_id = rows[0]["episode_id"]
    title = f"{map_name} / {episode_id}"
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="24" y="30" font-family="Arial" font-size="16" fill="#111827">{title}</text>',
        f'<text x="24" y="52" font-family="Arial" font-size="12" fill="#4b5563">steps={len(rows)} '
        f'x=[{meta["min_x"]:.2f},{meta["max_x"]:.2f}] y=[{meta["min_y"]:.2f},{meta["max_y"]:.2f}]</text>',
        f'<polyline points="{polyline}" fill="none" stroke="#2563eb" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>',
    ]
    for idx, (row, (sx, sy)) in enumerate(zip(rows, scaled)):
        if idx % max(1, arrow_stride) != 0:
            continue
        vx, vy = row["action"][0], row["action"][1]
        ax = sx + vx * arrow_scale * scale
        ay = sy - vy * arrow_scale * scale
        svg_lines.append(_arrow_svg(sx, sy, ax, ay, "#dc2626"))
    start_x, start_y = scaled[0]
    end_x, end_y = scaled[-1]
    svg_lines.append(f'<circle cx="{start_x:.2f}" cy="{start_y:.2f}" r="4.5" fill="#16a34a"/>')
    svg_lines.append(f'<circle cx="{end_x:.2f}" cy="{end_y:.2f}" r="4.5" fill="#111827"/>')
    svg_lines.append('<text x="24" y="584" font-family="Arial" font-size="12" fill="#4b5563">blue: x-y trajectory, red: vx/vy action arrows, green: start, black: end</text>')
    svg_lines.append("</svg>")
    out_path.write_text("\n".join(svg_lines) + "\n", encoding="utf-8")


def visualize(jsonl: Path, out_dir: Path, max_episodes: int, arrow_stride: int, arrow_scale: float) -> list[Path]:
    rows = _load_rows(jsonl)
    by_episode: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_episode[row["episode_id"]].append(row)
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for episode_id, episode_rows in sorted(by_episode.items())[:max_episodes]:
        map_name = episode_rows[0]["map"]
        filename = f"{_safe_name(jsonl.stem)}__{_safe_name(map_name)}__{_safe_name(episode_id)}.svg"
        out_path = out_dir / filename
        _write_episode_svg(
            episode_rows,
            out_path,
            width=900,
            height=620,
            arrow_stride=arrow_stride,
            arrow_scale=arrow_scale,
        )
        outputs.append(out_path)
    index_lines = ["# UAV JSONL Trajectory Plots", "", f"Input: `{jsonl.as_posix()}`", ""]
    for path in outputs:
        index_lines.append(f"- `{path.as_posix()}`")
    (out_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", default="data/debug/traveluav_BrushifyCountryRoads_debug.jsonl")
    parser.add_argument("--out-dir", default="data/debug/plots")
    parser.add_argument("--max-episodes", type=int, default=6)
    parser.add_argument("--arrow-stride", type=int, default=2)
    parser.add_argument("--arrow-scale", type=float, default=5.0)
    args = parser.parse_args()
    outputs = visualize(
        jsonl=Path(args.jsonl),
        out_dir=Path(args.out_dir),
        max_episodes=args.max_episodes,
        arrow_stride=args.arrow_stride,
        arrow_scale=args.arrow_scale,
    )
    print(f"Wrote {len(outputs)} plot(s) to {args.out_dir}")
    for path in outputs:
        print(path.as_posix())


if __name__ == "__main__":
    main()
