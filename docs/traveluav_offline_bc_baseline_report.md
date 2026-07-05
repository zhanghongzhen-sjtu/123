# TravelUAV Offline BC Baseline Report

## Status

- `OFFLINE_TRAVELUAV_SUPERVISED_DATA_PASS`
- `OFFLINE_TRAIN_VAL_SPLIT_PASS`
- `BC_FULL_PASS`
- `REAL_AIRSIM_ROLLOUT_NOT_INCLUDED`
- `OPENVLA_TRAINING_NOT_STARTED`
- `LORA_OFT_TRAINING_NOT_STARTED`
- `DIFFUSION_POLICY_TRAINING_NOT_STARTED`

## Data

- Train JSONL: `data/offline/splits/traveluav_offline_supervised_train.jsonl`
- Val JSONL: `data/offline/splits/traveluav_offline_supervised_val.jsonl`
- Train rows: `298304`
- Val rows: `31898`
- Maps: `11`
- Split: `episode_level`, seed `42`

## Model

- Model: MLP state-to-action baseline
- Input: `state = [x, y, z, yaw]`
- Output: `action = [vx, vy, vz, yaw_rate]`
- Training target: normalized action MSE
- Device: `cuda`
- Last checkpoint: `checkpoints/bc/traveluav_state_action_mlp_split_full.pt`
- Best checkpoint: `checkpoints/bc/traveluav_state_action_mlp_split_full_best.pt`

## Result

- Best epoch: `19`
- Best val normalized MSE: `0.587646`
- Last train normalized MSE: `0.541670`
- Last val normalized MSE: `0.587739`

Last validation action MAE:

- `vx`: `0.679630`
- `vy`: `0.644029`
- `vz`: `0.528502`
- `yaw_rate`: `0.074638`

## Normalization

State normalization from train split:

- mean: `[-18.905053307846526, -9.218444023294397, -44.1944408721605, 0.030553939216945568]`
- std: `[414.245949944548, 349.82276865430384, 55.44835288893365, 1.8103936693962572]`

Action normalization from train split:

- mean: `[0.030983938966805485, 0.033613208537051145, -0.03417930897020924, -0.0014431375014761286]`
- std: `[2.5383467891622913, 2.4182272217504934, 1.1514942832537325, 0.2809096015174054]`

## Boundary

This is an offline supervised behavior-cloning baseline using existing TravelUAV logged trajectories. It does not include online AirSim rollout, collision feedback, simulator reset, PPO/SAC interaction, OpenVLA training, LoRA/OFT, or Diffusion Policy training.

Real TravelUAV/AirSim expert trajectory generation still requires the local Windows RTX 3060 simulator path to launch successfully.
