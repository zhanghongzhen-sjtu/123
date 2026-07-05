# Action Head 3-Way Comparison Report

## Status

- `ACTION_HEAD_3WAY_COMPARISON_PASS`
- full LoRA/OFT training: `false`
- closed-loop simulation: `false`

## Summary

| model | rows | overall MAE | overall RMSE |
|---|---:|---:|---:|
| state_only_body | 4325 | 0.317849 | 0.515717 |
| lora_body_5000step | 4325 | 0.338384 | 0.603779 |

## Per-Dimension MAE

| model | vx | vy | vz | yaw_rate |
|---|---:|---:|---:|---:|
| state_only_body | 0.936842 | 0.144711 | 0.118415 | 0.071430 |
| lora_body_5000step | 1.031891 | 0.139387 | 0.119003 | 0.063253 |

## Per-Dimension RMSE

| model | vx | vy | vz | yaw_rate |
|---|---:|---:|---:|---:|
| state_only_body | 0.977018 | 0.239795 | 0.197168 | 0.113647 |
| lora_body_5000step | 1.162398 | 0.237324 | 0.197786 | 0.107601 |

## Plots

- `data/debug/plots/body_frame_val_2way/overall_error_bar.png`
- `data/debug/plots/body_frame_val_2way/per_dim_mae_bar.png`
- `data/debug/plots/body_frame_val_2way/per_dim_rmse_bar.png`

## Interpretation

This comparison evaluates action_chunk prediction on the same validation subset.
The LoRA 100-step result verifies the trainable OpenVLA transfer path, but it should still be treated as a pilot result rather than final OpenVLA-OFT training.

