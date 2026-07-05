# LoRA 100-Step UAV Prediction Export Report

```json
{
  "status": "LORA_UAV_PREDICTION_EXPORT_PASS",
  "jsonl": "data/processed/clean_val_timestamp_maps.jsonl",
  "rows": 64,
  "out": "data/debug/predictions/lora_500step_val_predictions.jsonl",
  "lora_adapter": "checkpoints/lora_pilot/uav_lora_500step/lora_adapter",
  "action_head": "checkpoints/lora_pilot/uav_lora_500step/uav_action_head.pt",
  "metrics": {
    "overall_mae": 0.3376010060310364,
    "overall_rmse": 0.5192945599555969,
    "per_dim_mae": {
      "vx": 0.6556137800216675,
      "vy": 0.5294370055198669,
      "vz": 0.09863714873790741,
      "yaw_rate": 0.06671608984470367
    },
    "per_dim_rmse": {
      "vx": 0.7674256563186646,
      "vy": 0.6816980838775635,
      "vz": 0.13076762855052948,
      "yaw_rate": 0.08895506709814072
    }
  },
  "cuda_max_memory_gb": 14.456,
  "full_training_started": false,
  "closed_loop_eval_started": false
}
```
