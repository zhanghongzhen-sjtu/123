# Action Head 3-Way Comparison Report

## Status

- `ACTION_HEAD_3WAY_COMPARISON_PASS`
- full LoRA/OFT training: `false`
- closed-loop simulation: `false`

## Summary

| model | rows | overall MAE | overall RMSE |
|---|---:|---:|---:|
| state_only | 4325 | 0.370358 | 0.540057 |
| frozen_openvla | 4325 | 0.378714 | 0.576812 |
| lora_full_5000step | 109 | 0.306522 | 0.488199 |
| lora_weighted_5000step | 4325 | 0.358230 | 0.516611 |

## Per-Dimension MAE

| model | vx | vy | vz | yaw_rate |
|---|---:|---:|---:|---:|
| state_only | 0.693377 | 0.581320 | 0.144735 | 0.062002 |
| frozen_openvla | 0.743466 | 0.565860 | 0.135154 | 0.070370 |
| lora_full_5000step | 0.253343 | 0.765815 | 0.160873 | 0.046056 |
| lora_weighted_5000step | 0.671483 | 0.583566 | 0.101883 | 0.075988 |

## Per-Dimension RMSE

| model | vx | vy | vz | yaw_rate |
|---|---:|---:|---:|---:|
| state_only | 0.813757 | 0.667918 | 0.216067 | 0.107913 |
| frozen_openvla | 0.903933 | 0.671239 | 0.220649 | 0.120405 |
| lora_full_5000step | 0.401141 | 0.844383 | 0.275011 | 0.061842 |
| lora_weighted_5000step | 0.741885 | 0.683022 | 0.189185 | 0.121834 |

## Plots

- `data/debug/plots/full_clean_val_weighted_4way/overall_error_bar.png`
- `data/debug/plots/full_clean_val_weighted_4way/per_dim_mae_bar.png`
- `data/debug/plots/full_clean_val_weighted_4way/per_dim_rmse_bar.png`

## Interpretation

This comparison evaluates action_chunk prediction on the same validation subset.
The LoRA 100-step result verifies the trainable OpenVLA transfer path, but it should still be treated as a pilot result rather than final OpenVLA-OFT training.

