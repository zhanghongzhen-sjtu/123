# Frozen OpenVLA Prediction Visualization Report

## Status

- FROZEN_OPENVLA_PREDICTION_EXPORT_PASS
- ACTION_PREDICTION_PLOT_PASS
- OPENVLA_FROZEN
- LORA_OFT_NOT_STARTED
- FULL_TRAINING_NOT_STARTED

## Files

Prediction JSONL:

- `data/debug/predictions/frozen_openvla_val_predictions.jsonl`

Plots:

- `data/debug/plots/frozen_openvla/frozen_openvla_vx_target_vs_pred.png`
- `data/debug/plots/frozen_openvla/frozen_openvla_vy_target_vs_pred.png`
- `data/debug/plots/frozen_openvla/frozen_openvla_vz_target_vs_pred.png`
- `data/debug/plots/frozen_openvla/frozen_openvla_yaw_rate_target_vs_pred.png`
- `data/debug/plots/frozen_openvla/frozen_openvla_vx_abs_error.png`
- `data/debug/plots/frozen_openvla/frozen_openvla_vy_abs_error.png`
- `data/debug/plots/frozen_openvla/frozen_openvla_vz_abs_error.png`
- `data/debug/plots/frozen_openvla/frozen_openvla_yaw_rate_abs_error.png`
- `data/debug/plots/frozen_openvla/frozen_openvla_per_dim_error_bar.png`

## Interpretation

These plots visualize the frozen OpenVLA + UAV action head pilot predictions.

They should be compared with the state-only baseline plots to understand whether visual-language features improve or degrade action prediction in each dimension.
