# TravelUAV 3-Map Statistics

This report is generated from lightweight debug JSONL files. It is suitable for schema validation and future normalization planning, but it is not a final full-dataset training statistic.

## Inputs
- `data/processed/medium_train_7maps.jsonl`: `300` rows

## Summary
- Schema version: `uav_openvla_jsonl_v0.1`
- Rows: `300`
- dt sources: `{'fallback_arg': 120, 'timestamp': 180}`
- action chunk lengths: `{'8': 300}`

## Per-Map Counts

| Map | Rows | Episodes |
| --- | ---: | ---: |
| BrushifyCountryRoads | 60 | 3 |
| BrushifyUrban | 60 | 3 |
| Carla_Town01 | 60 | 3 |
| Carla_Town03 | 60 | 3 |
| Carla_Town04 | 60 | 3 |

## Timing

- `dt`: min=1.000000, max=5.004107, mean=3.390114, std=1.951596, median=4.972606, q01=1.000000, q99=4.998107

## State Statistics

| Dimension | Stats |
| --- | --- |
| x | min=-963.186829, max=672.569214, mean=-74.805108, std=457.493644, median=70.419903, q01=-950.796750, q99=657.739895 |
| y | min=-1774.394043, max=201.048004, mean=-426.556229, std=626.634673, median=-143.032990, q01=-1774.394043, q99=197.184638 |
| z | min=-151.051819, max=0.633000, mean=-22.731618, std=30.882915, median=-9.053480, q01=-151.043412, q99=-2.651701 |
| yaw | min=-2.667481, max=3.101737, mean=0.396932, std=1.734211, median=0.027735, q01=-2.598173, q99=2.994858 |

State normalization vectors:

- mean: `[-74.80510842641195, -426.55622920105856, -22.731618272066115, 0.3969318136506823]`
- std: `[457.4936436835631, 626.6346725142442, 30.882915383121205, 1.7342107068831079]`
- min: `[-963.1868286132812, -1774.39404296875, -151.05181884765625, -2.667481401824842]`
- max: `[672.5692138671875, 201.04800415039062, 0.6330000162124634, 3.101737125634946]`

## Action Statistics

| Dimension | Stats |
| --- | --- |
| vx | min=-4.369812, max=4.925781, mean=0.481068, std=2.340825, median=0.035789, q01=-4.369812, q99=4.903336 |
| vy | min=-4.417114, max=4.524963, mean=-0.049529, std=1.959823, median=0.074186, q01=-4.392268, q99=4.522247 |
| vz | min=-3.599791, max=0.015012, mean=-0.165149, std=0.440046, median=0.000049, q01=-2.492811, q99=0.011092 |
| yaw_rate | min=-1.922261, max=2.693638, mean=0.014369, std=0.298784, median=-0.000000, q01=-0.446538, q99=0.677461 |

Action normalization vectors:

- mean: `[0.48106816275815567, -0.049529201737242734, -0.16514941485250675, 0.014368999461613957]`
- std: `[2.340825473346718, 1.9598226769141127, 0.4400456944592024, 0.2987839075440386]`
- min: `[-4.36981201171875, -4.4171142578125, -3.599790930747986, -1.9222609618523965]`
- max: `[4.92578125, 4.52496337890625, 0.015012264251708984, 2.6936376120447862]`

## Instruction Length

- characters: min=245.000000, max=478.000000, mean=325.600000, std=57.430306, median=320.000000, q01=245.000000, q99=478.000000

## Boundary

These statistics come from three small debug subsets only. Full training normalization must be recomputed from the actual training split on the 5090 stage before model training.
