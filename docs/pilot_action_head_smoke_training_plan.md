# Pilot Action-Head Smoke Training Plan

## Purpose

This is only a pilot smoke training plan for checking whether the UAV action target interface can be optimized.

It is not final OpenVLA-OFT migration training.

## Dataset

- train: data/processed/pilot_train_3maps.jsonl
- val: data/processed/pilot_val_3maps.jsonl
- stats: data/processed/pilot_train_3maps_stats.json

## Allowed Smoke Training Scope

Allowed:

- train only a tiny action-head prototype or MLP baseline
- use image path as metadata only, if needed
- use instruction as metadata only, if needed
- use state/action/action_chunk numerical tensors
- run very few epochs
- verify loss decreases
- verify dataloader and tensor shapes

Not allowed in this pilot:

- load OpenVLA-OFT / openvla-7b
- LoRA / OFT
- train full VLA
- closed-loop simulation
- Diffusion Policy training
- RL training
- claim final model performance

## Suggested Prototype

Input:

- state = [x, y, z, yaw]

Output:

- action_chunk = [8, 4]

Tiny MLP:

- input dim: 4
- hidden dim: 64 or 128
- output dim: 32

Loss:

- MSE between predicted action_chunk and target action_chunk

Expected Result:

- training loss should decrease on the pilot train set
- validation loss is only sanity reference
- no thesis-level conclusion

## Stop Marker

If this evolves into loading OpenVLA-OFT/openvla-7b or LoRA/OFT, stop and mark:

NEED_5090_MODEL_STAGE_CONFIRMATION

## Final Marker

- PILOT_SMOKE_TRAINING_PLAN_READY
- NOT_FINAL_TRAINING
