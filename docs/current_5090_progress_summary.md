# Current 5090 Progress Summary

## Completed

- TravelUAV real-data conversion and validation.
- OpenVLA processor smoke test.
- Frozen OpenVLA feature + UAV action head pilot.
- LoRA + UAV action head pilot training.
- Full clean 5000-step LoRA pilot result.
- Action prediction comparison reports and figures.
- Per-horizon action_chunk analysis.
- Toy PPO UAV expert trajectory generation.
- TravelUAV AirSim simulator contract check.

## Important Status

- CUDA RTX 5090 training works.
- OpenVLA / LoRA / action-head experiments work.
- Real TravelUAV AirSim closed-loop simulation is blocked on AutoDL because Vulkan only detects llvmpipe CPU rendering, not NVIDIA Vulkan.
- Real AirSim trajectory generation should be moved to local Windows RTX 3060 or another Vulkan-capable GPU environment.

## Not Included In Git

- Raw TravelUAV data.
- Checkpoints.
- LoRA adapters.
- Model weights.
- Large prediction JSONL files.
- Logs.
