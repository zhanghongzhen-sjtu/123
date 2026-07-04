# OpenVLA-OFT UAV Dataset Adapter Design

This document describes the intended bridge from TravelUAV debug JSONL to a future OpenVLA-OFT UAV migration training pipeline. The current implementation is CPU-only and does not load OpenVLA-OFT / openvla-7b weights.

## Current Data Contract

Validated JSONL schema:

```text
dataset = TravelUAV
episode_id: str
step_id: int
image: path
instruction: str
state: [x, y, z, yaw]
action: [vx, vy, vz, yaw_rate]
action_chunk: [[vx, vy, vz, yaw_rate], ...]
dt: float
source: dict
```

Current real debug validation:

- `FORMAT_PASS`
- `ACTION_PASS`
- `NOT_TRAINING_READY`

This means the data path is valid, but the small debug subset is not a final training dataset.

## Adapter Components

| Component | File | Role |
| --- | --- | --- |
| JSONL dataset loader | `src/openvla_uav_transfer/datasets/uav_jsonl_dataset.py` | Reads and validates UAV JSONL rows. |
| OpenVLA-OFT-style collator | `src/openvla_uav_transfer/datasets/uav_collator.py` | Builds plain Python batch dictionaries for interface smoke tests. |
| Adapter smoke test | `src/openvla_uav_transfer/checks/smoke_openvla_oft_adapter.py` | Checks batch shapes and field mapping without model loading. |
| Runner | `scripts/run_smoke_openvla_oft_adapter.sh` | Runs the CPU-only adapter smoke test. |

## OpenVLA-OFT Field Mapping

The local collator produces this mapping:

| OpenVLA-OFT concept | Current batch field | Notes |
| --- | --- | --- |
| Vision input | `image_paths` | Current smoke test preserves paths only; future adapter will decode/preprocess images using OpenVLA-OFT transforms. |
| Language input | `instructions` | Natural-language TravelUAV navigation instruction. |
| Proprio/state input | `states` | UAV 4D state `[x, y, z, yaw]`. |
| Single-step action | `actions` | UAV 4D action `[vx, vy, vz, yaw_rate]`. |
| Action target chunk | `action_chunks` | Shape `[B, T, 4]`, current `T=8`. |
| Timing metadata | `dts` | Timestamp-derived seconds; not necessarily direct model input. |
| Trace metadata | `sources` | Used for debugging, not model input. |

When normalization is enabled, the collator also emits:

- `states_normalized`
- `actions_normalized`
- `action_chunks_normalized`

## Current Smoke-Test Batch Contract

Current run:

```text
JSONL: data/debug/traveluav_BrushifyCountryRoads_debug.jsonl
batch_size: 8
state shape: [8, 4]
action shape: [8, 4]
action_chunk shape: [8, 8, 4]
normalized state shape: [8, 4]
normalized action shape: [8, 4]
normalized action_chunk shape: [8, 8, 4]
```

Success marker:

```text
ADAPTER_SMOKE_PASS: OpenVLA-OFT UAV adapter batch contract is valid without model loading.
```

## What This Does Not Do

The current adapter does not:

- import torch;
- decode images;
- run OpenVLA-OFT preprocessing;
- instantiate OpenVLA-OFT modules;
- load `openvla-7b`;
- train an action head;
- run LoRA / OFT;
- run simulator evaluation.

It only checks that the TravelUAV JSONL can be shaped into the future OpenVLA-OFT dataset interface.

## Later OpenVLA-OFT Integration Points

Future 5090-stage integration should connect this contract to OpenVLA-OFT:

1. Dataset registration / loader selection.
2. Image decode and visual processor.
3. Language prompt formatting.
4. UAV 4D proprio/state projector.
5. Continuous action head output dimension changed or configured to 4.
6. Action chunk length aligned with JSONL `action_chunk`.
7. State/action normalization loaded from full training split statistics.
8. Training script config with UAV dataset path and checkpoint path.

## When Full Data Uses 5090

Full TravelUAV data should be introduced in stages:

| Stage | Local 3060 / CPU OK? | 5090 Needed? | Reason |
| --- | --- | --- | --- |
| Download selected archives | Usually OK if disk/network allow | No | No model or training. |
| Extract selected archives | Usually OK if disk allow | No | CPU/disk work only. |
| Scan directory structure | Yes | No | Lightweight metadata work. |
| Convert a few debug episodes | Yes | No | Small JSONL validation. |
| Convert full train/val split | Prefer 5090 server if data is large | Often yes | Large IO and preprocessing; better close to training storage. |
| Compute full normalization stats | Prefer 5090 server | Often yes | Must match exact training split and may be large. |
| Load OpenVLA-OFT / openvla-7b | No | Yes | GPU memory requirement. |
| Train UAV action head | No | Yes | Training workload. |
| LoRA / OFT | No | Yes | Training workload. |
| Closed-loop sim evaluation | No | Yes | GPU/model/simulator workload. |
| Diffusion Policy training | No | Yes | Training workload. |
| RL expert generation | No | Yes | Long-running simulation/training workload. |

Practical rule:

- Use local machine for schema, small debug conversion, validation, visualization, and CPU-only adapter smoke tests.
- Move to AutoDL RTX 5090 before full train/val preprocessing that will be consumed by OpenVLA-OFT training, and definitely before loading any VLA model or running training.

The local pseudo config records this boundary explicitly:

```text
configs/openvla_oft_uav_debug.yaml
```

It must remain `training_enabled: false` and `model_loading_enabled: false` while running locally.

Stop marker:

```text
NEED_5090: 当前任务需要 AutoDL RTX 5090，不应在本地 3060 执行。
```

## Current Conclusion

The debug data path is ready as an engineering interface:

```text
TravelUAV raw episode
-> UAV JSONL
-> schema/action validation
-> CPU-only dataset loader
-> CPU-only OpenVLA-OFT-style collator
```

It is not training-ready. The pseudo OpenVLA-OFT config draft is now present and checked. The next 5090 step should only begin after the full data split plan and adapter contract are frozen.
