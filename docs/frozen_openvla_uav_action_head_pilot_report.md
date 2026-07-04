# Frozen OpenVLA UAV Action-Head Pilot Report

```json
{
  "status": "FROZEN_OPENVLA_UAV_ACTION_HEAD_PILOT_PASS",
  "openvla_frozen": true,
  "trained_component": "uav_action_head_only",
  "lora_oft_started": false,
  "full_training_started": false,
  "closed_loop_eval_started": false,
  "model_id": "openvla/openvla-7b",
  "feature_source": "openvla_last_hidden_state",
  "train_rows": 120,
  "val_rows": 64,
  "batch_size": 1,
  "epochs": 3,
  "lr": 0.0001,
  "initial_val_loss": 0.2424526154063642,
  "history": [
    {
      "epoch": 1,
      "train_loss": 0.09250917481258511,
      "val_loss": 0.5789309311658144,
      "train_steps": 120,
      "val_batches": 32
    },
    {
      "epoch": 2,
      "train_loss": 0.03364898378786165,
      "val_loss": 0.5619590431451797,
      "train_steps": 120,
      "val_batches": 32
    },
    {
      "epoch": 3,
      "train_loss": 0.01544018703183004,
      "val_loss": 0.3945161923766136,
      "train_steps": 120,
      "val_batches": 32
    }
  ],
  "checkpoint": "checkpoints/uav_action_head/frozen_openvla_uav_action_head_pilot.pt",
  "cuda_max_memory_gb": 14.457
}
```
