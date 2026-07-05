# LoRA 100-Step UAV Prediction Export Report

```json
{
  "status": "LORA_UAV_PREDICTION_EXPORT_PASS",
  "jsonl": "data/processed/clean_val_timestamp_maps.jsonl",
  "rows": 64,
  "out": "data/debug/predictions/lora_100step_val_predictions.jsonl",
  "lora_adapter": "checkpoints/lora_pilot/uav_lora_100step/lora_adapter",
  "action_head": "checkpoints/lora_pilot/uav_lora_100step/uav_action_head.pt",
  "metrics": {
    "overall_mae": 0.3800496757030487,
    "overall_rmse": 0.5646526217460632,
    "per_dim_mae": {
      "vx": 0.7776318788528442,
      "vy": 0.528260350227356,
      "vz": 0.1376183182001114,
      "yaw_rate": 0.07668785005807877
    },
    "per_dim_rmse": {
      "vx": 0.8851950764656067,
      "vy": 0.6744604706764221,
      "vz": 0.16560935974121094,
      "yaw_rate": 0.09714081883430481
    }
  },
  "cuda_max_memory_gb": 14.456,
  "full_training_started": false,
  "closed_loop_eval_started": false
}
```
