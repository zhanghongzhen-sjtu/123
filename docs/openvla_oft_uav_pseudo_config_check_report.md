# OpenVLA-OFT UAV Pseudo Config Check Report

This report validates the local pseudo configuration only. It does not load OpenVLA-OFT, train, run LoRA/OFT, or run simulator evaluation.

## Config

- Config file: `configs/openvla_oft_uav_debug.yaml`
- Schema version: `uav_openvla_pseudo_config_v0.1`
- Status: `PSEUDO_CONFIG_PASS`

## Safety

- `training_enabled=false`
- `model_loading_enabled=false`
- `lora_oft_enabled=false`
- `closed_loop_eval_enabled=false`
- `simulator_enabled=false`
- `diffusion_policy_training_enabled=false`
- `rl_training_enabled=false`

## Dataset

- JSONL files: `['data/debug/traveluav_BrushifyCountryRoads_debug.jsonl']`
- Dataset summary: `{'rows': 60, 'maps': {'BrushifyCountryRoads': {'rows': 60, 'episodes': 3}}, 'action_chunk_lengths': {8: 60}, 'dt_sources': {'timestamp': 60}, 'normalized': True, 'stats_path': 'data/debug/traveluav_3maps_stats.json'}`
- Stats summary: `{'row_count': 174, 'dt_sources': {'timestamp': 174}, 'action_chunk_lengths': {'8': 174}}`

## Batch Shapes

- `{'states': [8, 4], 'actions': [8, 4], 'action_chunks': [8, 8, 4], 'dts': [8], 'states_normalized': [8, 4], 'actions_normalized': [8, 4], 'action_chunks_normalized': [8, 8, 4]}`

## 5090 Boundary

- future_5090 status: `planned_only_do_not_run_locally`
- Full train/val conversion, full normalization stats, model loading, action-head training, LoRA/OFT, closed-loop evaluation, Diffusion Policy training, and RL training are not local tasks.

## Final

- `PSEUDO_CONFIG_PASS`
- `NOT_TRAINING_READY`
