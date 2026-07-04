# OpenVLA-OFT UAV Modification Plan

This document defines the next engineering interface between the local TravelUAV JSONL pipeline and a future OpenVLA-OFT UAV experiment. It is a planning document only. The current local machine must not load OpenVLA-OFT / openvla-7b weights, run LoRA / OFT, or train an action head.

## Current Stable Input Contract

The local pipeline now emits OpenVLA-style UAV rows with:

```text
image: front camera observation path
instruction: natural-language target/navigation instruction
state: [x, y, z, yaw]
action: [vx, vy, vz, yaw_rate]
action_chunk: future sequence of UAV actions
dt: timestamp-derived interval in seconds
```

This is the data contract that should be connected to the future OpenVLA-OFT dataset loader.

## Target OpenVLA-OFT Integration Points

Based on the local code-reading notes in `docs/openvla_oft_code_notes.md`, the likely later integration work is:

| Area | Later Change |
| --- | --- |
| Dataset loader | Add or adapt a dataset reader for UAV JSONL rows. |
| Image pipeline | Resolve `image` paths and apply the same visual preprocessing expected by OpenVLA-OFT. |
| Language pipeline | Feed `instruction` as the human/user instruction. |
| Proprio/state projector | Replace or extend robot proprio input with 4D UAV state `[x, y, z, yaw]`. |
| Continuous action head | Configure output dimension as 4D UAV action `[vx, vy, vz, yaw_rate]`. |
| Action chunking | Align model action chunk size with `action_chunk` length from JSONL. |
| Normalization | Use TravelUAV state/action statistics rather than robot dataset statistics. |

## Proposed Work Sequence

1. Freeze the JSONL schema and statistics on a small real subset.
2. Add a UAV dataset reader that yields image, instruction, state, action, action chunk, and metadata.
3. Add UAV state/action normalization config generated from TravelUAV statistics.
4. Add a 4D UAV proprio/state projector path.
5. Add a 4D UAV continuous action head or output adapter.
6. Run a CPU-only dataset-loader smoke test without model weights.
7. Move to AutoDL RTX 5090 for model loading and training experiments.

Steps 1 to 3 now have local lightweight implementations:

- JSONL schema: `docs/uav_jsonl_schema.md`
- Debug statistics: `data/debug/traveluav_3maps_stats.json`
- CPU-only loader: `src/openvla_uav_transfer/datasets/uav_jsonl_dataset.py`
- Smoke test: `scripts/run_smoke_dataset_loader.sh`
- CPU-only OpenVLA-OFT-style collator: `src/openvla_uav_transfer/datasets/uav_collator.py`
- Adapter smoke test: `scripts/run_smoke_openvla_oft_adapter.sh`
- Adapter design: `docs/openvla_oft_dataset_adapter_design.md`

The smoke test passed on both the 60-row merged debug file and the 174-row three-map debug set, with image existence checking and normalization enabled.

The OpenVLA-OFT adapter smoke test passed with batch shape `[8, 4]` for state/action and `[8, 8, 4]` for action chunks.

## Dataset Loader Requirements

The loader should reject rows that do not satisfy:

- `image` exists relative to the configured image root.
- `instruction` is a non-empty string.
- `state` is exactly 4 finite numeric values.
- `action` is exactly 4 finite numeric values.
- `action_chunk` is non-empty and every action is 4 finite numeric values.
- `dt` is a positive finite numeric value.

The loader should keep `source` metadata available for debugging but should not treat it as model input.

## Normalization Requirements

Before training, compute statistics from the actual training split:

- state mean/std/min/max/quantiles
- action mean/std/min/max/quantiles
- dt min/max/mean/median
- action chunk length distribution
- per-map and per-episode counts

The current `data/debug/traveluav_3maps_stats.json` is only a small-subset debug artifact. It should not be used as the final normalization file for full experiments.

## Local vs 5090 Boundary

Can stay local:

- JSONL schema checks.
- Small-subset statistics.
- Dataset-reader unit tests that do not load OpenVLA-OFT weights.
- Documentation and interface planning.
- CPU-only smoke tests for JSONL parsing, image path resolution, and normalization vectors.
- CPU-only OpenVLA-OFT-style batch/collator shape tests.

Must move to AutoDL RTX 5090:

- Loading OpenVLA-OFT / openvla-7b.
- Training or fine-tuning action head.
- LoRA / OFT.
- Full train/val TravelUAV preprocessing and full-split normalization intended for model training.
- Closed-loop simulator evaluation.
- Diffusion Policy training.
- RL expert trajectory generation.

Stop marker for local work:

```text
NEED_5090: 当前任务需要 AutoDL RTX 5090，不应在本地 3060 执行。
```

## Difference From AeroVLA

AeroVLA is a reference for TravelUAV organization and UAV continuous navigation formulation. This project should not simply reproduce AeroVLA. The research angle is cross-embodiment transfer from a general robot VLA base, OpenVLA-OFT, into UAV visual-language navigation, with a UAV-specific state/action adapter and later Diffusion Policy and RL components.
