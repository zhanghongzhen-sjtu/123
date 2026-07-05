# TravelUAV 3-Map Statistics

This report is generated from lightweight debug JSONL files. It is suitable for schema validation and future normalization planning, but it is not a final full-dataset training statistic.

## Inputs
- `data/offline/traveluav_offline_supervised_allmaps_1000ep.jsonl`: `330202` rows

## Summary
- Schema version: `uav_openvla_jsonl_v0.1`
- Rows: `330202`
- dt sources: `{'fallback_arg': 190576, 'timestamp': 139626}`
- action chunk lengths: `{'8': 330202}`

## Per-Map Counts

| Map | Rows | Episodes |
| --- | ---: | ---: |
| BrushifyCountryRoads | 20031 | 320 |
| BrushifyUrban | 26532 | 456 |
| Carla_Town01 | 45379 | 954 |
| Carla_Town02 | 19431 | 601 |
| Carla_Town03 | 27721 | 562 |
| Carla_Town04 | 34539 | 652 |
| Carla_Town05 | 25591 | 506 |
| Carla_Town06 | 20151 | 385 |
| Carla_Town07 | 17768 | 446 |
| Carla_Town10HD | 47148 | 1000 |
| Carla_Town15 | 45911 | 749 |

## Timing

- `dt`: min=0.540012, max=5.679121, mean=2.649162, std=1.942871, median=1.000000, q01=1.000000, q99=4.998107

## State Statistics

| Dimension | Stats |
| --- | --- |
| x | min=-2456.506348, max=1060.573730, mean=-20.497622, std=412.654173, median=35.294712, q01=-2007.774899, q99=889.376529 |
| y | min=-1783.636475, max=895.284058, mean=-8.913885, std=347.326656, median=40.447533, q01=-1346.286747, q99=726.045560 |
| z | min=-366.051300, max=13.327319, mean=-43.887086, std=55.304653, median=-17.493790, q01=-188.911935, q99=-0.067789 |
| yaw | min=-3.141593, max=3.141593, mean=0.037334, std=1.809418, median=0.013786, q01=-3.114873, q99=3.114428 |

State normalization vectors:

- mean: `[-20.49762206897943, -8.9138846716754, -43.887085552739876, 0.03733448499975936]`
- std: `[412.6541728358147, 347.3266556656686, 55.3046526630094, 1.8094184580300012]`
- min: `[-2456.50634765625, -1783.636474609375, -366.0513000488281, -3.1415926535660867]`
- max: `[1060.57373046875, 895.2840576171875, 13.327319145202637, 3.141592653560866]`

## Action Statistics

| Dimension | Stats |
| --- | --- |
| vx | min=-28.998863, max=17.710327, mean=0.049569, std=2.544490, median=0.022626, q01=-4.906525, q99=4.913086 |
| vy | min=-17.254425, max=14.933552, mean=0.038484, std=2.416756, median=0.004649, q01=-4.903336, q99=4.903336 |
| vz | min=-4.991516, max=21.363218, mean=-0.034883, std=1.152112, median=0.000238, q01=-4.801053, q99=4.638823 |
| yaw_rate | min=-3.141522, max=3.141529, mean=-0.000786, std=0.282594, median=-0.000000, q01=-0.766448, q99=0.727875 |

Action normalization vectors:

- mean: `[0.04956907331952039, 0.03848436145998086, -0.034882607594981636, -0.000785809321538779]`
- std: `[2.544490491004062, 2.416755808151704, 1.152111724696342, 0.28259369204351903]`
- min: `[-28.998863220214844, -17.254425048828125, -4.99151611328125, -3.1415219680140978]`
- max: `[17.7103271484375, 14.933551788330078, 21.363218307495117, 3.1415293309385186]`

## Instruction Length

- characters: min=192.000000, max=730.000000, mean=343.911094, std=54.996825, median=339.000000, q01=237.000000, q99=489.000000

## Boundary

These statistics come from three small debug subsets only. Full training normalization must be recomputed from the actual training split on the 5090 stage before model training.
