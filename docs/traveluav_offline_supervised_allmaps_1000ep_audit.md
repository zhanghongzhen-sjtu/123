# TravelUAV 3-Map JSONL Audit

## Inputs
- `data/offline/traveluav_offline_supervised_allmaps_1000ep.jsonl`

## Summary
- Rows: `330202`
- Maps: `11`
- Episodes: `6631`
- Image root checked: `.`
- Issues: `none`

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
- `dt`: min=0.540012, max=5.679121, mean=2.649162, median=1.000000
- frame delta: min=1.000000, max=5.000000, mean=4.959416, median=5.000000
- dt sources: `{'timestamp': 139626, 'fallback_arg': 190576}`

## Action Statistics

| Dimension | Stats |
| --- | --- |
| vx | min=-28.998863, max=17.710327, mean=0.049569, median=0.022626 |
| vy | min=-17.254425, max=14.933552, mean=0.038484, median=0.004649 |
| vz | min=-4.991516, max=21.363218, mean=-0.034883, median=0.000238 |
| yaw_rate | min=-3.141522, max=3.141529, mean=-0.000786, median=-0.000000 |

## Raw Velocity Consistency

The converted action velocity is compared with the current raw log `linear_velocity` and `angular_velocity[2]`. The first frame of an episode often has zero raw velocity, so nonzero-only errors are also reported.

| Quantity | All rows mean abs error | Nonzero raw rows mean abs error |
| --- | ---: | ---: |
| vx vs raw linear | 0.029864 | 0.021762 |
| vy vs raw linear | 0.029049 | 0.022045 |
| vz vs raw linear | 0.034586 | 0.028680 |
| yaw_rate vs raw angular z | 0.023063 | 0.017512 |

## Sample Rows

```json
{
  "map": "BrushifyCountryRoads",
  "episode_id": "0008c004-9c02-40d3-928f-b7228c17a39d",
  "step_id": 0,
  "frame": 0,
  "next_frame": 5,
  "dt": 4.986106368,
  "dt_source": "timestamp",
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
  "image": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/frontcamera/000000.png"
}
```
```json
{
  "map": "BrushifyCountryRoads",
  "episode_id": "0008c004-9c02-40d3-928f-b7228c17a39d",
  "step_id": 1,
  "frame": 5,
  "next_frame": 10,
  "dt": 4.992106496,
  "dt_source": "timestamp",
  "state": [
    -542.2400512695312,
    -456.2330322265625,
    -42.26011657714844,
    -1.9670469068200325
  ],
  "action": [
    -0.31015761482464976,
    -0.742254561541985,
    -0.5689951970008263,
    -0.01468905933022172
  ],
  "image": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/frontcamera/000005.png"
}
```
```json
{
  "map": "BrushifyCountryRoads",
  "episode_id": "0008c004-9c02-40d3-928f-b7228c17a39d",
  "step_id": 2,
  "frame": 10,
  "next_frame": 15,
  "dt": 4.992106496,
  "dt_source": "timestamp",
  "state": [
    -543.7883911132812,
    -459.9384460449219,
    -45.10060119628906,
    -2.0403762553225615
  ],
  "action": [
    -0.4705426507466679,
    -0.8231928858142643,
    -0.13170358706216417,
    -0.01791959115065642
  ],
  "image": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/frontcamera/000010.png"
}
```
