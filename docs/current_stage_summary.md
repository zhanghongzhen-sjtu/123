# Current Stage Summary

## Project

VLA + UAV + Reinforcement Learning + Diffusion Policy

Thesis direction:

- OpenVLA-OFT migration to UAV simulation navigation
- TravelUAV as main UAV simulation data source
- UAV continuous action space
- future Diffusion Policy and RL expert trajectory generation

## Current Stage Result

The current stage validates the data and interface route before final OpenVLA-OFT training.

## Completed

### Data

- Downloaded and extracted TravelUAV map subsets on AutoDL RTX 5090.
- Generated real debug JSONL files.
- Built clean timestamp split:
  - `data/processed/clean_train_timestamp_maps.jsonl`
  - `data/processed/clean_val_timestamp_maps.jsonl`

### Validation

- JSONL format checks passed.
- Image paths exist.
- Instructions are non-empty.
- State format: `[x, y, z, yaw]`
- Action format: `[vx, vy, vz, yaw_rate]`
- Action chunk format: `[8, 4]`

### Smoke Tests

- Dataset loader smoke passed.
- Tiny action-head smoke training passed.
- OpenVLA-OFT semantic adapter stub passed.
- OpenVLA-OFT collator-ready stub passed.

### OpenVLA-OFT Analysis

Identified collator contract:

Required item fields:

- `pixel_values`
- `input_ids`
- `labels`
- `actions`

Optional/needed for UAV:

- `proprio`
- `dataset_name`

Identified dimension mismatch:

- OpenVLA-OFT LIBERO default: `ACTION_DIM=7`, `PROPRIO_DIM=8`, `NUM_ACTIONS_CHUNK=8`
- UAV target: `ACTION_DIM=4`, `PROPRIO_DIM=4`, `NUM_ACTIONS_CHUNK=8`

## Current Best Dataset For First Model Stage

Use only clean timestamp split:

- train: `data/processed/clean_train_timestamp_maps.jsonl`
- val: `data/processed/clean_val_timestamp_maps.jsonl`

Hold out fallback-dt maps until dt policy is fixed:

- `Carla_Town01`
- `Carla_Town04`
- `Carla_Town05`

## Not Done Yet

- No OpenVLA/openvla-7b loaded.
- No OpenVLA-OFT checkpoint downloaded.
- No LoRA/OFT run.
- No final VLA training.
- No closed-loop simulator evaluation.
- No Diffusion Policy training.
- No RL training.

## Current Decision

- DATA_ROUTE_READY
- COLLATOR_STUB_READY
- MODEL_STAGE_PLAN_READY
- NOT_FINAL_TRAINING

## Next Decision

Before loading OpenVLA/openvla-7b or any checkpoint, require:

`MODEL_STAGE_CONFIRMED_BY_USER`
