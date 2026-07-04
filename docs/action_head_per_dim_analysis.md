# Action Head Per-Dimension Analysis

## Status

- ACTION_HEAD_PER_DIM_EVAL_PASS
- LORA_OFT_NOT_STARTED
- FULL_TRAINING_NOT_STARTED
- CLOSED_LOOP_EVAL_NOT_STARTED

## Validation Split

- file: `data/processed/clean_val_timestamp_maps.jsonl`
- rows: 64

## Overall Metrics

| Model | Overall MAE | Overall RMSE |
|---|---:|---:|
| State-only MLP | 0.3269 | 0.5125 |
| Frozen OpenVLA + UAV state | 0.3783 | 0.5667 |

## Per-Dimension MAE

| Model | vx | vy | vz | yaw_rate |
|---|---:|---:|---:|---:|
| State-only MLP | 0.5747 | 0.5412 | 0.1261 | 0.0656 |
| Frozen OpenVLA + UAV state | 0.6335 | 0.6503 | 0.1268 | 0.1026 |

## Per-Dimension RMSE

| Model | vx | vy | vz | yaw_rate |
|---|---:|---:|---:|---:|
| State-only MLP | 0.7332 | 0.6932 | 0.1578 | 0.0872 |
| Frozen OpenVLA + UAV state | 0.7674 | 0.8067 | 0.1651 | 0.1334 |

## Interpretation

The state-only MLP is stronger in the current pilot setting.

The frozen OpenVLA + UAV state model is trainable and its validation loss decreases, but it does not yet outperform the state-only baseline.

The largest errors for both models are in horizontal velocity:

- `vx`
- `vy`

The vertical velocity and yaw-rate targets are easier in this pilot subset:

- `vz`
- `yaw_rate`

## Likely Reasons

1. The clean pilot dataset is small.
2. OpenVLA is frozen, so its robot-domain representation may not align with UAV motion.
3. The action head may overfit the small train subset.
4. Action dimensions are not normalized per dimension for training/eval.
5. The current feature extraction uses a simple last hidden state, not necessarily an action-relevant representation.
6. The validation maps may differ from training maps.

## Current Research Conclusion

The project has passed the feasibility gate for OpenVLA-to-UAV action-head adaptation.

However, current evidence does not prove that frozen OpenVLA features improve UAV action prediction over a state-only baseline.

## Recommended Next Work

1. Add action normalization using train-set statistics.
2. Re-run both state-only and frozen-OpenVLA pilots with identical normalized targets.
3. Evaluate per-dimension normalized and denormalized errors.
4. Save prediction samples for trajectory visualization.
5. Consider LoRA/OFT only after normalized frozen-feature pilot is stable.
