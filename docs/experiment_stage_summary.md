# Experiment Stage Summary

## Current Research Goal

Study OpenVLA-OFT transfer for UAV simulation visual-language-action navigation.

The target UAV interface is:

- state: `[x, y, z, yaw]`
- action: `[vx, vy, vz, yaw_rate]`
- action_chunk: `[8, 4]`

## Completed Engineering Pipeline

1. TravelUAV real subset downloaded and parsed.
2. TravelUAV trajectories converted to OpenVLA-style UAV JSONL.
3. JSONL format, image paths, instruction strings, state/action/action_chunk were validated.
4. Clean timestamp train/val split was created.
5. OpenVLA-OFT collator contract was inspected.
6. UAV dimensions were mapped:
   - `ACTION_DIM = 4`
   - `PROPRIO_DIM = 4`
   - `NUM_ACTIONS_CHUNK = 8`
7. OpenVLA processor smoke passed.
8. OpenVLA one-batch forward smoke passed.
9. UAVJsonlDatasetForOpenVLAOFT dry run passed.
10. Frozen OpenVLA + UAV action head pilot training passed.
11. State-only baseline and per-dimension evaluation were completed.

## Pilot Results

### State-Only Baseline

Unnormalized:

- overall MAE: 0.3269
- overall RMSE: 0.5125

Normalized:

- overall MAE: 0.3173
- overall RMSE: 0.5141

### Frozen OpenVLA + UAV State

Unnormalized:

- overall MAE: 0.3783
- overall RMSE: 0.5667

Normalized:

- overall MAE: 0.4397
- overall RMSE: 0.6436

## Interpretation

The frozen OpenVLA feature path is technically feasible:

- OpenVLA can process TravelUAV images and instructions.
- UAV state can be concatenated as proprio.
- UAV action_chunk can be trained as a continuous target.
- The action head loss can decrease.

However, in the current small pilot setting, frozen OpenVLA features do not outperform the state-only baseline.

This suggests that direct frozen feature reuse is not enough for UAV cross-embodiment transfer.

## Main Bottleneck

The largest prediction errors are in horizontal velocity:

- `vx`
- `vy`

The easier dimensions are:

- `vz`
- `yaw_rate`

## Research Implication

The project should not claim that OpenVLA transfer already improves UAV action prediction.

A stronger next-stage method is needed:

1. better action normalization;
2. more TravelUAV maps;
3. improved visual-language feature extraction;
4. LoRA/OFT adaptation;
5. Diffusion Policy for action-sequence generation;
6. RL expert trajectories for better supervision.

## Current Stage Conclusion

The project has completed the first meaningful feasibility gate:

- data route works;
- OpenVLA model route works;
- UAV action head route works;
- baseline comparison exists.

But it is not final training and not final evaluation.
