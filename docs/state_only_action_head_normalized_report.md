# State-Only Normalized Action Head Report

```json
{
  "status": "STATE_ONLY_NORMALIZED_ACTION_HEAD_PASS",
  "train_rows": 120,
  "val_rows": 64,
  "stats": "data/processed/clean_train_action_stats.json",
  "initial_val": {
    "overall_mae": 0.3265121877193451,
    "overall_rmse": 0.5016598105430603,
    "per_dim_mae": {
      "vx": 0.6866856217384338,
      "vy": 0.46141746640205383,
      "vz": 0.13505704700946808,
      "yaw_rate": 0.022888708859682083
    },
    "per_dim_rmse": {
      "vx": 0.7910274863243103,
      "vy": 0.5978490710258484,
      "vz": 0.14315520226955414,
      "yaw_rate": 0.05485185235738754
    },
    "normalized_loss": 0.41679680766537786
  },
  "history": [
    {
      "epoch": 1,
      "train_normalized_loss": 0.3219137458751599,
      "val_normalized_loss": 0.4281207504682243,
      "val_overall_mae": 0.3329026699066162,
      "val_overall_rmse": 0.513624906539917,
      "val_per_dim_mae": {
        "vx": 0.6880909204483032,
        "vy": 0.4771798849105835,
        "vz": 0.1435016393661499,
        "yaw_rate": 0.022838126868009567
      },
      "val_per_dim_rmse": {
        "vx": 0.8041296005249023,
        "vy": 0.6182941794395447,
        "vz": 0.15274882316589355,
        "yaw_rate": 0.054752450436353683
      }
    },
    {
      "epoch": 2,
      "train_normalized_loss": 0.29575906582176686,
      "val_normalized_loss": 0.43506208760663867,
      "val_overall_mae": 0.33269694447517395,
      "val_overall_rmse": 0.5239101648330688,
      "val_per_dim_mae": {
        "vx": 0.6712395548820496,
        "vy": 0.49171730875968933,
        "vz": 0.1450689733028412,
        "yaw_rate": 0.022762000560760498
      },
      "val_per_dim_rmse": {
        "vx": 0.8148365616798401,
        "vy": 0.637353777885437,
        "vz": 0.1573251485824585,
        "yaw_rate": 0.054750725626945496
      }
    },
    {
      "epoch": 3,
      "train_normalized_loss": 0.2815242792945355,
      "val_normalized_loss": 0.4431982699315995,
      "val_overall_mae": 0.3384249210357666,
      "val_overall_rmse": 0.5396386981010437,
      "val_per_dim_mae": {
        "vx": 0.6972020864486694,
        "vy": 0.49460020661354065,
        "vz": 0.13912901282310486,
        "yaw_rate": 0.022768430411815643
      },
      "val_per_dim_rmse": {
        "vx": 0.8522350788116455,
        "vy": 0.6416988372802734,
        "vz": 0.15415772795677185,
        "yaw_rate": 0.05470767989754677
      }
    }
  ],
  "checkpoint": "checkpoints/uav_action_head/state_only_action_head_normalized.pt",
  "cuda_max_memory_gb": 0.018
}
```
