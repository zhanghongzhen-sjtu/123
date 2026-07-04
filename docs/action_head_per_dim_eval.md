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
    "overall_mae": 0.34351685643196106,
    "overall_rmse": 0.5353508591651917,
    "per_dim_mae": {
      "vx": 0.6321014165878296,
      "vy": 0.5615946054458618,
      "vz": 0.12193897366523743,
      "yaw_rate": 0.05843236297369003
    },
    "per_dim_rmse": {
      "vx": 0.7886570692062378,
      "vy": 0.7038219571113586,
      "vz": 0.14976151287555695,
      "yaw_rate": 0.08141594380140305
    },
    "rows": 64
  },
  "frozen_openvla_plus_state": {
    "overall_mae": 0.3780280351638794,
    "overall_rmse": 0.5605542659759521,
    "per_dim_mae": {
      "vx": 0.6387233734130859,
      "vy": 0.6544771194458008,
      "vz": 0.12094108015298843,
      "yaw_rate": 0.09797054529190063
    },
    "per_dim_rmse": {
      "vx": 0.7514405846595764,
      "vy": 0.8074747920036316,
      "vz": 0.1574282944202423,
      "yaw_rate": 0.12418647110462189
    },
    "rows": 64,
    "feature_source": "openvla_last_hidden_state"
  },
  "lora_oft_started": false,
  "full_training_started": false,
  "closed_loop_eval_started": false
}
```