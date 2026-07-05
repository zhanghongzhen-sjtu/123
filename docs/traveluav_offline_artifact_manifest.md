# TravelUAV Offline Artifact Manifest

## Status

- `TRAVELUAV_OFFLINE_ARTIFACT_MANIFEST_READY`
- `LARGE_ARTIFACTS_NOT_COMMITTED_TO_GITHUB`
- `REAL_AIRSIM_ROLLOUT_NOT_INCLUDED`

## Artifacts

| Path | Exists | Size MB | SHA256 |
| --- | --- | ---: | --- |
| `data/offline/traveluav_offline_supervised_allmaps_1000ep.jsonl` | `True` | 703.0 | `b21a4337fa3759da98268de61250ad5f2e875a784116f91d912455a2d26b9e46` |
| `data/offline/splits/traveluav_offline_supervised_train.jsonl` | `True` | 635.15 | `4c689d2ac769f987819929bb03644f86ace0cf76c3f6144b73a117ef17db559b` |
| `data/offline/splits/traveluav_offline_supervised_val.jsonl` | `True` | 67.85 | `c837936ce2176a5351867321cec90a5f6d0a936be099fa285ac9ad46703087a3` |
| `checkpoints/bc/traveluav_state_action_mlp_split_full.pt` | `True` | 0.39 | `ac4788ea4cba789bf7cffd59af31abf532a61f1e51b12f2e033bf170731e6911` |
| `checkpoints/bc/traveluav_state_action_mlp_split_full_best.pt` | `True` | 0.39 | `d880189b9af3ab7ef74e9e071bd2d3355b016ce43e3c4269228b967eb37a9d65` |

## Notes

- The JSONL files and checkpoints are kept on the 5090 filesystem or external storage.
- GitHub contains reports/statistics/manifests only.
- These are offline supervised behavior-cloning artifacts, not online AirSim RL expert trajectories.
