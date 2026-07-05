# LoRA 100-Step UAV Prediction Export Report

```json
{
  "status": "LORA_UAV_PREDICTION_EXPORT_PASS",
  "jsonl": "data/processed/full_clean_val_timestamp_body.jsonl",
  "rows": 4325,
  "out": "data/debug/predictions/lora_body_full_clean_5000step_val_predictions.jsonl",
  "lora_adapter": "checkpoints/lora_body/uav_lora_body_full_clean_5000step/lora_adapter",
  "action_head": "checkpoints/lora_body/uav_lora_body_full_clean_5000step/uav_action_head.pt",
  "metrics": {
    "overall_mae": 0.33838364481925964,
    "overall_rmse": 0.603779137134552,
    "per_dim_mae": {
      "vx": 1.0318907499313354,
      "vy": 0.13938698172569275,
      "vz": 0.11900318413972855,
      "yaw_rate": 0.06325327605009079
    },
    "per_dim_rmse": {
      "vx": 1.1623982191085815,
      "vy": 0.2373243123292923,
      "vz": 0.19778616726398468,
      "yaw_rate": 0.10760116577148438
    }
  },
  "cuda_max_memory_gb": 14.465,
  "full_training_started": false,
  "closed_loop_eval_started": false
}
```
