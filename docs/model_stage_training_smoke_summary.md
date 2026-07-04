# Model Stage Training Smoke Summary

## Status

- MODEL_STAGE_CONFIRMED_BY_USER
- OPENVLA_PROCESSOR_SMOKE_PASS
- OPENVLA_REAL_PROCESSOR_COLLATOR_SMOKE_PASS
- OPENVLA_ONE_BATCH_FORWARD_SMOKE_PASS
- TINY_UAV_ACTION_HEAD_TRAINING_SMOKE_PASS
- OPENVLA_FROZEN
- LORA_OFT_NOT_STARTED
- FULL_TRAINING_NOT_STARTED
- CLOSED_LOOP_EVAL_NOT_STARTED

## Tiny UAV Action-Head Smoke Result

Settings:

- model: `openvla/openvla-7b`
- OpenVLA backbone: frozen
- trained component: tiny UAV action head only
- batch size: 1
- max steps: 3
- target: `action_chunk = [8, 4]`
- proprio/state: `[x, y, z, yaw]`

Loss:

- step 1: 0.3095709979534149
- step 2: 0.07122696936130524
- step 3: 0.05707600340247154

Memory:

- max CUDA memory: about 14.456 GB

## Meaning

This verifies the minimum model-stage training loop:

TravelUAV image + instruction + UAV state
-> OpenVLA processor
-> frozen OpenVLA feature extraction
-> UAV action head
-> action_chunk regression loss
-> backward + optimizer step

## What This Does Not Prove

This is not final OpenVLA-OFT migration training.

It does not prove:

- final navigation performance;
- closed-loop UAV success rate;
- generalization across full TravelUAV;
- LoRA/OFT benefit;
- Diffusion Policy performance;
- RL expert trajectory quality.

## Current Best Interpretation

The project has passed the minimum feasibility gate for OpenVLA-to-UAV action-head adaptation.

The next stage should move from smoke testing to a controlled pilot training experiment.
