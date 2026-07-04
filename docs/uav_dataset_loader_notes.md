# UAV JSONL Dataset Loader Notes

This note records the CPU-only dataset-loader smoke test for the first-stage TravelUAV to OpenVLA-OFT-style data path.

## Purpose

The loader verifies that future OpenVLA-OFT integration can consume the local JSONL contract without loading model weights. It checks the data interface only:

```text
image_path + instruction + state + action + action_chunk + dt + source
```

It does not import torch, transformers, OpenVLA-OFT, or simulator code.

## Files

- Loader: `src/openvla_uav_transfer/datasets/uav_jsonl_dataset.py`
- Smoke test: `src/openvla_uav_transfer/checks/smoke_uav_dataset_loader.py`
- Runner: `scripts/run_smoke_dataset_loader.sh`

## Input Contract

The loader expects rows following `uav_openvla_jsonl_v0.1`:

- `dataset == "TravelUAV"`
- non-empty `episode_id`
- non-negative integer `step_id`
- non-empty `image`
- non-empty `instruction`
- `state` is 4D numeric `[x, y, z, yaw]`
- `action` is 4D numeric `[vx, vy, vz, yaw_rate]`
- `action_chunk` is a non-empty list of 4D numeric actions
- `dt` is positive
- `source` is optional metadata

## Normalization

The smoke test can read `data/debug/traveluav_3maps_stats.json` and attach:

- `state_normalized`
- `action_normalized`
- `action_chunk_normalized`

These are plain Python lists. The current stats are only from the 3-map debug subset and must not be reused as final training statistics.

## Command

```bash
cd /mnt/d/中期/vla-uav-diffusion
bash scripts/run_smoke_dataset_loader.sh
```

Expected success marker:

```text
SMOKE_PASS: UAV JSONL dataset loader works without model loading.
```

## Current Results

The smoke test has passed in two modes:

- `data/debug/traveluav_3maps_debug.jsonl`: 60 rows, max 20 rows per map.
- Three single-map debug JSONL files together: 174 rows.

The 174-row run reported:

- maps: 3
- action chunk lengths: `8`
- dt sources: `timestamp`
- image existence check: enabled
- normalization: enabled with `data/debug/traveluav_3maps_stats.json`

## Boundary

This loader is a bridge toward OpenVLA-OFT dataset integration. It is not a model-training script, does not load `openvla-7b`, and does not run closed-loop evaluation.
