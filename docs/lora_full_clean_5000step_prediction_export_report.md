# LoRA 100-Step UAV Prediction Export Report

```json
{
  "status": "LORA_UAV_PREDICTION_EXPORT_PASS",
  "jsonl": "data/processed/full_clean_val_timestamp.jsonl",
  "rows": 4325,
  "out": "data/debug/predictions/lora_full_clean_5000step_val_predictions.jsonl",
  "lora_adapter": "checkpoints/lora_full/uav_lora_full_clean_5000step/lora_adapter",
  "action_head": "checkpoints/lora_full/uav_lora_full_clean_5000step/uav_action_head.pt",
  "metrics": {
    "overall_mae": 0.3492880165576935,
    "overall_rmse": 0.5066825151443481,
    "per_dim_mae": {
      "vx": 0.6696819067001343,
      "vy": 0.5706051588058472,
      "vz": 0.09778779000043869,
      "yaw_rate": 0.059081438928842545
    },
    "per_dim_rmse": {
      "vx": 0.7366259694099426,
      "vy": 0.6620259881019592,
      "vz": 0.18530778586864471,
      "yaw_rate": 0.10803883522748947
    }
  },
  "cuda_max_memory_gb": 14.465,
  "full_training_started": false,
  "closed_loop_eval_started": false
}
```
