# Pilot Visualization Summary

## Status

- PILOT_PIPELINE_PASS
- STATE_ONLY_PLOTS_READY
- FROZEN_OPENVLA_PLOTS_READY
- COMBINED_COMPARISON_PLOTS_READY
- TRAJECTORY_ROLLOUT_PLOTS_READY

## Prediction Plots

State-only plots:

- `data/debug/plots/state_only/`

Frozen OpenVLA plots:

- `data/debug/plots/frozen_openvla/`

Combined comparison plots:

- `data/debug/plots/combined/`

Trajectory rollout plots:

- `data/debug/plots/trajectory/`

## Interpretation

The plots show that the largest action prediction errors occur in horizontal velocity dimensions:

- `vx`
- `vy`

The state-only baseline currently performs better than frozen OpenVLA + UAV state in this pilot setting.

This does not invalidate the OpenVLA transfer direction. It shows that direct frozen feature reuse is insufficient and motivates:

- better feature selection;
- LoRA/OFT adaptation;
- larger and cleaner data;
- Diffusion Policy sequence prediction;
- RL expert trajectory generation.

## Warning

The plotted action curves flatten validation samples and action chunks. Discontinuities may occur at sample or episode boundaries.

Trajectory rollout plots are open-loop action-chunk rollouts, not closed-loop simulator evaluation.
