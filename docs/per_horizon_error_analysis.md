# Per-Horizon Action Chunk Error Analysis

## Status

- `PER_HORIZON_ERROR_ANALYSIS_PASS`

## Overall MAE By Horizon

| model | h1 | h2 | h3 | h4 | h5 | h6 | h7 | h8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| state_only | 0.367891 | 0.392321 | 0.351241 | 0.367636 | 0.358622 | 0.373943 | 0.362798 | 0.388413 |
| frozen_openvla | 0.405505 | 0.385590 | 0.373936 | 0.378854 | 0.369709 | 0.367894 | 0.376836 | 0.371390 |
| lora_full_5000step | 0.327059 | 0.323925 | 0.285123 | 0.324137 | 0.307795 | 0.301878 | 0.295725 | 0.286533 |

## Interpretation

This analysis shows how action_chunk prediction error changes from near-term to farther-horizon actions.
If errors grow with horizon, it motivates a sequence modeling module such as Diffusion Policy for low-level control.

## Plots

- `data/debug/plots/per_horizon_error_analysis/per_horizon_overall_mae.png`
- `data/debug/plots/per_horizon_error_analysis/per_horizon_dim_mae.png`
- `data/debug/plots/per_horizon_error_analysis/per_horizon_dim_rmse.png`
