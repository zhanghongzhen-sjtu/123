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
  "initial_val_loss": 0.11951119499281049,
  "history": [
    {
      "epoch": 1,
      "train_loss": 0.11613869816064834,
      "val_loss": 0.11793208355084062,
      "train_steps": 120,
      "val_batches": 64
    },
    {
      "epoch": 2,
      "train_loss": 0.10170291638933122,
      "val_loss": 0.1243434154894203,
      "train_steps": 120,
      "val_batches": 64
    },
    {
      "epoch": 3,
      "train_loss": 0.09472371832622836,
      "val_loss": 0.1305138526367955,
      "train_steps": 120,
      "val_batches": 64
    }
  ],
  "checkpoint": "checkpoints/uav_action_head/state_only_action_head_baseline.pt",
  "cuda_max_memory_gb": 0.018
}
```
