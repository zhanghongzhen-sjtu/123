# Frozen OpenVLA Normalized UAV Action Head Report

```json
{
  "status": "FROZEN_OPENVLA_NORMALIZED_UAV_ACTION_HEAD_PASS",
  "openvla_frozen": true,
  "trained_component": "uav_action_head_only",
  "lora_oft_started": false,
  "full_training_started": false,
  "closed_loop_eval_started": false,
  "model_id": "openvla/openvla-7b",
  "feature_source": "openvla_last_hidden_state",
  "train_rows": 120,
  "val_rows": 64,
  "stats": "data/processed/clean_train_action_stats.json",
  "initial_val": {
    "overall_mae": 0.3229137063026428,
    "overall_rmse": 0.5011511445045471,
    "per_dim_mae": {
      "vx": 0.674026608467102,
      "vy": 0.47008535265922546,
      "vz": 0.12481004744768143,
      "yaw_rate": 0.022732743993401527
    },
    "per_dim_rmse": {
      "vx": 0.7783002257347107,
      "vy": 0.6144441366195679,
      "vz": 0.1353510022163391,
      "yaw_rate": 0.054747454822063446
    },
    "normalized_loss": 0.41458379616960883,
    "batches": 64,
    "feature_source": "openvla_last_hidden_state"
  },
  "history": [
    {
      "epoch": 1,
      "train_normalized_loss": 0.2899120177142322,
      "val_normalized_loss": 0.5744378187227994,
      "val_overall_mae": 0.4341130554676056,
      "val_overall_rmse": 0.6808276772499084,
      "val_per_dim_mae": {
        "vx": 0.9028321504592896,
        "vy": 0.6921473741531372,
        "vz": 0.11780799925327301,
        "yaw_rate": 0.0236646868288517
      },
      "val_per_dim_rmse": {
        "vx": 1.0366190671920776,
        "vy": 0.8623064160346985,
        "vz": 0.18141323328018188,
        "yaw_rate": 0.05516466498374939
      },
      "train_steps": 120,
      "val_batches": 64
    },
    {
      "epoch": 2,
      "train_normalized_loss": 0.1527323701729377,
      "val_normalized_loss": 0.5717788126785308,
      "val_overall_mae": 0.43687573075294495,
      "val_overall_rmse": 0.6695227026939392,
      "val_per_dim_mae": {
        "vx": 0.8344354033470154,
        "vy": 0.742729902267456,
        "vz": 0.14680059254169464,
        "yaw_rate": 0.02353702113032341
      },
      "val_per_dim_rmse": {
        "vx": 0.9740580320358276,
        "vy": 0.9012884497642517,
        "vz": 0.16997665166854858,
        "yaw_rate": 0.05514098331332207
      },
      "train_steps": 120,
      "val_batches": 64
    },
    {
      "epoch": 3,
      "train_normalized_loss": 0.0978598068477974,
      "val_normalized_loss": 0.5191776286810637,
      "val_overall_mae": 0.39153972268104553,
      "val_overall_rmse": 0.5964946746826172,
      "val_per_dim_mae": {
        "vx": 0.6930934190750122,
        "vy": 0.6794859170913696,
        "vz": 0.16956335306167603,
        "yaw_rate": 0.02401629649102688
      },
      "val_per_dim_rmse": {
        "vx": 0.8345286250114441,
        "vy": 0.8301041722297668,
        "vz": 0.18619626760482788,
        "yaw_rate": 0.055167317390441895
      },
      "train_steps": 120,
      "val_batches": 64
    }
  ],
  "checkpoint": "checkpoints/uav_action_head/frozen_openvla_uav_action_head_normalized.pt",
  "cuda_max_memory_gb": 14.457
}
```
