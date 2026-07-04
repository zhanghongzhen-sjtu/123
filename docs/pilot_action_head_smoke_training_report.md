# Pilot Action-Head Smoke Training Report

## Status

- `PILOT_ACTION_HEAD_SMOKE_PASS`
- `NOT_OPENVLA_TRAINING`
- `NOT_FINAL_TRAINING`

## Dataset

- train: `data/processed/pilot_train_3maps.jsonl`
- val: `data/processed/pilot_val_3maps.jsonl`
- train rows: `120`
- val rows: `54`

## Model

Tiny MLP baseline only.

- input: `state=[x,y,z,yaw]`
- output: `action_chunk=[8,4]`
- hidden dim: `128`
- epochs: `30`
- batch size: `32`
- lr: `0.001`
- device: `cuda`

## Loss

- initial val loss: `116.468388`
- final train loss: `1.232998`
- final val loss: `94.509247`
- train loss decreased: `True`
- val loss finite: `True`

## Interpretation

This confirms that the pilot UAV action target can be loaded into a torch Dataset and optimized by a tiny action-head prototype.

It does not prove OpenVLA-OFT migration performance.

## Not Included

- no OpenVLA-OFT / openvla-7b loading
- no LoRA / OFT
- no full VLA training
- no closed-loop simulation
- no Diffusion Policy training
- no RL training

## Next Step

Prepare a full-data plan before any OpenVLA-OFT model loading.
