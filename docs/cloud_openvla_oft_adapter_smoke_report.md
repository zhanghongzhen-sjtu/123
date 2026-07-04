# OpenVLA-OFT UAV Adapter Smoke Report

This report validates only the CPU-side dataset adapter shape contract. It does not load OpenVLA-OFT, does not train a model, and does not run simulator evaluation.

## Inputs
- `data/debug/cloud_BrushifyCountryRoads_debug.jsonl`

## Dataset Summary

- Rows loaded: `60`
- Maps: `{'BrushifyCountryRoads': {'rows': 60, 'episodes': 3}}`
- action chunk lengths: `{8: 60}`
- dt sources: `{'timestamp': 60}`
- normalized: `True`
- stats path: `data/debug/cloud_3maps_stats.json`

## Batch Contract

- Batch size: `8`
- Shapes: `{'states': [8, 4], 'actions': [8, 4], 'action_chunks': [8, 8, 4], 'dts': [8], 'states_normalized': [8, 4], 'actions_normalized': [8, 4], 'action_chunks_normalized': [8, 8, 4]}`

## OpenVLA-OFT Field Mapping

- `vision` <- `image_paths`
- `language` <- `instructions`
- `proprio` <- `states`
- `action_target` <- `action_chunks`
- `single_step_action` <- `actions`
- `metadata` <- `sources`

## First Sample

```json
{
  "episode_id": "0008c004-9c02-40d3-928f-b7228c17a39d",
  "step_id": 0,
  "image_path": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/frontcamera/000000.png",
  "instruction_chars": 407,
  "state": [
    -540.9619750976562,
    -453.1080017089844,
    -39.50600051879883,
    0.2372481270116989
  ],
  "action": [
    -0.25632749836174373,
    -0.6267476637951509,
    -0.5523580636035098,
    -0.44208744682595014
  ],
  "action_chunk_len": 8,
  "dt": 4.986106368,
  "map": "BrushifyCountryRoads"
}
```

## Status

- `ADAPTER_SMOKE_PASS`
- `NOT_TRAINING_READY`: this remains a debug subset and an interface smoke test, not a final OpenVLA-OFT training dataset.
