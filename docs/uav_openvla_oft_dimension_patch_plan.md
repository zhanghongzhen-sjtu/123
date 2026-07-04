# UAV OpenVLA-OFT Dimension Patch Plan

## Confirmed Defaults

OpenVLA-OFT defaults to LIBERO when platform is unclear:

- NUM_ACTIONS_CHUNK = 8
- ACTION_DIM = 7
- PROPRIO_DIM = 8

## UAV Target

- NUM_ACTIONS_CHUNK = 8
- ACTION_DIM = 4
- PROPRIO_DIM = 4

## Consequence

UAV action_chunk shape is [8, 4], while default LIBERO action target expects [8, 7].

UAV state/proprio shape is [4], while default LIBERO proprio expects [8].

Therefore UAV JSONL is not directly trainable with the unmodified default OpenVLA-OFT constants.

## Required Minimal Patch

Add a UAV platform config in:

- external/openvla-oft/prismatic/vla/constants.py

Target constants:

- NUM_ACTIONS_CHUNK = 8
- ACTION_DIM = 4
- PROPRIO_DIM = 4
- ACTION_PROPRIO_NORMALIZATION_TYPE = NormalizationType.BOUNDS_Q99 or NORMAL

Also update platform detection so commands containing `uav` select UAV constants.

## Model Components Affected

- action head
- diffusion action head
- noisy action projector
- proprio projector
- dataset statistics
- collator-ready dataset item shape

## Current Status

- DATA_PASS
- CLEAN_TIMESTAMP_SPLIT_PASS
- ADAPTER_STUB_PASS
- COLLATOR_CONTRACT_IDENTIFIED
- DIMENSION_MISMATCH_IDENTIFIED
- MODEL_NOT_LOADED
- TRAINING_NOT_STARTED

## Next Step

Create a minimal UAV config patch proposal, but do not start OpenVLA-OFT training until explicitly confirmed.
