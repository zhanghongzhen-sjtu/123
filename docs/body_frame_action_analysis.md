# Body-Frame UAV Action Analysis

## Status

- `BODY_FRAME_ACTION_ANALYSIS_PASS`
- training started: `false`
- model loaded: `false`

## Converted Files

- train body JSONL: `data/processed/full_clean_train_timestamp_body.jsonl` rows=16267
- val body JSONL: `data/processed/full_clean_val_timestamp_body.jsonl` rows=4325

## Action Definitions

World-frame action:

```text
action_world = [vx, vy, vz, yaw_rate]
```

Body-frame action:

```text
v_forward = cos(yaw) * vx + sin(yaw) * vy
v_right   = -sin(yaw) * vx + cos(yaw) * vy
action_body = [v_forward, v_right, vz, yaw_rate]
```

## Motivation

World-frame vx/vy depend on global map axes. For UAV navigation, the same forward motion may appear as different world-frame vx/vy values depending on yaw and map orientation.

Body-frame actions are ego-centric and therefore better aligned with cross-map and cross-heading transfer.

## Plots

- `data/debug/plots/body_frame_action_analysis/train_world_action_std_by_map.png`
- `data/debug/plots/body_frame_action_analysis/train_body_action_std_by_map.png`
- `data/debug/plots/body_frame_action_analysis/val_world_action_std_by_map.png`
- `data/debug/plots/body_frame_action_analysis/val_body_action_std_by_map.png`

## Train World-Frame Stats

| map | dim | mean | std | min | max |
|---|---|---:|---:|---:|---:|
| BrushifyCountryRoads | vx | 0.107311 | 0.616203 | -0.986714 | 0.986714 |
| BrushifyCountryRoads | vy | -0.003757 | 0.652857 | -0.986812 | 0.996886 |
| BrushifyCountryRoads | vz | -0.070118 | 0.360704 | -0.996273 | 1.002547 |
| BrushifyCountryRoads | yaw_rate | 0.000901 | 0.065200 | -0.626805 | 0.765774 |
| BrushifyUrban | vx | 0.054550 | 0.698393 | -0.996886 | 0.996886 |
| BrushifyUrban | vy | 0.090606 | 0.639890 | -0.996886 | 0.996886 |
| BrushifyUrban | vz | 0.018088 | 0.210683 | -0.973179 | 1.002378 |
| BrushifyUrban | yaw_rate | -0.001034 | 0.055278 | -0.830701 | 0.843045 |
| Carla_Town02 | vx | -0.022953 | 0.703064 | -0.994343 | 0.994343 |
| Carla_Town02 | vy | 0.024916 | 0.622976 | -0.996886 | 0.991800 |
| Carla_Town02 | vz | 0.016006 | 0.176289 | -0.996741 | 0.983397 |
| Carla_Town02 | yaw_rate | -0.002092 | 0.095388 | -0.892472 | 0.871012 |
| Carla_Town03 | vx | 0.010736 | 0.625270 | -0.994343 | 0.994343 |
| Carla_Town03 | vy | -0.042679 | 0.679071 | -0.993881 | 0.994337 |
| Carla_Town03 | vz | -0.011883 | 0.285402 | -0.996850 | 1.000636 |
| Carla_Town03 | yaw_rate | -0.002951 | 0.092480 | -1.447991 | 0.744003 |

## Train Body-Frame Stats

| map | dim | mean | std | min | max |
|---|---|---:|---:|---:|---:|
| BrushifyCountryRoads | v_forward | 0.834093 | 0.327789 | -0.999646 | 1.001856 |
| BrushifyCountryRoads | v_right | -0.001033 | 0.119641 | -0.989210 | 0.993245 |
| BrushifyCountryRoads | vz | -0.070118 | 0.360704 | -0.996273 | 1.002547 |
| BrushifyCountryRoads | yaw_rate | 0.000901 | 0.065200 | -0.626805 | 0.765774 |
| BrushifyUrban | v_forward | 0.901683 | 0.253884 | -1.008351 | 1.020654 |
| BrushifyUrban | v_right | -0.002156 | 0.175770 | -0.998241 | 0.997611 |
| BrushifyUrban | vz | 0.018088 | 0.210683 | -0.973179 | 1.002378 |
| BrushifyUrban | yaw_rate | -0.001034 | 0.055278 | -0.830701 | 0.843045 |
| Carla_Town02 | v_forward | 0.808095 | 0.336415 | -0.996379 | 0.997601 |
| Carla_Town02 | v_right | -0.009960 | 0.342413 | -0.993777 | 0.993223 |
| Carla_Town02 | vz | 0.016006 | 0.176289 | -0.996741 | 0.983397 |
| Carla_Town02 | yaw_rate | -0.002092 | 0.095388 | -0.892472 | 0.871012 |
| Carla_Town03 | v_forward | 0.864470 | 0.275942 | -0.984763 | 0.995275 |
| Carla_Town03 | v_right | -0.007796 | 0.174693 | -0.994327 | 0.990175 |
| Carla_Town03 | vz | -0.011883 | 0.285402 | -0.996850 | 1.000636 |
| Carla_Town03 | yaw_rate | -0.002951 | 0.092480 | -1.447991 | 0.744003 |
