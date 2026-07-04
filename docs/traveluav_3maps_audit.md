# TravelUAV 3-Map JSONL Audit

## Inputs
- `data/debug/traveluav_BrushifyCountryRoads_debug.jsonl`
- `data/debug/traveluav_BrushifyUrban_debug.jsonl`
- `data/debug/traveluav_Carla_Town02_debug.jsonl`

## Summary
- Rows: `174`
- Maps: `3`
- Episodes: `9`
- Image root checked: `.`
- Issues: `none`

## Per-Map Counts

| Map | Rows | Episodes |
| --- | ---: | ---: |
| BrushifyCountryRoads | 60 | 3 |
| BrushifyUrban | 60 | 3 |
| Carla_Town02 | 54 | 3 |

## Timing
- `dt`: min=4.164089, max=5.004107, mean=4.966554, median=4.989106
- frame delta: min=5.000000, max=5.000000, mean=5.000000, median=5.000000
- dt sources: `{'timestamp': 174}`

## Action Statistics

| Dimension | Stats |
| --- | --- |
| vx | min=-0.991800, max=0.996886, mean=-0.135667, median=-0.109453 |
| vy | min=-0.991800, max=0.986714, mean=-0.183105, median=0.000000 |
| vz | min=-0.991800, max=0.011324, mean=-0.119726, median=0.003008 |
| yaw_rate | min=-0.532123, max=0.523692, mean=-0.006232, median=-0.000000 |

## Raw Velocity Consistency

The converted action velocity is compared with the current raw log `linear_velocity` and `angular_velocity[2]`. The first frame of an episode often has zero raw velocity, so nonzero-only errors are also reported.

| Quantity | All rows mean abs error | Nonzero raw rows mean abs error |
| --- | ---: | ---: |
| vx vs raw linear | 0.041517 | 0.015947 |
| vy vs raw linear | 0.033459 | 0.017164 |
| vz vs raw linear | 0.025486 | 0.012027 |
| yaw_rate vs raw angular z | 0.024688 | 0.010528 |

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
