# TravelUAV Action Chunk BC Baseline

## Result

- Status: `BC_ACTION_CHUNK_FULL_PASS`
- Model type: non-large-model MLP behavior cloning baseline
- Input: `state = [x, y, z, yaw]`
- Output: `action_chunk = [8, 4]`
- OpenVLA training started: `False`
- LoRA/OFT training started: `False`
- Diffusion Policy training started: `False`
- Real AirSim rollout: `False`

## Final Metrics

- Final epoch: `20`
- Final train MSE norm: `0.5569451669715855`
- Final val MSE norm: `0.6272119525820017`
- Final elapsed sec: `25.87`

## Best Validation

- Best epoch: `9`
- Best val MSE norm: `0.6243616007268429`

## Artifact

The checkpoint is intentionally not committed to git.

- Best checkpoint: `checkpoints/bc/traveluav_state_action_chunk_mlp_full_best.pt`
- Size bytes: `1628469`
- SHA256: `9dc3cbb6f4187def66f403c738b00791f640ebc0324d3cbf41682d334caad4a1`

## Conclusion

This is an offline supervised sequence baseline over existing TravelUAV trajectories. It is not a real AirSim rollout and not a large-model training run.
