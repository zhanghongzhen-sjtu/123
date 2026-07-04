# OpenVLA-OFT UAV Minimal Model Smoke Plan

## Goal

Validate whether the UAV JSONL dataset can enter the real OpenVLA-OFT preprocessing/model interface on RTX 5090.

This is not final training.

## Stage 0: Already Completed

- TravelUAV real data converted to JSONL.
- Clean timestamp split created.
- Tiny action-head smoke passed.
- Collator-ready stub passed.

## Stage 1: Processor/Image Transform Smoke

Purpose:

- replace fake tokenizer with OpenVLA tokenizer;
- replace fake PIL resize with OpenVLA image transform;
- keep model weights unloaded if possible.

Checks:

- `input_ids` shape valid;
- `labels` mask valid;
- `pixel_values` shape valid;
- `actions = [B, 8, 4]`;
- `proprio = [B, 4]`.

Expected result:

- `OPENVLA_PROCESSOR_SMOKE_PASS`

## Stage 2: Model Import Smoke

Purpose:

- import OpenVLA-OFT modules;
- verify UAV constants are selected;
- instantiate or load only required lightweight components if possible.

Stop if checkpoint/model weights are required unless user confirms.

Expected result:

- `OPENVLA_IMPORT_SMOKE_PASS`

## Stage 3: One-Batch Forward Smoke

Only after explicit confirmation.

Purpose:

- load OpenVLA-OFT/openvla-7b or checkpoint;
- run one mini-batch forward;
- no training loop;
- no LoRA/OFT optimizer step.

Expected result:

- `OPENVLA_ONE_BATCH_FORWARD_SMOKE_PASS`

## Stage 4: Tiny Model-Stage Training Smoke

Only after separate confirmation.

Purpose:

- very small clean timestamp subset;
- very few steps;
- confirm loss can be computed;
- not final training.

Expected result:

- `OPENVLA_TINY_UAV_TRAINING_SMOKE_PASS`

## Full Training Is Separate

Full OpenVLA-OFT UAV training requires:

- fixed dataset scale decision;
- stable dt policy;
- normalization policy;
- action head/proprio projector config;
- checkpoint storage plan;
- experiment logging;
- GPU time budget;
- explicit confirmation.

## Stop Markers

If a step requires loading OpenVLA/openvla-7b, downloading checkpoints, LoRA/OFT, or full training, stop and require:

`MODEL_STAGE_CONFIRMED_BY_USER`

