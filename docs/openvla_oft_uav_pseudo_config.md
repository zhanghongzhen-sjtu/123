# OpenVLA-OFT UAV Pseudo Config

This document explains the local pseudo configuration for the future OpenVLA-OFT UAV migration experiment.

Config file:

```text
configs/openvla_oft_uav_debug.yaml
```

Check script:

```text
src/openvla_uav_transfer/checks/check_pseudo_config.py
```

Runner:

```bash
cd /mnt/d/中期/vla-uav-diffusion
bash scripts/run_check_pseudo_config.sh
```

Expected marker:

```text
PSEUDO_CONFIG_PASS: local OpenVLA-OFT UAV pseudo config is valid and training remains disabled.
```

## Purpose

The pseudo config freezes the first-stage interface:

```text
TravelUAV real debug JSONL
-> UAV schema/action validation
-> dataset loader
-> OpenVLA-OFT-style collator
-> future 5090 training plan
```

It is not a training config. It is a local interface contract and a checklist for the later 5090 stage.

## Current Local Debug Inputs

The active debug JSONL is:

```text
data/debug/traveluav_BrushifyCountryRoads_debug.jsonl
```

Related local files:

- `data/debug/traveluav_3maps_stats.json`
- `docs/jsonl_validation_report.md`
- `docs/openvla_oft_adapter_smoke_report.md`

The pseudo config checks:

- all safety training/model flags are disabled;
- external repo paths exist;
- debug JSONL exists;
- stats JSON exists and contains 4D state/action normalization vectors;
- state dim is 4;
- action dim is 4;
- action chunk size is 8;
- batch shapes match `[B,4]` and `[B,8,4]`;
- future 5090 section is marked as `planned_only_do_not_run_locally`.

## Full Data And 5090 Boundary

Full data is introduced only after the local interface is frozen.

Local is still appropriate for:

- small debug JSONL validation;
- schema checks;
- trajectory visualization;
- CPU-only dataset loader tests;
- CPU-only collator/batch shape tests;
- pseudo config checks.

Move to AutoDL RTX 5090 for:

- full train/val conversion when it is intended for OpenVLA-OFT training;
- full train split normalization statistics;
- loading OpenVLA-OFT / openvla-7b;
- UAV action head training;
- LoRA / OFT;
- closed-loop simulator evaluation;
- Diffusion Policy training;
- RL expert generation.

The practical handoff moment is:

```text
After debug schema + adapter + pseudo config pass, and before full train/val preprocessing intended for training.
```

If the local workflow attempts model loading or training, stop with:

```text
NEED_5090: 当前任务需要 AutoDL RTX 5090，不应在本地 3060 执行。
```

## Current Status

The pseudo config is expected to remain:

```text
training_enabled: false
model_loading_enabled: false
lora_oft_enabled: false
closed_loop_eval_enabled: false
```

Therefore the correct conclusion is:

```text
PSEUDO_CONFIG_PASS
NOT_TRAINING_READY
```

## Handoff Link

The next-stage 5090 handoff files are:

- `configs/autodl_5090_paths.yaml`
- `docs/autodl_5090_handoff_plan.md`
- `docs/autodl_5090_handoff_manifest.md`
- `scripts/package_handoff_preview.sh`

The manifest is only a lightweight preview. It intentionally excludes raw TravelUAV data, external repositories, logs, virtual environments, and model weights.
