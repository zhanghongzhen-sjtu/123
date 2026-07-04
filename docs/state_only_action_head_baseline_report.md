# State-Only Action Head Baseline Report

```json
{
  "status": "STATE_ONLY_ACTION_HEAD_BASELINE_PASS",
  "model": "state_only_mlp",
  "train_rows": 120,
  "val_rows": 64,
  "batch_size": 1,
  "epochs": 3,
  "lr": 0.0001,
  "initial_val_loss": 0.12694853299763054,
  "history": [
    {
      "epoch": 1,
      "train_loss": 0.11538908102860053,
      "val_loss": 0.12596249440684915,
      "train_steps": 120,
      "val_batches": 64
    },
    {
      "epoch": 2,
      "train_loss": 0.10182837111254534,
      "val_loss": 0.13063451973721385,
      "train_steps": 120,
      "val_batches": 64
    },
    {
      "epoch": 3,
      "train_loss": 0.09465585958678276,
      "val_loss": 0.14117807080037892,
      "train_steps": 120,
      "val_batches": 64
    }
  ],
  "checkpoint": "checkpoints/uav_action_head/state_only_action_head_baseline.pt",
  "cuda_max_memory_gb": 0.018
}
```
