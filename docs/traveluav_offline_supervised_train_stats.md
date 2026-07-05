# TravelUAV 3-Map Statistics

This report is generated from lightweight debug JSONL files. It is suitable for schema validation and future normalization planning, but it is not a final full-dataset training statistic.

## Inputs
- `data/offline/splits/traveluav_offline_supervised_train.jsonl`: `298304` rows

## Summary
- Schema version: `uav_openvla_jsonl_v0.1`
- Rows: `298304`
- dt sources: `{'fallback_arg': 171805, 'timestamp': 126499}`
- action chunk lengths: `{'8': 298304}`

## Per-Map Counts

| Map | Rows | Episodes |
| --- | ---: | ---: |
| BrushifyCountryRoads | 18454 | 291 |
| BrushifyUrban | 23415 | 401 |
| Carla_Town01 | 40772 | 860 |
| Carla_Town02 | 17213 | 526 |
| Carla_Town03 | 25457 | 512 |
| Carla_Town04 | 31030 | 588 |
| Carla_Town05 | 23735 | 465 |
| Carla_Town06 | 18370 | 350 |
| Carla_Town07 | 16010 | 398 |
| Carla_Town10HD | 41888 | 898 |
| Carla_Town15 | 41960 | 678 |

## Timing

- `dt`: min=0.540012, max=5.679121, mean=2.653977, std=1.943657, median=1.000000, q01=1.000000, q99=4.998107

## State Statistics

| Dimension | Stats |
| --- | --- |
| x | min=-2456.506348, max=1060.573730, mean=-18.905053, std=414.245950, median=35.192646, q01=-2013.222758, q99=894.286655 |
| y | min=-1783.636475, max=895.284058, mean=-9.218444, std=349.822769, median=40.094883, q01=-1355.439414, q99=729.862533 |
| z | min=-366.051300, max=13.327319, mean=-44.194441, std=55.448353, median=-17.644957, q01=-188.915430, q99=-0.130456 |
| yaw | min=-3.141593, max=3.141593, mean=0.030554, std=1.810394, median=0.013136, q01=-3.114432, q99=3.114377 |

State normalization vectors:

- mean: `[-18.905053307846526, -9.218444023294397, -44.1944408721605, 0.030553939216945568]`
- std: `[414.245949944548, 349.82276865430384, 55.44835288893365, 1.8103936693962572]`
- min: `[-2456.50634765625, -1783.636474609375, -366.0513000488281, -3.1415926535660867]`
- max: `[1060.57373046875, 895.2840576171875, 13.327319145202637, 3.141592653560866]`

## Action Statistics

| Dimension | Stats |
| --- | --- |
| vx | min=-25.478075, max=17.710327, mean=0.030984, std=2.538347, median=0.017993, q01=-4.906738, q99=4.913086 |
| vy | min=-17.254425, max=14.933552, mean=0.033613, std=2.418227, median=0.004115, q01=-4.903336, q99=4.903336 |
| vz | min=-4.991516, max=21.363218, mean=-0.034179, std=1.151494, median=0.000235, q01=-4.795460, q99=4.646631 |
| yaw_rate | min=-3.141490, max=3.141529, mean=-0.001443, std=0.280910, median=-0.000000, q01=-0.761309, q99=0.700738 |

Action normalization vectors:

- mean: `[0.030983938966805485, 0.033613208537051145, -0.03417930897020924, -0.0014431375014761286]`
- std: `[2.5383467891622913, 2.4182272217504934, 1.1514942832537325, 0.2809096015174054]`
- min: `[-25.47807502746582, -17.254425048828125, -4.99151611328125, -3.1414896711594213]`
- max: `[17.7103271484375, 14.933551788330078, 21.363218307495117, 3.1415293309385186]`

## Instruction Length

- characters: min=192.000000, max=561.000000, mean=343.702716, std=54.985271, median=339.000000, q01=237.000000, q99=492.000000

## Boundary

These statistics come from three small debug subsets only. Full training normalization must be recomputed from the actual training split on the 5090 stage before model training.
