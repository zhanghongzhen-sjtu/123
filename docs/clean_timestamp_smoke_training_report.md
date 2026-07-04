# Clean Timestamp Smoke Training Report

## Status

- FORMAT_PASS
- LOADER_PASS
- CLEAN_TIMESTAMP_SPLIT_PASS
- TINY_ACTION_HEAD_SMOKE_PASS
- NOT_FINAL_OPENVLA_TRAINING

## Dataset

Clean timestamp split uses only samples whose `source.dt_source` is `timestamp`.

Train:

- data/processed/clean_train_timestamp_maps.jsonl
- maps: BrushifyCountryRoads, BrushifyUrban

Validation:

- data/processed/clean_val_timestamp_maps.jsonl
- maps: Carla_Town02, Carla_Town03

Excluded from clean timestamp split for now:

- Carla_Town01
- Carla_Town04
- Carla_Town05

Reason: these maps include samples whose action dt comes from `fallback_arg`, so they are useful for format/debug checks but not yet ideal for first clean action-target training.

## Smoke Training

Tiny MLP only:

- input: state = [x, y, z, yaw]
- output: action_chunk = [8, 4]
- no image encoder
- no instruction encoder
- no OpenVLA-OFT
- no openvla-7b
- no LoRA/OFT

Report file:

- logs/pilot/tiny_action_head_clean_timestamp_report.json

## Interpretation

This confirms that the real TravelUAV clean timestamp subset can be loaded as tensors and optimized by a tiny action-head prototype.

This does not prove OpenVLA-OFT migration performance.

## Next Step

Before OpenVLA-OFT migration training, prepare a model-stage checklist:

1. confirm exact OpenVLA-OFT training entrypoint;
2. confirm action head modification location;
3. confirm UAV state projector location;
4. confirm image/instruction/state/action batch schema;
5. run a no-model dataloader dry run against the OpenVLA-OFT-style adapter;
6. only then decide whether to load OpenVLA/openvla-7b on RTX 5090.

