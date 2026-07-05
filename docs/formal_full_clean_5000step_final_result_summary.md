# Formal Full Clean 5000-Step Final Result Summary

## Result Status

This is the current thesis-usable result for the VLA-UAV transfer experiment.

The comparison is conducted on the same full clean timestamp validation set.

## Models Compared

- state_only
- frozen_openvla
- lora_full_5000step

## Main Conclusion

The LoRA-adapted OpenVLA model achieves the best overall action_chunk prediction performance.

This supports the feasibility of transferring a robot VLA backbone to UAV continuous action prediction through LoRA and a UAV-specific action head.

## Dimension-Level Observation

The improvement is dimension-dependent.

- vx: LoRA improves strongly.
- yaw_rate: LoRA improves strongly.
- vy: LoRA is worse than baselines.
- vz: LoRA is worse than baselines.

## Interpretation

The result shows that OpenVLA visual-language features can provide useful transfer for UAV motion prediction, especially forward velocity and yaw control.

However, lateral and vertical velocity prediction still require further improvement. This motivates later work on action normalization, per-dimension loss weighting, balanced sampling, and possibly Diffusion Policy for smoother multi-step control.

## Thesis Claim Boundary

This result supports data-driven VLA-to-UAV action transfer.

It does not yet prove closed-loop navigation success.

Not included:

- closed-loop simulator evaluation
- RL expert trajectory generation
- Diffusion Policy training
- official OpenVLA-OFT RLDS full finetuning
