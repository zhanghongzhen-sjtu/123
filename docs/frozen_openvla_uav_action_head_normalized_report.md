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
    "overall_mae": 0.32422834634780884,
    "overall_rmse": 0.5017383098602295,
    "per_dim_mae": {
      "vx": 0.6773396134376526,
      "vy": 0.47289738059043884,
      "vz": 0.12389514595270157,
      "yaw_rate": 0.022781144827604294
    },
    "per_dim_rmse": {
      "vx": 0.7804794311523438,
      "vy": 0.6139996647834778,
      "vz": 0.13348700106143951,
      "yaw_rate": 0.05479783937335014
    },
    "normalized_loss": 0.41523234685882926,
    "batches": 64,
    "feature_source": "openvla_last_hidden_state"
  },
  "history": [
    {
      "epoch": 1,
      "train_normalized_loss": 0.29394298971941074,
      "val_normalized_loss": 0.5529828290455043,
      "val_overall_mae": 0.4178415536880493,
      "val_overall_rmse": 0.6514674425125122,
      "val_per_dim_mae": {
        "vx": 0.7236107587814331,
        "vy": 0.7892531752586365,
        "vz": 0.13492196798324585,
        "yaw_rate": 0.023580439388751984
      },
      "val_per_dim_rmse": {
        "vx": 0.8650867342948914,
        "vy": 0.9597964286804199,
        "vz": 0.15817216038703918,
        "yaw_rate": 0.05510897561907768
      },
      "train_steps": 120,
      "val_batches": 64
    },
    {
      "epoch": 2,
      "train_normalized_loss": 0.16426537084626033,
      "val_normalized_loss": 0.6177552798762918,
      "val_overall_mae": 0.4772813618183136,
      "val_overall_rmse": 0.7094748020172119,
      "val_per_dim_mae": {
        "vx": 0.9549887180328369,
        "vy": 0.7596538066864014,
        "vz": 0.1706051230430603,
        "yaw_rate": 0.023877747356891632
      },
      "val_per_dim_rmse": {
        "vx": 1.0757402181625366,
        "vy": 0.9045524001121521,
        "vz": 0.18696363270282745,
        "yaw_rate": 0.05504859238862991
      },
      "train_steps": 120,
      "val_batches": 64
    },
    {
      "epoch": 3,
      "train_normalized_loss": 0.10616876421748506,
      "val_normalized_loss": 0.5910661164671183,
      "val_overall_mae": 0.4397362172603607,
      "val_overall_rmse": 0.6435747742652893,
      "val_per_dim_mae": {
        "vx": 0.778316855430603,
        "vy": 0.7186950445175171,
        "vz": 0.23781231045722961,
        "yaw_rate": 0.024120740592479706
      },
      "val_per_dim_rmse": {
        "vx": 0.9154921174049377,
        "vy": 0.8670238852500916,
        "vz": 0.2527293562889099,
        "yaw_rate": 0.055005718022584915
      },
      "train_steps": 120,
      "val_batches": 64
    }
  ],
  "checkpoint": "checkpoints/uav_action_head/frozen_openvla_uav_action_head_normalized.pt",
  "cuda_max_memory_gb": 14.459
}
```
