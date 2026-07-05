# LoRA 100-Step UAV Prediction Export Report

```json
{
  "status": "LORA_UAV_PREDICTION_EXPORT_PASS",
  "jsonl": "data/processed/full_clean_val_timestamp.jsonl",
  "rows": 4325,
  "out": "data/debug/predictions/lora_weighted_full_clean_5000step_val_predictions.jsonl",
  "lora_adapter": "checkpoints/lora_weighted/uav_lora_weighted_full_clean_5000step/lora_adapter",
  "action_head": "checkpoints/lora_weighted/uav_lora_weighted_full_clean_5000step/uav_action_head.pt",
  "metrics": {
    "overall_mae": 0.35823026299476624,
    "overall_rmse": 0.5166113376617432,
    "per_dim_mae": {
      "vx": 0.6714833378791809,
      "vy": 0.5835656523704529,
      "vz": 0.10188288986682892,
      "yaw_rate": 0.07598771899938583
    },
    "per_dim_rmse": {
      "vx": 0.7418848872184753,
      "vy": 0.6830219030380249,
      "vz": 0.18918529152870178,
      "yaw_rate": 0.1218341514468193
    }
  },
  "cuda_max_memory_gb": 14.465,
  "full_training_started": false,
  "closed_loop_eval_started": false
}
```
