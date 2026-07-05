# TravelUAV Simulator Env Contract Report

```json
{
  "status": "TRAVELUAV_SIMULATOR_ENV_CONTRACT_PASS",
  "jsonl": "data/processed/full_clean_val_timestamp.jsonl",
  "max_rows": 1000,
  "missing_backend_guard_ok": true,
  "reward_sanity_ok": true,
  "reward_toward": 0.91,
  "reward_away": -1.13,
  "replay_episodes": 5,
  "replay_steps": 229,
  "reward_mean": 2.5711441560603525,
  "reward_min": -2.2529571533203123,
  "reward_max": 14.94983721524477,
  "distance_mean": 106.32801095679338,
  "real_simulator_started": false,
  "ppo_training_started": false,
  "openvla_training_started": false
}
```

## Interpretation

This validates the interface contract for replacing the toy PPO environment with a real TravelUAV simulator backend.

The replay environment is only for interface and reward sanity checks. It must not be treated as interactive PPO training.
