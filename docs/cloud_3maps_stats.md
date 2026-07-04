# TravelUAV 3-Map Statistics

This report is generated from lightweight debug JSONL files. It is suitable for schema validation and future normalization planning, but it is not a final full-dataset training statistic.

## Inputs
- `data/debug/cloud_BrushifyCountryRoads_debug.jsonl`: `60` rows
- `data/debug/cloud_BrushifyUrban_debug.jsonl`: `60` rows
- `data/debug/cloud_Carla_Town02_debug.jsonl`: `54` rows

## Summary
- Schema version: `uav_openvla_jsonl_v0.1`
- Rows: `174`
- dt sources: `{'timestamp': 174}`
- action chunk lengths: `{'8': 174}`

## Per-Map Counts

| Map | Rows | Episodes |
| --- | ---: | ---: |
| BrushifyCountryRoads | 60 | 3 |
| BrushifyUrban | 60 | 3 |
| Carla_Town02 | 54 | 3 |

## Timing

- `dt`: min=4.164089, max=5.004107, mean=4.966554, std=0.109110, median=4.989106, q01=4.355373, q99=5.001107

## State Statistics

| Dimension | Stats |
| --- | --- |
| x | min=-963.186829, max=672.569214, mean=-253.317397, std=487.850069, median=-368.118576, q01=-955.754012, q99=663.982640 |
| y | min=-1774.394043, max=249.969498, mean=-645.381201, std=754.026350, median=-500.916534, q01=-1774.394043, q99=247.487383 |
| z | min=-151.051819, max=-1.790799, mean=-30.433830, std=38.556590, median=-8.939421, q01=-151.045889, q99=-1.816896 |
| yaw | min=-3.119737, max=3.121951, mean=-0.409518, std=1.993159, median=-0.000000, q01=-3.097039, q99=3.116533 |

State normalization vectors:

- mean: `[-253.31739719434717, -645.3812010315643, -30.433829955671026, -0.4095179415783362]`
- std: `[487.8500691596089, 754.0263496805277, 38.556590251937976, 1.993158602677007]`
- min: `[-963.1868286132812, -1774.39404296875, -151.05181884765625, -3.119737218959457]`
- max: `[672.5692138671875, 249.96949768066406, -1.7907992601394653, 3.1219505106238037]`

## Action Statistics

| Dimension | Stats |
| --- | --- |
| vx | min=-0.991800, max=0.996886, mean=-0.135667, std=0.699536, median=-0.109453, q01=-0.991800, q99=0.996886 |
| vy | min=-0.991800, max=0.986714, mean=-0.183105, std=0.561817, median=0.000000, q01=-0.991401, q99=0.986714 |
| vz | min=-0.991800, max=0.011324, mean=-0.119726, std=0.306034, median=0.003008, q01=-0.991800, q99=0.011072 |
| yaw_rate | min=-0.532123, max=0.523692, mean=-0.006232, std=0.088311, median=-0.000000, q01=-0.443004, q99=0.192909 |

Action normalization vectors:

- mean: `[-0.13566715958563544, -0.18310460726690508, -0.11972598082955935, -0.006232022407943826]`
- std: `[0.6995363412683623, 0.5618171093169642, 0.30603431141399057, 0.08831146900677601]`
- min: `[-0.9918001306597126, -0.9918001306597126, -0.9918001306597126, -0.5321233302604399]`
- max: `[0.9968862851759164, 0.986713976143509, 0.011323847645649424, 0.5236916080035919]`

## Instruction Length

- characters: min=245.000000, max=407.000000, mean=310.034483, std=48.418304, median=291.000000, q01=245.000000, q99=407.000000

## Boundary

These statistics come from three small debug subsets only. Full training normalization must be recomputed from the actual training split on the 5090 stage before model training.
