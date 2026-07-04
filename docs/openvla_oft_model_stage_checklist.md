# OpenVLA-OFT Model Stage Checklist

## Current Confirmed Status

- Real TravelUAV data has been converted to OpenVLA-style UAV JSONL.
- Image paths exist.
- Instructions are non-empty.
- UAV state is `[x, y, z, yaw]`.
- UAV action is `[vx, vy, vz, yaw_rate]`.
- UAV action chunk target is `[8, 4]`.
- Clean timestamp subset passes dataloader smoke.
- Tiny action-head smoke training passes.

## Current Best Dataset For First Model-Stage Experiment

Use clean timestamp subset first:

- train: `data/processed/clean_train_timestamp_maps.jsonl`
- val: `data/processed/clean_val_timestamp_maps.jsonl`
- stats: `data/processed/clean_train_timestamp_stats.json`

Do not use fallback-dt maps for first OpenVLA-OFT model-stage training:

- `Carla_Town01`
- `Carla_Town04`
- `Carla_Town05`

They can be used later after dt policy is fixed.

## Before Loading OpenVLA-OFT

Verify without model loading:

1. OpenVLA-OFT repo exists:
   - `external/openvla-oft`

2. Identify training entrypoint:
   - likely under `external/openvla-oft/vla-scripts/`
   - likely under `external/openvla-oft/experiments/`

3. Identify action head code:
   - continuous action head location needs final confirmation.

4. Identify proprio/state projector code:
   - UAV state `[x,y,z,yaw]` should connect here.

5. Confirm action chunk size:
   - current UAV target uses `[8,4]`.

6. Confirm batch schema:
   - image path
   - instruction string
   - state tensor `[4]`
   - action tensor `[4]`
   - action_chunk tensor `[8,4]`

## Allowed On RTX 5090

- load OpenVLA-OFT/openvla-7b only after explicit model-stage confirmation;
- run tiny subset model loading smoke;
- run small LoRA/OFT smoke only after config is frozen;
- train UAV action head on clean timestamp subset;
- later scale to medium/full TravelUAV.

## Not Yet Ready

This project is not yet ready for full OpenVLA-OFT training because:

- only small debug/medium subsets have been validated;
- UAV action head integration is not implemented inside OpenVLA-OFT yet;
- state projector wiring still needs code-level confirmation;
- fallback-dt maps need a consistent timing policy;
- no closed-loop simulation evaluation has been run.

## Stop Condition

If the next command would load OpenVLA-OFT/openvla-7b or start LoRA/OFT training, explicitly confirm model-stage execution first.

Marker:

MODEL_STAGE_CONFIRMATION_REQUIRED
