# Formal Clean 5000-Step Result Interpretation

## Main Finding

The full clean timestamp LoRA 5000-step run achieves the best overall action_chunk prediction error on the full clean validation set.

Compared with state-only and frozen OpenVLA baselines, the LoRA-adapted OpenVLA model shows clear overall improvement.

## Per-Dimension Finding

The improvement is not uniform across action dimensions.

- vx: strong improvement
- yaw_rate: strong improvement
- vy: worse than baseline
- vz: worse than baseline

## Interpretation

This suggests that OpenVLA visual-language representations, when adapted with LoRA and a UAV action head, can transfer to UAV continuous action prediction.

However, the current model still has dimension-specific weaknesses. The vy and vz errors indicate that the action space is not yet balanced and may require:

- action normalization
- per-dimension loss weighting
- more diverse timestamp-clean trajectories
- better train/val map balancing
- longer training after data balancing

## Thesis-Usable Claim

This result supports the feasibility of OpenVLA-OFT-style cross-embodiment transfer from robot VLA models to UAV simulated visual-language navigation.

It should not yet be claimed as final closed-loop navigation performance.

## Not Included

- No closed-loop simulation
- No RL expert trajectory generation
- No Diffusion Policy training
- No official OpenVLA-OFT RLDS full finetuning
