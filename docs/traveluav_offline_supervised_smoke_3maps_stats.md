# TravelUAV 3-Map Statistics

This report is generated from lightweight debug JSONL files. It is suitable for schema validation and future normalization planning, but it is not a final full-dataset training statistic.

## Inputs
- `data/offline/traveluav_offline_supervised_smoke_3maps.jsonl`: `1582` rows

## Summary
- Schema version: `uav_openvla_jsonl_v0.1`
- Rows: `1582`
- dt sources: `{'timestamp': 1582}`
- action chunk lengths: `{'8': 1582}`

## Per-Map Counts

| Map | Rows | Episodes |
| --- | ---: | ---: |
| BrushifyCountryRoads | 715 | 10 |
| BrushifyUrban | 487 | 10 |
| Carla_Town02 | 380 | 10 |

## Timing

- `dt`: min=0.981021, max=5.007107, mean=4.931792, std=0.371397, median=4.989106, q01=2.991064, q99=5.001107

## State Statistics

| Dimension | Stats |
| --- | --- |
| x | min=-1006.166016, max=736.347168, mean=-268.206739, std=397.274031, median=-369.169525, q01=-995.063915, q99=658.631370 |
| y | min=-1774.394043, max=316.671875, mean=-423.316807, std=488.861223, median=-481.119690, q01=-1774.394043, q99=304.556834 |
| z | min=-155.658356, max=-1.535330, mean=-50.063866, std=51.491716, median=-17.921608, q01=-155.656782, q99=-1.654397 |
| yaw | min=-3.141593, max=3.141593, mean=-0.024856, std=1.748952, median=-0.025227, q01=-3.100886, q99=3.114673 |

State normalization vectors:

- mean: `[-268.20673926820797, -423.3168071115062, -50.06386598345603, -0.024856025488059243]`
- std: `[397.27403099925846, 488.86122300709997, 51.49171642611169, 1.7489524782480934]`
- min: `[-1006.166015625, -1774.39404296875, -155.65835571289062, -3.1415926528095643]`
- max: `[736.34716796875, 316.671875, -1.535329818725586, 3.1415926494991995]`

## Action Statistics

| Dimension | Stats |
| --- | --- |
| vx | min=-0.996886, max=0.996886, mean=0.087580, std=0.682102, median=0.091158, q01=-0.996886, q99=0.996886 |
| vy | min=-0.996886, max=0.991800, mean=-0.057548, std=0.599824, median=-0.012265, q01=-0.986714, q99=0.986714 |
| vz | min=-0.993184, max=1.001972, mean=-0.008481, std=0.351387, median=0.000520, q01=-0.991800, q99=0.977329 |
| yaw_rate | min=-0.622554, max=0.626606, mean=-0.001931, std=0.077402, median=-0.000000, q01=-0.375181, q99=0.215416 |

Action normalization vectors:

- mean: `[0.08758017370968595, -0.057547533369623434, -0.008481314710737403, -0.0019313380489057528]`
- std: `[0.6821022533313573, 0.5998238544621772, 0.35138718595514434, 0.07740201770106317]`
- min: `[-0.9968862851759164, -0.9968862851759164, -0.9931841338967482, -0.6225535983815065]`
- max: `[0.9968862851759164, 0.9918001306597127, 1.00197243969212, 0.6266060716642696]`

## Instruction Length

- characters: min=229.000000, max=412.000000, mean=318.833123, std=48.511862, median=309.000000, q01=229.000000, q99=412.000000

## Boundary

These statistics come from three small debug subsets only. Full training normalization must be recomputed from the actual training split on the 5090 stage before model training.
