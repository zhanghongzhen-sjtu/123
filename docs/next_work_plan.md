# Next Work Plan

## Stop Current Branch

Do not continue long action-head training now.

Reason:

- frozen OpenVLA action head is feasible but underperforms state-only baseline;
- more training without method changes is unlikely to answer the main research question.

## Next Engineering Work

1. Clean up code and reports.
2. Package current results.
3. Prepare a reproducible experiment table.
4. Decide which maps are clean timestamp and which require dt repair.
5. Add trajectory-level visualization for predictions.

## Next Research Work

### Stage 1: Robust Baseline

Improve state-only and trajectory baselines:

- state-only MLP;
- normalized action head;
- per-dimension metrics;
- trajectory rollout visualization.

### Stage 2: OpenVLA Transfer

Improve OpenVLA transfer:

- use better hidden states;
- use action-token hidden states instead of last token;
- test LoRA/OFT tiny smoke;
- compare frozen vs adapted OpenVLA.

### Stage 3: Diffusion Policy

Use Diffusion Policy for control sequence prediction:

- input: OpenVLA/UAV features + state;
- output: action sequence;
- target: smooth UAV control.

### Stage 4: RL Expert Trajectories

Use RL to generate or refine expert trajectories:

- improve action supervision;
- support closed-loop evaluation;
- compare imitation-only vs RL-enhanced supervision.

## Next Immediate Deliverable

Write a thesis method draft and experiment section based on current pilot findings.
