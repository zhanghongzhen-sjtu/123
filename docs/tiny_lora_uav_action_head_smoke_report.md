# Tiny LoRA UAV Action-Head Smoke Report

```json
{
  "status": "TINY_LORA_UAV_ACTION_HEAD_SMOKE_PASS",
  "model_id": "openvla/openvla-7b",
  "feature_source": "openvla_last_hidden_state",
  "train_rows": 8,
  "batch_size": 1,
  "max_steps": 3,
  "losses": [
    0.12070686370134354,
    0.11401572078466415,
    0.10496032238006592
  ],
  "lora_rank": 8,
  "lora_dropout": 0.0,
  "saved_lora_adapter": "checkpoints/lora_smoke/tiny_lora_uav/lora_adapter",
  "saved_action_head": "checkpoints/lora_smoke/tiny_lora_uav/uav_action_head.pt",
  "full_training_started": false,
  "closed_loop_eval_started": false,
  "merged_full_model_saved": false,
  "cuda_max_memory_gb": 20.375
}
```
