# Per-Horizon Result Interpretation

## Main Finding

The LoRA full clean 5000-step model achieves the lowest overall MAE across all 8 action_chunk horizon steps.

This indicates that the OpenVLA+LoRA UAV action head does not only improve immediate action prediction, but also improves short-horizon action sequence prediction.

## Dimension-Level Finding

The improvement is dimension-dependent.

- vx: LoRA is consistently and substantially better than state-only and frozen OpenVLA across all horizons.
- yaw_rate: LoRA is generally better than baselines across most horizons.
- vy: LoRA is worse than baselines across horizons, indicating lateral velocity remains the main weakness.
- vz: LoRA shows mixed behavior, with some horizons worse and later horizons partially improved.

## Interpretation

The per-horizon result supports the usefulness of OpenVLA representation transfer for UAV action_chunk prediction.

However, the dimension-level analysis also shows that direct MLP action head prediction is not sufficient for all UAV control dimensions.

This motivates future use of Diffusion Policy as a sequence-level control module to better model action coupling and smooth multi-step control.

## Thesis Usage

This analysis can be used as evidence for:

1. open-loop VLA-to-UAV action prediction feasibility;
2. action_chunk-level prediction improvement;
3. motivation for adding Diffusion Policy in the next stage.

