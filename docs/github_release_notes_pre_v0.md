# GitHub Initial Upload Notes

## Repository Stage

This repository contains the first engineering stage of the VLA-UAV diffusion project.

## Completed

- TravelUAV subset conversion to UAV JSONL.
- UAV state/action adapter.
- OpenVLA-OFT code structure analysis.
- OpenVLA-OFT UAV dimension patch analysis.
- OpenVLA processor smoke.
- OpenVLA one-batch forward smoke.
- UAVJsonlDatasetForOpenVLAOFT dry run.
- Frozen OpenVLA UAV action-head pilot.
- State-only baseline.
- Per-dimension evaluation.
- Thesis method and pilot experiment drafts.

## Not Included

Large files are intentionally excluded:

- raw TravelUAV maps;
- external cloned repositories;
- OpenVLA/openvla-7b weights;
- HuggingFace cache;
- large checkpoints;
- auth files or secrets.

## Current Research Conclusion

The data route and model-stage smoke route are feasible.

However, the state-only baseline currently outperforms frozen OpenVLA features in the small pilot setting. This motivates future work on normalization, better OpenVLA feature selection, LoRA/OFT adaptation, Diffusion Policy, and RL expert trajectories.
