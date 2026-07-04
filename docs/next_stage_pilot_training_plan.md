# Next Stage Pilot Training Plan

## Goal

Run a controlled pilot training experiment for UAV action head adaptation using real TravelUAV clean timestamp data.

This is still not full thesis-scale training.

## Recommended Dataset

Start with clean timestamp split:

- train: `data/processed/clean_train_timestamp_maps.jsonl`
- val: `data/processed/clean_val_timestamp_maps.jsonl`

Use these first because their `dt` comes from timestamp-derived action calculation.

Hold out fallback-dt maps for now:

- `Carla_Town01`
- `Carla_Town04`
- `Carla_Town05`

## Model Setup

Recommended first pilot:

- load `openvla/openvla-7b`
- freeze OpenVLA backbone
- train UAV action head only
- input feature: frozen OpenVLA feature + UAV proprio `[4]`
- output: `action_chunk [8,4]`
- loss: MSE or SmoothL1

Do not start LoRA/OFT yet.

## Pilot Scale

Start small:

- batch size: 1 or 2
- train rows: 64 to 120
- val rows: 32 to 64
- epochs: 1 to 3
- save only tiny action head checkpoint
- log train/val loss

## Required Checks

Before longer pilot:

1. verify train/val loader;
2. verify no fallback-dt maps in clean split;
3. verify action statistics;
4. verify GPU memory;
5. save config and logs;
6. save tiny action head checkpoint only.

## Success Criteria

Pilot is successful if:

- training loss decreases;
- validation loss is finite;
- no shape mismatch;
- no image path errors;
- checkpoint can be saved and reloaded;
- no LoRA/OFT or full model training is accidentally started.

## Next After Pilot

Only after pilot action-head training works:

1. compare frozen-feature action head vs state-only MLP baseline;
2. decide whether OpenVLA visual-language features help;
3. consider LoRA/OFT tiny smoke;
4. design Diffusion Policy control-sequence module;
5. design RL expert trajectory generation.
