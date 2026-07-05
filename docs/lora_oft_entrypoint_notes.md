# LoRA/OFT Entrypoint Notes

## Purpose

This document records the OpenVLA-OFT LoRA/OFT training entrypoints and the places that must be checked before running a tiny LoRA/OFT smoke.

## Current Policy

This is static code inspection only.

No LoRA/OFT training was started by this step.

## Candidate Entrypoint

Primary candidate:

- `external/openvla-oft/vla-scripts/finetune.py`

Relevant areas to inspect:

- config dataclass / CLI arguments;
- LoRA configuration;
- OFT or adapter configuration;
- action head construction;
- proprio projector construction;
- dataset / collator construction;
- checkpoint save logic.

## UAV Requirements

For UAV migration:

- `ACTION_DIM = 4`
- `PROPRIO_DIM = 4`
- `NUM_ACTIONS_CHUNK = 8`
- dataset item must provide `actions = [B,8,4]`
- dataset item must provide `proprio = [B,4]`

## Risks Before Running

1. Native finetune path expects RLDS datasets, not the current UAV JSONL dataset.
2. Native collator can handle `actions` and `proprio`, but dataset class must provide correct fields.
3. Native constants default to LIBERO unless UAV detection is active.
4. Saving logic may save large checkpoints if not controlled.
5. LoRA/OFT may train more modules than intended if config is not constrained.
6. Full OpenVLA training must not start accidentally.

## Recommended Tiny Smoke Strategy

Instead of directly running full `vla-scripts/finetune.py`, first create a small standalone LoRA smoke script that:

- loads `openvla/openvla-7b`;
- freezes most parameters;
- applies LoRA only to selected small target modules;
- uses `UAVJsonlDatasetForOpenVLAOFT`;
- runs 1 to 5 optimizer steps;
- saves only LoRA/action-head smoke checkpoint;
- logs memory and loss.

## Decision Marker

Before running:

`LORA_OFT_TINY_SMOKE_CONFIRMED`
