# Stage 2 RL PPO Result Summary

## Status

- `PPO_SIMPLE_UAV_FULL_SMOKE_PASS`
- `NOT_REAL_TRAVELUAV_SIMULATOR_TRAINING`
- OpenVLA training started: `False`
- LoRA/OFT started: `False`
- Diffusion Policy training started: `False`

## Method

This stage validates the RL expert trajectory generation pipeline with PPO.

The current environment is a lightweight toy UAV point-navigation environment:

- state: `state=[x,y,z,yaw]`
- action: `action=[vx,vy,vz,yaw_rate]`
- algorithm: PPO
- purpose: validate RL rollout -> UAV JSONL -> action_chunk interface

## Training Result

- total timesteps: `500000`
- eval mean reward: `12.0146405625`
- eval std reward: `0.4305532445116355`
- model path: `checkpoints/rl/ppo_simple_uav_full/ppo_simple_uav.zip`

## Exported Expert Trajectories

- JSONL: `data/rl_debug/ppo_simple_uav_expert_full.jsonl`
- rows: `311`
- exported successful episodes: `32`
- attempted rollouts: `32`
- plot: `data/rl_debug/plots/ppo_simple_uav_full_paths.png`

## Interpretation

This result confirms that the second-stage reinforcement learning pipeline can produce expert UAV trajectories in the same action/action_chunk format used by the TravelUAV-to-OpenVLA-OFT data path.

It does not yet represent real TravelUAV simulator training. The next required step is to replace the toy point-mass environment with a real simulator wrapper exposing:

- `reset()`
- `step(action)`
- `observation`
- `reward`
- `done`
- simulator state/image/instruction fields

## Next Stage

To move from toy PPO to real simulator PPO/SAC:

1. Implement `TravelUAVSimulatorEnv`.
2. Define reward from distance-to-goal, collision, progress, altitude, smoothness, and success.
3. Validate random policy rollout.
4. Run short PPO smoke training.
5. Export real simulator expert trajectories.
6. Use those trajectories as expert data for VLA/Diffusion Policy stages.

