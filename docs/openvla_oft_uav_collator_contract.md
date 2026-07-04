# OpenVLA-OFT UAV Collator Contract

## Source

Static reading only:

- `external/openvla-oft/prismatic/util/data_utils.py`
- `external/openvla-oft/prismatic/vla/datasets/datasets.py`
- `external/openvla-oft/vla-scripts/finetune.py`

No OpenVLA/openvla-7b model was loaded. No LoRA/OFT training was started.

## OpenVLA-OFT Collator

`PaddedCollatorForActionPrediction` expects each dataset item to contain:

Required:

- `pixel_values`: `torch.Tensor`
- `input_ids`: `torch.Tensor`
- `labels`: `torch.Tensor`
- `actions`: numpy array, stacked into batch tensor by the collator

Optional:

- `proprio`: stacked into batch tensor if present
- `dataset_name`: collected as `dataset_names`
- `pixel_values_wrist`: optionally concatenated with `pixel_values`

The collator returns:

- `pixel_values`
- `proprio`
- `input_ids`
- `attention_mask`
- `labels`
- `actions`
- optional `dataset_names`

## Current UAV JSONL Schema

Each TravelUAV JSONL row contains:

- `dataset`
- `episode_id`
- `step_id`
- `image`
- `instruction`
- `state = [x, y, z, yaw]`
- `action = [vx, vy, vz, yaw_rate]`
- `action_chunk = [8, 4]`
- `dt`
- `source`

## UAV To OpenVLA-OFT Item Mapping

| UAV JSONL field | OpenVLA-OFT dataset item field | Notes |
|---|---|---|
| `image` | `pixel_values` | Requires image loading and OpenVLA/OFT image transform. |
| `instruction` | `input_ids`, `labels` | Requires tokenizer and prompt builder. |
| `state` | `proprio` | UAV proprio dim is 4. |
| `action_chunk` | `actions` | Shape should be `[8, 4]`. |
| `dataset` | `dataset_name` | Use `TravelUAV`. |
| `episode_id`, `step_id`, `source`, `dt` | metadata only | Useful for debugging, not required by collator. |

## Prompt Format Candidate

Following OpenVLA dummy dataset style:

Human:

`What action should the robot take to {instruction}?`

Assistant:

action tokens or continuous action target placeholder.

For continuous action-head training, `actions` carries the numeric target. The label masking policy still needs to follow OpenVLA-OFT training code.

## Dimension Contract

Current UAV setting:

- proprio dim: `4`
- action dim: `4`
- action chunk size: `8`
- actions shape per item: `[8, 4]`

OpenVLA-OFT defaults may differ:

- `PROPRIO_DIM` may be robot-specific.
- `ACTION_DIM` may be robot-specific.
- `NUM_ACTIONS_CHUNK` may already be 8.

Therefore, UAV migration requires checking and possibly changing constants/config:

- `prismatic/vla/constants.py`
- action head construction
- proprio projector construction
- dataset statistics normalization

## Important Decision

The JSONL and adapter stub are valid for data-route verification.

They are not yet directly ready for OpenVLA-OFT training because:

1. `pixel_values` requires the OpenVLA image transform;
2. `input_ids` and `labels` require tokenizer and prompt builder;
3. UAV `ACTION_DIM=4` must be reconciled with OpenVLA-OFT constants;
4. UAV `PROPRIO_DIM=4` must be reconciled with proprio projector config;
5. normalization statistics must match UAV action/state dimensions.

## Recommended Next Step

Create a `UAVJsonlDataset` design that mirrors `DummyDataset`, but keep it as a design/stub until model-stage confirmation.

Do not start full OpenVLA-OFT training yet.

## Status

- COLLATOR_CONTRACT_IDENTIFIED
- UAV_JSONL_SCHEMA_COMPATIBLE_AT_SEMANTIC_LEVEL
- MODEL_STAGE_CONFIRMATION_REQUIRED_FOR_TOKENIZER_IMAGE_TRANSFORM
- NOT_FINAL_TRAINING
