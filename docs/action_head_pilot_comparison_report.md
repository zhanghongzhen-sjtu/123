# Action Head Pilot Comparison Report

## Status

- STATE_ONLY_ACTION_HEAD_BASELINE_PASS
- FROZEN_OPENVLA_UAV_ACTION_HEAD_PILOT_PASS
- LORA_OFT_NOT_STARTED
- FULL_OPENVLA_TRAINING_NOT_STARTED
- CLOSED_LOOP_EVAL_NOT_STARTED

## Dataset

Both pilot runs use the clean timestamp split:

- train: `data/processed/clean_train_timestamp_maps.jsonl`
- val: `data/processed/clean_val_timestamp_maps.jsonl`

Subset size:

- train rows: 120
- val rows: 64

## State-Only Baseline

Model:

- input: `state = [x, y, z, yaw]`
- output: `action_chunk = [8, 4]`
- trainable component: MLP only
- OpenVLA not loaded

Result:

| Epoch | Train Loss | Val Loss |
|---:|---:|---:|
| 1 | 0.1161386982 | 0.1179320836 |
| 2 | 0.1017029164 | 0.1243434155 |
| 3 | 0.0947237183 | 0.1305138526 |

Checkpoint:

- `checkpoints/uav_action_head/state_only_action_head_baseline.pt`

## Frozen OpenVLA + UAV State Pilot

Model:

- input: TravelUAV image + instruction + UAV state
- OpenVLA backbone: frozen
- trainable component: UAV action head only
- output: `action_chunk = [8, 4]`

Result:

| Epoch | Train Loss | Val Loss |
|---:|---:|---:|
| 1 | 0.0925091748 | 0.5789309312 |
| 2 | 0.0336489838 | 0.5619590431 |
| 3 | 0.0154401870 | 0.3945161924 |

Checkpoint:

- `checkpoints/uav_action_head/frozen_openvla_uav_action_head_pilot.pt`

## Interpretation

The state-only baseline has lower validation loss in this pilot setting.

The frozen OpenVLA + UAV state model shows clear training loss reduction and validation loss reduction, which confirms the OpenVLA feature path can be optimized for UAV action chunks.

However, this pilot does not yet prove that frozen OpenVLA features outperform state-only control. The comparison is preliminary because:

- the feature dimensions and heads differ;
- the OpenVLA path may overfit faster on only 120 train rows;
- action/state normalization is not yet fully controlled;
- loss scale may differ due to feature/head behavior;
- only a tiny clean timestamp subset is used.

## Current Conclusion

The project has passed the feasibility gate for OpenVLA-to-UAV action-head adaptation.

The best current baseline for action regression is still the state-only MLP.

The OpenVLA feature path is viable but needs improved normalization, more data, and a more controlled evaluation before claiming advantage.

## Recommended Next Work

1. Add action normalization for both methods.
2. Use identical head architecture where possible.
3. Evaluate on more validation rows.
4. Add per-dimension error metrics for `vx`, `vy`, `vz`, `yaw_rate`.
5. Save prediction samples for trajectory-level visualization.
6. Only after this consider LoRA/OFT tiny smoke.
