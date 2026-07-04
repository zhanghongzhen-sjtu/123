# Model Stage Entry Checklist

## Current Completed Status

- REAL_TRAVELUAV_DATA_PASS
- CLEAN_TIMESTAMP_SPLIT_PASS
- TINY_ACTION_HEAD_SMOKE_PASS
- OPENVLA_OFT_COLLATOR_CONTRACT_IDENTIFIED
- UAV_DIMENSION_MISMATCH_IDENTIFIED
- UAV_CONSTANTS_PATCH_PLANNED
- UAV_JSONL_COLLATOR_READY_STUB_PASS

## Current Best Dataset

Use only clean timestamp subset for first model-stage smoke:

- train: `data/processed/clean_train_timestamp_maps.jsonl`
- val: `data/processed/clean_val_timestamp_maps.jsonl`

Do not use fallback-dt maps for first model-stage training:

- `Carla_Town01`
- `Carla_Town04`
- `Carla_Town05`

## UAV Dimensions

- `NUM_ACTIONS_CHUNK = 8`
- `ACTION_DIM = 4`
- `PROPRIO_DIM = 4`
- `state = [x, y, z, yaw]`
- `action = [vx, vy, vz, yaw_rate]`
- `action_chunk = [8, 4]`

## OpenVLA-OFT Collator Contract

Each dataset item should provide:

Required:

- `pixel_values`
- `input_ids`
- `labels`
- `actions`

Optional but needed for UAV migration:

- `proprio`
- `dataset_name`

Expected batch shapes:

- `pixel_values = [B, 3, H, W]`
- `input_ids = [B, L]`
- `attention_mask = [B, L]`
- `labels = [B, L]`
- `actions = [B, 8, 4]`
- `proprio = [B, 4]`

## Must Not Do Without Explicit Confirmation

- load `openvla-7b`
- download OpenVLA-OFT checkpoints
- start LoRA/OFT
- train OpenVLA
- run closed-loop simulator evaluation
- process full TravelUAV
- claim final performance

## Allowed First Model-Stage Smoke

Only after explicit confirmation:

1. install missing OpenVLA-OFT Python dependencies if needed;
2. load tokenizer/processor or image transform only;
3. verify one clean timestamp mini-batch can be tokenized/transformed;
4. optionally load OpenVLA-OFT model on RTX 5090 for a one-batch forward smoke;
5. no optimizer step unless separately confirmed.

## Decision Marker

Before loading OpenVLA/openvla-7b or any checkpoint, require:

`MODEL_STAGE_CONFIRMED_BY_USER`

