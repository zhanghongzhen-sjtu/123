# UAV OpenVLA-Style JSONL Schema

Schema version: `uav_openvla_jsonl_v0.1`

This schema freezes the lightweight data contract used in the current local stage. It is designed for TravelUAV raw episode debug conversion and for later OpenVLA-OFT dataset integration. It does not require loading any OpenVLA / OpenVLA-OFT model weights.

## Required Row Fields

Each JSONL line must be one JSON object with the following fields:

| Field | Type | Requirement |
| --- | --- | --- |
| `dataset` | string | Must be `TravelUAV` for current data. |
| `episode_id` | string | Stable episode directory or raw episode id. |
| `step_id` | integer | Zero-based step index inside the converted episode. |
| `image` | string | Path to the observation image. Current raw conversion uses `frontcamera/*.png`. |
| `instruction` | string | Natural-language navigation instruction. Empty string is invalid for training data. |
| `state` | list[float] | Four-dimensional UAV state `[x, y, z, yaw]`. |
| `action` | list[float] | Four-dimensional UAV action `[vx, vy, vz, yaw_rate]`. |
| `action_chunk` | list[list[float]] | Future action sequence. Each inner action must be four-dimensional. |
| `dt` | float | Positive time interval in seconds used to compute the current action. |
| `source` | object | Trace metadata for raw file, map, frame, timestamp, and target. |

## State And Action Convention

State:

```text
state = [x, y, z, yaw]
```

Action:

```text
action = [vx, vy, vz, yaw_rate]
```

If raw action is not provided, action is computed from adjacent states:

```text
vx = (x_next - x) / dt
vy = (y_next - y) / dt
vz = (z_next - z) / dt
yaw_rate = wrap_angle(yaw_next - yaw) / dt
```

`yaw` and `yaw_rate` are in radians. `wrap_angle` maps angular differences to `[-pi, pi]`.

## `dt` Policy

For TravelUAV raw episode data, `dt` should be computed from adjacent `sensors.state.timestamp` values whenever available. The current 3-map debug conversion uses image-aligned frames with frame delta 5 and timestamp-derived `dt` around 4.97 seconds.

Using `dt=1.0` for these image-aligned raw frames would overestimate velocity, so timestamp-derived `dt` is the preferred source. When timestamp data is missing or non-positive, the converter may fall back to the CLI `--dt` value and must record `source.dt_source = "fallback_arg"`.

## Recommended `source` Fields

The current raw episode converter writes these trace fields when available:

| Field | Meaning |
| --- | --- |
| `raw_file` | Current raw log JSON file. |
| `next_raw_file` | Next raw log JSON file used for action computation. |
| `raw_episode_dir` | Raw episode directory. |
| `map` | TravelUAV map name, such as `BrushifyUrban`. |
| `frame` | Current image/log frame id. |
| `next_frame` | Next image/log frame id. |
| `timestamp` | Current raw timestamp. |
| `next_timestamp` | Next raw timestamp. |
| `dt_source` | `timestamp` or `fallback_arg`. |
| `raw_linear_velocity` | Optional raw log linear velocity for auditing. |
| `raw_angular_velocity` | Optional raw log angular velocity for auditing. |
| `target` | Optional target object and endpoint metadata from `mark.json`. |

These fields are not the model input contract, but they should be preserved in debug files because they make data auditing reproducible.

## Current 3-Map Validation Status

The schema has been validated on three downloaded TravelUAV raw map subsets:

- `BrushifyCountryRoads`
- `BrushifyUrban`
- `Carla_Town02`

Generated debug files:

- `data/debug/traveluav_BrushifyCountryRoads_debug.jsonl`
- `data/debug/traveluav_BrushifyUrban_debug.jsonl`
- `data/debug/traveluav_Carla_Town02_debug.jsonl`
- `data/debug/traveluav_3maps_debug.jsonl`

The current rows contain `image`, `instruction`, `state`, `action`, `action_chunk`, `dt`, and `source`. Image path existence has been checked with `--image-root .`.

## Validation Commands

```bash
cd /mnt/d/中期/vla-uav-diffusion

python -m src.openvla_uav_transfer.checks.check_uav_jsonl \
  --jsonl data/debug/traveluav_BrushifyCountryRoads_debug.jsonl \
  --image-root . \
  --max-show 5

python -m src.openvla_uav_transfer.checks.check_uav_jsonl \
  --jsonl data/debug/traveluav_BrushifyUrban_debug.jsonl \
  --image-root . \
  --max-show 5

python -m src.openvla_uav_transfer.checks.check_uav_jsonl \
  --jsonl data/debug/traveluav_Carla_Town02_debug.jsonl \
  --image-root . \
  --max-show 5
```

## Boundary

This schema is a local engineering artifact. It is suitable for data-path validation and later dataset integration planning. It is not evidence of completed OpenVLA-OFT training, closed-loop simulator success, Diffusion Policy training, or RL expert generation.

## Dataset Loader Smoke Test

The schema is also validated by a CPU-only loader:

- `src/openvla_uav_transfer/datasets/uav_jsonl_dataset.py`
- `src/openvla_uav_transfer/checks/smoke_uav_dataset_loader.py`

Run:

```bash
cd /mnt/d/中期/vla-uav-diffusion
bash scripts/run_smoke_dataset_loader.sh
```

The loader checks row fields, resolves image paths, reads optional normalization statistics, and can attach normalized state/action fields. It does not import torch or load OpenVLA-OFT weights.
