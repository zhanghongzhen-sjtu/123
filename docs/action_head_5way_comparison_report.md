# Action Head 3-Way Comparison Report

## Status

- `ACTION_HEAD_3WAY_COMPARISON_PASS`
- full LoRA/OFT training: `false`
- closed-loop simulation: `false`

## Summary

| model | rows | overall MAE | overall RMSE |
|---|---:|---:|---:|
| state_only | 64 | 0.343517 | 0.535351 |
| frozen_openvla | 64 | 0.378028 | 0.560554 |
| lora_100step | 64 | 0.380050 | 0.564653 |
| lora_500step | 64 | 0.337601 | 0.519295 |
| lora_1000step | 64 | 0.316975 | 0.498845 |

## Per-Dimension MAE

| model | vx | vy | vz | yaw_rate |
|---|---:|---:|---:|---:|
| state_only | 0.632102 | 0.561595 | 0.121939 | 0.058432 |
| frozen_openvla | 0.638723 | 0.654477 | 0.120941 | 0.097971 |
| lora_100step | 0.777632 | 0.528260 | 0.137618 | 0.076688 |
| lora_500step | 0.655614 | 0.529437 | 0.098637 | 0.066716 |
| lora_1000step | 0.668144 | 0.471828 | 0.062454 | 0.065476 |

## Per-Dimension RMSE

| model | vx | vy | vz | yaw_rate |
|---|---:|---:|---:|---:|
| state_only | 0.788657 | 0.703822 | 0.149762 | 0.081416 |
| frozen_openvla | 0.751441 | 0.807475 | 0.157428 | 0.124186 |
| lora_100step | 0.885195 | 0.674460 | 0.165609 | 0.097141 |
| lora_500step | 0.767426 | 0.681698 | 0.130768 | 0.088955 |
| lora_1000step | 0.775280 | 0.613470 | 0.102953 | 0.085915 |

## Plots

- `data/debug/plots/combined_5way/overall_error_bar.png`
- `data/debug/plots/combined_5way/per_dim_mae_bar.png`
- `data/debug/plots/combined_5way/per_dim_rmse_bar.png`

## Interpretation

This comparison evaluates action_chunk prediction on the same validation subset.
The LoRA 100-step result verifies the trainable OpenVLA transfer path, but it should still be treated as a pilot result rather than final OpenVLA-OFT training.

