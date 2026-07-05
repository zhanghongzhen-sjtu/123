# State-Only Action Head Baseline Report

```json
{
  "status": "STATE_ONLY_ACTION_HEAD_BASELINE_PASS",
  "model": "state_only_mlp",
  "train_rows": 120,
  "val_rows": 64,
  "batch_size": 32,
  "epochs": 3,
  "lr": 0.001,
  "initial_val_loss": 0.11081687733530998,
  "history": [
    {
      "epoch": 1,
      "train_loss": 0.10786807723343372,
      "val_loss": 0.10884170979261398,
      "train_steps": 4,
      "val_batches": 2
    },
    {
      "epoch": 2,
      "train_loss": 0.08118205890059471,
      "val_loss": 0.10831954330205917,
      "train_steps": 4,
      "val_batches": 2
    },
    {
      "epoch": 3,
      "train_loss": 0.05838762689381838,
      "val_loss": 0.10997169464826584,
      "train_steps": 4,
      "val_batches": 2
    }
  ],
  "checkpoint": "checkpoints/lora_body/state_only_body_full_clean.pt",
  "cuda_max_memory_gb": 0.017
}
```
