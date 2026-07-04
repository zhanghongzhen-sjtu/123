# Medium 7-Map dt Audit

## Dataset

- train: data/processed/medium_train_7maps.jsonl
- val: data/processed/medium_val_7maps.jsonl

## Split

train:

- BrushifyCountryRoads
- BrushifyUrban
- Carla_Town01
- Carla_Town03
- Carla_Town04

val:

- Carla_Town02
- Carla_Town05

## Validation Status

- medium train rows: 300
- medium val rows: 114
- train CHECK_PASS
- val CHECK_PASS
- train STATS_PASS

## dt Source Summary

train:

- timestamp: 180
- fallback_arg: 120

val:

- timestamp: 54
- fallback_arg: 60

## Interpretation

The medium 7-map dataset is format-valid but not yet timing-clean.

Some maps provide valid timestamp deltas and yield velocities around the expected scale.

Some CARLA maps have missing or non-positive timestamp deltas and fall back to dt=1.0. These rows show larger velocity magnitudes.

## Risk

If fallback dt rows are mixed with timestamp dt rows without correction, the action distribution becomes inconsistent.

This can hurt action-head or OpenVLA-OFT training because the model sees different velocity scales for different maps.

## Recommendation

Before OpenVLA-OFT training, choose one of:

1. exclude maps with fallback dt from training;
2. recover true dt from raw logs or frame rate metadata;
3. use a fixed frame-based dt consistently for all maps;
4. train with explicit dt input or map-specific normalization.

## Current Conclusion

- MEDIUM_7MAP_FORMAT_PASS
- MEDIUM_7MAP_TIMING_NOT_CLEAN
- NOT_READY_FOR_OPENVLA_TRAINING
