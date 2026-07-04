# TravelUAV 3-Map Statistics

This report is generated from lightweight debug JSONL files. It is suitable for schema validation and future normalization planning, but it is not a final full-dataset training statistic.

## Inputs
- `data/processed/clean_train_timestamp_maps.jsonl`: `120` rows

## Summary
- Schema version: `uav_openvla_jsonl_v0.1`
- Rows: `120`
- dt sources: `{'timestamp': 120}`
- action chunk lengths: `{'8': 120}`

## Per-Map Counts

| Map | Rows | Episodes |
| --- | ---: | ---: |
| BrushifyCountryRoads | 60 | 3 |
| BrushifyUrban | 60 | 3 |

## Timing

- `dt`: min=4.947106, max=5.004107, mean=4.980681, std=0.012516, median=4.983106, q01=4.950106, q99=5.000537

## State Statistics

| Dimension | Stats |
| --- | --- |
| x | min=-963.186829, max=672.569214, mean=-412.832336, std=512.326555, median=-468.376907, q01=-958.031445, q99=666.661909 |
| y | min=-1774.394043, max=-204.954254, mean=-1036.924358, std=574.666073, median=-1076.866974, q01=-1774.394043, q99=-210.783893 |
| z | min=-151.051819, max=-8.328043, mean=-43.170921, std=40.408112, median=-28.774500, q01=-151.047702, q99=-8.346780 |
| yaw | min=-2.667481, max=2.491504, mean=-0.041053, std=1.781907, median=-0.000000, q01=-2.649890, q99=2.465810 |

State normalization vectors:

- mean: `[-412.8323361714681, -1036.9243584950766, -43.17092085679372, -0.04105283624400983]`
- std: `[512.3265554135331, 574.6660732116625, 40.40811207817776, 1.781907342112329]`
- min: `[-963.1868286132812, -1774.39404296875, -151.05181884765625, -2.667481401824842]`
- max: `[672.5692138671875, -204.95425415039062, -8.328042984008789, 2.4915041500567696]`

## Action Statistics

| Dimension | Stats |
| --- | --- |
| vx | min=-0.874819, max=0.996886, mean=0.087249, std=0.690011, median=-0.037900, q01=-0.869993, q99=0.996886 |
| vy | min=-0.834129, max=0.986714, mean=-0.051947, std=0.568814, median=0.000000, q01=-0.834129, q99=0.986714 |
| vz | min=-0.991800, max=0.011324, mean=-0.175026, std=0.354890, median=0.001925, q01=-0.991800, q99=0.011085 |
| yaw_rate | min=-0.445482, max=0.523692, mean=-0.000532, std=0.081528, median=0.000000, q01=-0.368976, q99=0.292605 |

Action normalization vectors:

- mean: `[0.08724884566885598, -0.05194670970470034, -0.17502553020638847, -0.0005317851770499641]`
- std: `[0.6900113283276199, 0.5688137160170776, 0.35488997252601323, 0.08152787073017669]`
- min: `[-0.8748185767870285, -0.8341293406573994, -0.9918001306597126, -0.44548232441290436]`
- max: `[0.9968862851759164, 0.986713976143509, 0.011323847645649424, 0.5236916080035919]`

## Instruction Length

- characters: min=245.000000, max=407.000000, mean=303.500000, std=51.857979, median=288.000000, q01=245.000000, q99=407.000000

## Boundary

These statistics come from three small debug subsets only. Full training normalization must be recomputed from the actual training split on the 5090 stage before model training.
