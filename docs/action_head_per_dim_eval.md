# Action Head Per-Dimension Evaluation

## Status

- ACTION_HEAD_PER_DIM_EVAL_PASS
- LORA_OFT_NOT_STARTED
- FULL_TRAINING_NOT_STARTED
- CLOSED_LOOP_EVAL_NOT_STARTED

## Result

```json
{
  "status": "ACTION_HEAD_PER_DIM_EVAL_PASS",
  "val_jsonl": "data/processed/clean_val_timestamp_maps.jsonl",
  "max_rows": 64,
  "state_only": {
    "overall_mae": 0.3268895447254181,
    "overall_rmse": 0.5124872922897339,
    "per_dim_mae": {
      "vx": 0.5746629238128662,
      "vy": 0.541178822517395,
      "vz": 0.12612277269363403,
      "yaw_rate": 0.06559378653764725
    },
    "per_dim_rmse": {
      "vx": 0.7331687808036804,
      "vy": 0.6932064890861511,
      "vz": 0.15776298940181732,
      "yaw_rate": 0.08724750578403473
    },
    "rows": 64
  },
  "frozen_openvla_plus_state": {
    "overall_mae": 0.3783036172389984,
    "overall_rmse": 0.5667319893836975,
    "per_dim_mae": {
      "vx": 0.6335176229476929,
      "vy": 0.6503187417984009,
      "vz": 0.12680014967918396,
      "yaw_rate": 0.10257796198129654
    },
    "per_dim_rmse": {
      "vx": 0.7674236297607422,
      "vy": 0.8066933751106262,
      "vz": 0.16505597531795502,
      "yaw_rate": 0.13343091309070587
    },
    "rows": 64,
    "feature_source": "openvla_last_hidden_state"
  },
  "lora_oft_started": false,
  "full_training_started": false,
  "closed_loop_eval_started": false
}
```