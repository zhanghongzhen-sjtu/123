# LoRA 100-Step UAV Prediction Export Report

```json
{
  "status": "LORA_UAV_PREDICTION_EXPORT_PASS",
  "jsonl": "data/processed/clean_val_timestamp_maps.jsonl",
  "rows": 64,
  "out": "data/debug/predictions/lora_1000step_val_predictions.jsonl",
  "lora_adapter": "checkpoints/lora_pilot/uav_lora_1000step/lora_adapter",
  "action_head": "checkpoints/lora_pilot/uav_lora_1000step/uav_action_head.pt",
  "metrics": {
    "overall_mae": 0.3169754445552826,
    "overall_rmse": 0.4988451302051544,
    "per_dim_mae": {
      "vx": 0.6681436896324158,
      "vy": 0.4718279540538788,
      "vz": 0.06245376914739609,
      "yaw_rate": 0.06547625362873077
    },
    "per_dim_rmse": {
      "vx": 0.775280237197876,
      "vy": 0.6134700775146484,
      "vz": 0.1029534712433815,
      "yaw_rate": 0.08591504395008087
    }
  },
  "cuda_max_memory_gb": 14.456,
  "full_training_started": false,
  "closed_loop_eval_started": false
}
```
