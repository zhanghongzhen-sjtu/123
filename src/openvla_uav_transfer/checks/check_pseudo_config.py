"""Check the local OpenVLA-OFT UAV pseudo config without model loading."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from src.openvla_uav_transfer.datasets import OpenVLAOFTUavCollator, UavJsonlDataset


EXPECTED_SCHEMA = "uav_openvla_pseudo_config_v0.1"
STOP_MARKER = "NEED_5090: 当前任务需要 AutoDL RTX 5090，不应在本地 3060 执行。"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level YAML must be a mapping")
    return data


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _path_exists(path_text: str, label: str) -> None:
    _require(Path(path_text).exists(), f"{label} does not exist: {path_text}")


def _check_safety(config: dict[str, Any]) -> list[str]:
    safety = config.get("safety")
    _require(isinstance(safety, dict), "missing safety section")
    disabled_flags = (
        "training_enabled",
        "model_loading_enabled",
        "lora_oft_enabled",
        "closed_loop_eval_enabled",
        "simulator_enabled",
        "diffusion_policy_training_enabled",
        "rl_training_enabled",
    )
    for flag in disabled_flags:
        _require(safety.get(flag) is False, f"safety.{flag} must be false for local pseudo config")
    _require(safety.get("stop_marker") == STOP_MARKER, "safety.stop_marker is missing or changed")
    return [f"{flag}=false" for flag in disabled_flags]


def _check_stats(stats_path: Path, state_dim: int, action_dim: int) -> dict[str, Any]:
    with stats_path.open("r", encoding="utf-8") as f:
        stats = json.load(f)
    state_norm = stats.get("state", {}).get("normalization", {})
    action_norm = stats.get("action", {}).get("normalization", {})
    for key in ("mean", "std", "min", "max"):
        _require(len(state_norm.get(key, [])) == state_dim, f"state normalization {key} must be {state_dim}D")
        _require(len(action_norm.get(key, [])) == action_dim, f"action normalization {key} must be {action_dim}D")
    return {
        "row_count": stats.get("row_count"),
        "dt_sources": stats.get("dt_sources"),
        "action_chunk_lengths": stats.get("action_chunk_lengths"),
    }


def check_config(config_path: Path) -> dict[str, Any]:
    config = _load_yaml(config_path)
    _require(config.get("schema_version") == EXPECTED_SCHEMA, f"schema_version must be {EXPECTED_SCHEMA}")
    safety_flags = _check_safety(config)

    repos = config.get("external_repos")
    _require(isinstance(repos, dict), "missing external_repos section")
    for key in ("openvla_oft_root", "traveluav_root", "aerovla_root"):
        _path_exists(str(repos.get(key)), f"external_repos.{key}")

    local_debug = config.get("local_debug")
    _require(isinstance(local_debug, dict), "missing local_debug section")
    _require(local_debug.get("training_ready") is False, "local_debug.training_ready must be false")
    _require(local_debug.get("real_data_debug") is True, "local_debug.real_data_debug must be true")

    jsonl_files = local_debug.get("jsonl_files")
    _require(isinstance(jsonl_files, list) and jsonl_files, "local_debug.jsonl_files must be a non-empty list")
    for path in jsonl_files:
        _path_exists(str(path), "local_debug.jsonl_files item")

    stats_path = Path(str(local_debug.get("stats_json")))
    _path_exists(stats_path.as_posix(), "local_debug.stats_json")
    _path_exists(str(local_debug.get("validation_report")), "local_debug.validation_report")
    _path_exists(str(local_debug.get("adapter_smoke_report")), "local_debug.adapter_smoke_report")

    uav = config.get("uav_interface")
    _require(isinstance(uav, dict), "missing uav_interface section")
    _require(uav.get("state_dim") == 4, "uav_interface.state_dim must be 4")
    _require(uav.get("action_dim") == 4, "uav_interface.action_dim must be 4")
    _require(uav.get("action_chunk_size") == 8, "uav_interface.action_chunk_size must be 8")
    _require(uav.get("dt_source") == "timestamp", "uav_interface.dt_source must be timestamp")

    stats_summary = _check_stats(stats_path, int(uav["state_dim"]), int(uav["action_dim"]))

    smoke = config.get("adapter_smoke")
    _require(isinstance(smoke, dict), "missing adapter_smoke section")
    batch_size = int(smoke.get("batch_size"))
    chunk_size = int(uav["action_chunk_size"])
    dataset = UavJsonlDataset(
        jsonl_paths=[Path(str(path)) for path in jsonl_files],
        image_root=Path(str(local_debug.get("image_root", "."))),
        stats_path=stats_path,
        require_image_exists=bool(smoke.get("check_images")),
        normalize=bool(smoke.get("normalize")),
    )
    samples = [dataset[idx] for idx in range(min(batch_size, len(dataset)))]
    batch = OpenVLAOFTUavCollator(
        expected_action_chunk_size=chunk_size,
        require_normalized=bool(smoke.get("normalize")),
    )(samples)

    expected_shapes = smoke.get("expected_shapes")
    _require(isinstance(expected_shapes, dict), "adapter_smoke.expected_shapes must be a mapping")
    for key, expected in expected_shapes.items():
        _require(batch["shapes"].get(key) == expected, f"shape mismatch for {key}: expected {expected}, got {batch['shapes'].get(key)}")

    future = config.get("future_5090")
    _require(isinstance(future, dict), "missing future_5090 section")
    _require(future.get("status") == "planned_only_do_not_run_locally", "future_5090.status must remain planned_only_do_not_run_locally")

    return {
        "config": config_path.as_posix(),
        "schema_version": config.get("schema_version"),
        "safety_flags": safety_flags,
        "jsonl_files": jsonl_files,
        "dataset_summary": dataset.summary(),
        "stats_summary": stats_summary,
        "batch_shapes": batch["shapes"],
        "future_5090_status": future.get("status"),
        "status": "PSEUDO_CONFIG_PASS",
    }


def write_report(result: dict[str, Any], out: Path) -> None:
    lines = [
        "# OpenVLA-OFT UAV Pseudo Config Check Report",
        "",
        "This report validates the local pseudo configuration only. It does not load OpenVLA-OFT, train, run LoRA/OFT, or run simulator evaluation.",
        "",
        "## Config",
        "",
        f"- Config file: `{result['config']}`",
        f"- Schema version: `{result['schema_version']}`",
        f"- Status: `{result['status']}`",
        "",
        "## Safety",
        "",
    ]
    lines.extend(f"- `{flag}`" for flag in result["safety_flags"])
    lines.extend(
        [
            "",
            "## Dataset",
            "",
            f"- JSONL files: `{result['jsonl_files']}`",
            f"- Dataset summary: `{result['dataset_summary']}`",
            f"- Stats summary: `{result['stats_summary']}`",
            "",
            "## Batch Shapes",
            "",
            f"- `{result['batch_shapes']}`",
            "",
            "## 5090 Boundary",
            "",
            f"- future_5090 status: `{result['future_5090_status']}`",
            "- Full train/val conversion, full normalization stats, model loading, action-head training, LoRA/OFT, closed-loop evaluation, Diffusion Policy training, and RL training are not local tasks.",
            "",
            "## Final",
            "",
            "- `PSEUDO_CONFIG_PASS`",
            "- `NOT_TRAINING_READY`",
        ]
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/openvla_oft_uav_debug.yaml")
    parser.add_argument("--out", default="docs/openvla_oft_uav_pseudo_config_check_report.md")
    args = parser.parse_args()
    try:
        result = check_config(Path(args.config))
        write_report(result, Path(args.out))
    except Exception as exc:
        print(f"PSEUDO_CONFIG_FAIL: {exc}")
        raise SystemExit(1) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("PSEUDO_CONFIG_PASS: local OpenVLA-OFT UAV pseudo config is valid and training remains disabled.")


if __name__ == "__main__":
    main()
