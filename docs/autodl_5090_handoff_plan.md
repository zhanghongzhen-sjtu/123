# AutoDL RTX 5090 Handoff Plan

This plan describes how to move from the local first-stage engineering work to a future AutoDL RTX 5090 training environment. It is a handoff plan only. It does not authorize local model loading or training.

## Current Local Status

Completed locally:

- Project structure and external repo analysis.
- TravelUAV raw 3-map debug conversion.
- UAV state/action adapter.
- Real JSONL schema validation.
- Trajectory visualization.
- Debug statistics.
- CPU-only dataset loader smoke test.
- CPU-only OpenVLA-OFT-style collator smoke test.
- OpenVLA-OFT UAV pseudo config check.

Current status markers:

```text
FORMAT_PASS
ACTION_PASS
ADAPTER_SMOKE_PASS
PSEUDO_CONFIG_PASS
NOT_TRAINING_READY
```

The debug subset validates the data path, but it is not a final training dataset.

## Handoff Goal

The 5090 stage should start only after the local schema and adapter contract are frozen. Its goal is to prepare and run the actual training/evaluation work:

```text
full TravelUAV train/val split
-> full OpenVLA-OFT-style JSONL
-> full train split normalization stats
-> OpenVLA-OFT UAV dataset adapter
-> UAV 4D proprio/state projector
-> UAV 4D continuous action head
-> 5090 training/evaluation
```

## What To Transfer

Transfer the lightweight project files:

- `README.md`
- `.gitignore`
- `requirements.txt`
- `configs/`
- `src/`
- `scripts/`
- `docs/`
- `data/debug/README.md`
- small debug JSONL/stat files under `data/debug/`
- debug trajectory plots under `data/debug/plots/`

Do not transfer as part of the lightweight handoff payload:

- `data/raw/`
- `data/processed/`
- `external/`
- `.venv/`
- `logs/`
- `work/`
- `tools/`
- model checkpoints or weight files

Raw datasets and model checkpoints should be placed directly on AutoDL storage according to `configs/autodl_5090_paths.yaml`.

## AutoDL Path Template

Path template:

```text
configs/autodl_5090_paths.yaml
```

Important planned paths:

- Project root: `/root/autodl-tmp/vla-uav-diffusion`
- Full TravelUAV root: `/root/autodl-tmp/datasets/TravelUAV`
- Train JSONL: `/root/autodl-tmp/vla-uav-diffusion/data/processed/traveluav_train_openvla_oft.jsonl`
- Val JSONL: `/root/autodl-tmp/vla-uav-diffusion/data/processed/traveluav_val_openvla_oft.jsonl`
- Train stats: `/root/autodl-tmp/vla-uav-diffusion/data/processed/traveluav_train_stats.json`
- OpenVLA base checkpoint: `/root/autodl-tmp/models/openvla-7b`
- OpenVLA-OFT checkpoint: `/root/autodl-tmp/models/openvla-oft`

All training-related switches in the template remain `false` until the 5090 environment is ready and the user explicitly approves training.

## Recommended 5090 Sequence

1. Create AutoDL project directory.
2. Copy the lightweight handoff payload into the project directory.
3. Clone or copy external repos on AutoDL.
4. Place the full TravelUAV dataset under the configured dataset root.
5. Run repository/data inspection on AutoDL.
6. Convert full train/val split to OpenVLA-OFT-style JSONL.
7. Compute full train split normalization stats.
8. Run JSONL validation on the full train/val outputs.
9. Run CPU-only dataset loader and collator smoke tests on full split samples.
10. Only then load OpenVLA-OFT / openvla-7b and begin model work.

## Commands That Remain Local-Safe

These are safe locally because they do not load models or train:

```bash
bash scripts/run_check_pseudo_config.sh
bash scripts/run_smoke_dataset_loader.sh
bash scripts/run_smoke_openvla_oft_adapter.sh
python3 -m src.openvla_uav_transfer.checks.validate_uav_jsonl --image-root . --out docs/jsonl_validation_report.md
python3 scripts/visualize_uav_jsonl.py --jsonl data/debug/traveluav_BrushifyCountryRoads_debug.jsonl --out-dir data/debug/plots
```

## Commands That Must Wait For 5090

Do not run locally:

- loading OpenVLA-OFT / openvla-7b;
- training UAV action head;
- LoRA / OFT fine-tuning;
- full train/val preprocessing intended for training;
- full normalization stats for final training;
- closed-loop simulator evaluation;
- Diffusion Policy training;
- RL expert trajectory generation.

If a local task requires any of these, stop with:

```text
NEED_5090: 当前任务需要 AutoDL RTX 5090，不应在本地 3060 执行。
```

## Full Data Timing

Full data should be used when the project moves from interface validation to training preparation:

- The local debug schema has passed.
- The action recompute check has passed.
- Dataset loader and collator smoke tests have passed.
- The pseudo config and 5090 path template are fixed.
- The user is ready to allocate 5090 storage and runtime.

At that point, full train/val conversion and full train statistics should be performed on or near the 5090 environment, so the generated paths and normalization stats match the actual training setup.

## Handoff Preview

Run locally:

```bash
bash scripts/package_handoff_preview.sh
```

This writes:

```text
docs/autodl_5090_handoff_manifest.md
```

The preview lists files that should be included and confirms that heavy directories such as `data/raw`, `external`, `.venv`, `logs`, `work`, and model weights are excluded.
