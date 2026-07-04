# State-Only Prediction Visualization Report

## Status

- STATE_ONLY_PREDICTION_EXPORT_PASS
- ACTION_PREDICTION_PLOT_PASS

## Files

Prediction JSONL:

- `data/debug/predictions/state_only_val_predictions.jsonl`

Plots:

- `data/debug/plots/state_only/state_only_vx_target_vs_pred.png`
- `data/debug/plots/state_only/state_only_vy_target_vs_pred.png`
- `data/debug/plots/state_only/state_only_vz_target_vs_pred.png`
- `data/debug/plots/state_only/state_only_yaw_rate_target_vs_pred.png`
- `data/debug/plots/state_only/state_only_vx_abs_error.png`
- `data/debug/plots/state_only/state_only_vy_abs_error.png`
- `data/debug/plots/state_only/state_only_vz_abs_error.png`
- `data/debug/plots/state_only/state_only_yaw_rate_abs_error.png`
- `data/debug/plots/state_only/state_only_per_dim_error_bar.png`

## Interpretation

These plots are for pilot debugging and thesis-method visualization.

They help identify which UAV action dimensions are difficult to predict.

Current pilot metrics show that horizontal velocity dimensions, especially `vx` and `vy`, dominate the error.
