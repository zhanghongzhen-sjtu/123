# Action Head Combined Comparison Report

## Status

- ACTION_HEAD_COMBINED_COMPARISON_PASS
- LORA_OFT_NOT_STARTED
- FULL_TRAINING_NOT_STARTED

## Plots

- `data/debug/plots/combined/combined_per_dim_error_bar.png`
- `data/debug/plots/combined/combined_overall_error_bar.png`
- `data/debug/plots/combined/combined_error_difference_bar.png`

## Result

```json
{
  "status": "ACTION_HEAD_COMBINED_COMPARISON_PASS",
  "state_only": {
    "rows": 64,
    "overall_mae": 0.34351685643196106,
    "overall_rmse": 0.5353509187698364,
    "per_dim_mae": {
      "vx": 0.6321017146110535,
      "vy": 0.5615947842597961,
      "vz": 0.12193899601697922,
      "yaw_rate": 0.058432381600141525
    },
    "per_dim_rmse": {
      "vx": 0.7886570692062378,
      "vy": 0.7038221955299377,
      "vz": 0.14976152777671814,
      "yaw_rate": 0.08141595125198364
    }
  },
  "frozen_openvla_plus_state": {
    "rows": 64,
    "overall_mae": 0.3780280351638794,
    "overall_rmse": 0.5605542659759521,
    "per_dim_mae": {
      "vx": 0.6387233138084412,
      "vy": 0.6544771790504456,
      "vz": 0.12094108760356903,
      "yaw_rate": 0.09797053784132004
    },
    "per_dim_rmse": {
      "vx": 0.7514405846595764,
      "vy": 0.8074748516082764,
      "vz": 0.15742826461791992,
      "yaw_rate": 0.12418647110462189
    }
  },
  "plots": {
    "per_dim": "data/debug/plots/combined/combined_per_dim_error_bar.png",
    "overall": "data/debug/plots/combined/combined_overall_error_bar.png",
    "difference": "data/debug/plots/combined/combined_error_difference_bar.png"
  }
}
```

## Interpretation

Positive values in the error-difference plot mean the frozen OpenVLA + state model has higher error than the state-only baseline.

This pilot comparison should be interpreted as an engineering-stage result, not final thesis performance.