# State-Only Normalized Action Head Report

```json
{
  "status": "STATE_ONLY_NORMALIZED_ACTION_HEAD_PASS",
  "train_rows": 120,
  "val_rows": 64,
  "stats": "data/processed/clean_train_action_stats.json",
  "initial_val": {
    "overall_mae": 0.3156943619251251,
    "overall_rmse": 0.4899864196777344,
    "per_dim_mae": {
      "vx": 0.6775535941123962,
      "vy": 0.45003026723861694,
      "vz": 0.11213592439889908,
      "yaw_rate": 0.02305762842297554
    },
    "per_dim_rmse": {
      "vx": 0.7810952067375183,
      "vy": 0.5761008262634277,
      "vz": 0.12389510124921799,
      "yaw_rate": 0.054725177586078644
    },
    "normalized_loss": 0.40162186743691564
  },
  "history": [
    {
      "epoch": 1,
      "train_normalized_loss": 0.3229632094502449,
      "val_normalized_loss": 0.41789551824331284,
      "val_overall_mae": 0.3245514929294586,
      "val_overall_rmse": 0.5033162236213684,
      "val_per_dim_mae": {
        "vx": 0.6776200532913208,
        "vy": 0.46631622314453125,
        "vz": 0.13143634796142578,
        "yaw_rate": 0.02283323183655739
      },
      "val_per_dim_rmse": {
        "vx": 0.7894721031188965,
        "vy": 0.6050531268119812,
        "vz": 0.14476634562015533,
        "yaw_rate": 0.05473947525024414
      }
    },
    {
      "epoch": 2,
      "train_normalized_loss": 0.30094784007718167,
      "val_normalized_loss": 0.4190435572527349,
      "val_overall_mae": 0.31996726989746094,
      "val_overall_rmse": 0.5084277987480164,
      "val_per_dim_mae": {
        "vx": 0.6527864933013916,
        "vy": 0.4763450026512146,
        "vz": 0.12785781919956207,
        "yaw_rate": 0.022879697382450104
      },
      "val_per_dim_rmse": {
        "vx": 0.7887424230575562,
        "vy": 0.6231397986412048,
        "vz": 0.14343754947185516,
        "yaw_rate": 0.054800745099782944
      }
    },
    {
      "epoch": 3,
      "train_normalized_loss": 0.28315261979587375,
      "val_normalized_loss": 0.42071052780374885,
      "val_overall_mae": 0.31728091835975647,
      "val_overall_rmse": 0.5141318440437317,
      "val_per_dim_mae": {
        "vx": 0.6482284665107727,
        "vy": 0.47410836815834045,
        "vz": 0.1238776296377182,
        "yaw_rate": 0.02290917932987213
      },
      "val_per_dim_rmse": {
        "vx": 0.8032407164573669,
        "vy": 0.6235319375991821,
        "vz": 0.14259818196296692,
        "yaw_rate": 0.05481144040822983
      }
    }
  ],
  "checkpoint": "checkpoints/uav_action_head/state_only_action_head_normalized.pt",
  "cuda_max_memory_gb": 0.018
}
```
