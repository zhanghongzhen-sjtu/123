"""Inspect TravelUAV repository/data structure without loading models or large datasets."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TEXT_EXTS = {".md", ".txt", ".json", ".jsonl", ".csv", ".py", ".sh", ".yaml", ".yml"}
DATA_EXTS = {".json", ".jsonl", ".csv", ".txt"}
KEYWORDS = {
    "instruction": ("instruction", "conversations", "prompt", "task", "description"),
    "image": ("image", "rgb", "camera", "frontcamera", "png", "jpg", "feature"),
    "trajectory": ("trajectory", "traj", "waypoint", "position", "pose"),
    "yaw": ("yaw", "orientation", "rotation", "quaternion"),
    "action": ("action", "teacher_action", "waypoint", "velocity"),
}


def _safe_read(path: Path, max_bytes: int = 8192) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
    except OSError:
        return ""
    return data.decode("utf-8", errors="replace")


def _is_lfs_pointer(text: str) -> bool:
    return text.startswith("version https://git-lfs.github.com/spec/v1")


def _walk_limited(root: Path, max_files: int = 200) -> list[Path]:
    if not root.exists():
        return []
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_EXTS:
            files.append(path)
            if len(files) >= max_files:
                break
    return files


def _tree(root: Path, max_depth: int = 3, max_items: int = 180) -> list[str]:
    lines: list[str] = []
    if not root.exists():
        return ["(missing)"]
    base_parts = len(root.parts)
    for path in sorted(root.rglob("*")):
        depth = len(path.parts) - base_parts
        if depth > max_depth:
            continue
        rel = path.relative_to(root)
        suffix = "/" if path.is_dir() else ""
        lines.append(f"- {rel.as_posix()}{suffix}")
        if len(lines) >= max_items:
            lines.append(f"- ... truncated after {max_items} items")
            break
    return lines


def _collect_json_keys(obj: Any, prefix: str = "", out: Counter[str] | None = None) -> Counter[str]:
    if out is None:
        out = Counter()
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            out[path] += 1
            _collect_json_keys(value, path, out)
    elif isinstance(obj, list):
        for item in obj[:5]:
            _collect_json_keys(item, f"{prefix}[]", out)
    return out


def _load_json_sample(path: Path) -> Any | None:
    if path.stat().st_size > 2_000_000:
        return None
    text = _safe_read(path, max_bytes=2_000_000)
    if _is_lfs_pointer(text):
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def inspect(traveluav_root: Path, dataset_root: Path | None, out_path: Path) -> None:
    candidate_roots = [
        traveluav_root / "README.md",
        traveluav_root / "data",
        traveluav_root / "scripts",
        traveluav_root / "src",
        traveluav_root / "tools",
        traveluav_root / "Model" / "LLaMA-UAV" / "tools",
    ]
    if dataset_root is not None:
        candidate_roots.append(dataset_root)
    candidate_roots.append(traveluav_root / "dataset_raw")

    files: list[Path] = []
    for root in candidate_roots:
        if root.is_file():
            files.append(root)
        else:
            files.extend(_walk_limited(root, max_files=200))

    keyword_hits: dict[str, list[str]] = defaultdict(list)
    json_key_counter: Counter[str] = Counter()
    data_samples: list[str] = []
    lfs_files: list[str] = []

    for path in sorted(set(files)):
        text = _safe_read(path)
        rel = path.relative_to(traveluav_root).as_posix() if path.is_relative_to(traveluav_root) else path.as_posix()
        if _is_lfs_pointer(text):
            lfs_files.append(rel)
        lower = text.lower()
        for group, words in KEYWORDS.items():
            if any(word in lower for word in words):
                keyword_hits[group].append(rel)
        if path.suffix.lower() in DATA_EXTS:
            data_samples.append(rel)
        if path.suffix.lower() == ".json":
            sample = _load_json_sample(path)
            if sample is not None:
                json_key_counter.update(_collect_json_keys(sample))

    dataset_root_exists = bool(dataset_root and dataset_root.exists())
    merged_files: list[Path] = []
    if dataset_root_exists:
        merged_files = list(dataset_root.rglob("merged_data.json"))[:20]
    repo_dataset_raw = traveluav_root / "dataset_raw"
    if not merged_files and repo_dataset_raw.exists():
        merged_files = list(repo_dataset_raw.rglob("merged_data.json"))[:20]
    raw_episode_dirs: list[Path] = []
    if dataset_root_exists and dataset_root is not None:
        try:
            for child in sorted(dataset_root.iterdir()):
                if child.is_dir() and (child / "log").is_dir() and (child / "frontcamera").is_dir():
                    raw_episode_dirs.append(child)
                    if len(raw_episode_dirs) >= 20:
                        break
        except OSError:
            raw_episode_dirs = []

    lines = [
        "# TravelUAV Data Notes",
        "",
        "## Inspection Scope",
        f"- TravelUAV root: `{traveluav_root.as_posix()}`",
        f"- Dataset root: `{dataset_root.as_posix() if dataset_root else '(not provided)'}`",
        f"- Dataset root exists: `{dataset_root_exists}`",
        f"- Found `merged_data.json`: `{len(merged_files)}` sample path(s)",
        f"- Found raw episode dirs with `log/` and `frontcamera/`: `{len(raw_episode_dirs)}` sample path(s)",
        "",
    ]
    if not merged_files and raw_episode_dirs:
        lines.extend(
            [
                "> 已发现真实 TravelUAV raw episode 目录，但当前子集未预生成 `merged_data.json`。本项目转换脚本可直接从 `log/*.json` 与 `frontcamera/*.png` 生成 debug JSONL；后续若要完全复刻 TravelUAV/AeroVLA 流程，可再运行 TravelUAV 的 `generate_merged_json.py`。",
                "",
            ]
        )
    elif not merged_files:
        lines.extend(
            [
                "> 当前未发现完整 dataset_raw，只完成仓库结构和样例文件分析；后续需要用户下载 TravelUAV dataset_raw 后再运行转换。",
                "",
            ]
        )

    lines.extend(["## Repository Structure Summary", ""])
    for sub in [Path("."), Path("data"), Path("scripts"), Path("src"), Path("Model/LLaMA-UAV/tools")]:
        root = traveluav_root / sub
        lines.append(f"### `{sub.as_posix()}`")
        lines.extend(_tree(root, max_depth=2, max_items=60))
        lines.append("")

    lines.extend(["## Candidate Data Entry Files", ""])
    for sample in data_samples[:80]:
        marker = " (Git LFS pointer)" if sample in lfs_files else ""
        lines.append(f"- `{sample}`{marker}")
    if not data_samples:
        lines.append("- No JSON/JSONL/CSV/TXT samples found in scanned paths.")
    lines.append("")

    lines.extend(["## Observed JSON Field Hints", ""])
    for key, count in json_key_counter.most_common(80):
        lines.append(f"- `{key}`: {count}")
    if not json_key_counter:
        lines.append("- No small parseable JSON samples were available.")
    lines.append("")

    lines.extend(["## Keyword-Based Field Candidates", ""])
    for group in ["instruction", "image", "trajectory", "yaw", "action"]:
        lines.append(f"### {group}")
        hits = keyword_hits.get(group, [])
        for hit in hits[:40]:
            lines.append(f"- `{hit}`")
        if not hits:
            lines.append("- No direct keyword hit in scanned lightweight files.")
        lines.append("")

    lines.extend(
        [
            "## Current Understanding",
            "- TravelUAV 仓库 README 指向 Hugging Face 数据集和环境；本地 clone 里部分训练 JSON 是 Git LFS pointer，未下载大数据。",
            "- `data/uav_dataset/*valset*.json` 的样例条目包含 `json` 和 `frame`，其中 `json` 指向 `MapName/EpisodeId/merged_data.json`。",
            "- `Model/LLaMA-UAV/tools/generate_merged_json.py` 会从 `dataset_raw/<map>/<episode>/log/*.json`、相机目录和 `object_description.json` 生成 `merged_data.json`。",
            "- 生成的 `merged_data.json` 关键字段包括 `trajectory`、`trajectory_raw`、`trajectory_raw_detailed`、`image_feature_path`、`index`、`length`、`conversations`。",
            "- 本次下载的地图子集为 raw episode 结构：`<map>/<episode>/log/*.json`、`frontcamera/*.png`、`object_description.json`、`mark.json`；未发现预生成 `merged_data.json`。",
            "- `trajectory_raw*` 中的 pose 预计使用 `position` 和四元数 `orientation`；可转换为本项目 `state=[x,y,z,yaw]`。",
            "- 当前未确认原始文件中存在直接的连续动作字段；默认由相邻轨迹点计算 `action=[vx,vy,vz,yaw_rate]`。",
            "",
            "## TravelUAV -> OpenVLA-OFT JSONL Mapping Suggestion",
            "- `dataset`: 固定为 `TravelUAV`。",
            "- `episode_id`: 从 `merged_data.json` 父目录名或原始 JSON 中 episode 字段获得。",
            "- `step_id`: 使用帧序号或转换后的连续 step index。",
            "- `image`: 优先记录 `frontcamera/<frame>.png`；如后续需要双视角，可扩展为 front/down 两路。",
            "- `instruction`: 使用 `conversations[0].value`，去掉可选 `<image>` 前缀后作为自然语言指令。",
            "- `state`: 从 `trajectory_raw_detailed` 或 `trajectory_raw` 的 `position` + `orientation` 得到 `[x,y,z,yaw]`。",
            "- `action`: 若没有直接 action，则由相邻 state 和 `dt` 计算。",
            "- `action_chunk`: 从当前 step 起取未来 `chunk_size` 个 action，不足时用最后一个 action 填充。",
            "",
        ]
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--traveluav-root", default="external/TravelUAV")
    parser.add_argument("--dataset-root", default=None)
    parser.add_argument("--out", default="docs/traveluav_data_notes.md")
    args = parser.parse_args()
    inspect(Path(args.traveluav_root), Path(args.dataset_root) if args.dataset_root else None, Path(args.out))
    print(f"Wrote TravelUAV notes to {args.out}")


if __name__ == "__main__":
    main()
