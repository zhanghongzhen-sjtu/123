# Full Data Training Plan

## Current Status

Completed:

- Cloud 5090 environment check
- 3-map raw data restore
- cloud raw -> JSONL conversion
- cloud JSONL validation
- pilot train/val split
- pilot stats
- dataset loader smoke test
- OpenVLA-OFT-style collator smoke test
- tiny action-head smoke training
- HuggingFace TravelUAV archive listing

## Available Archive Groups

HuggingFace TravelUAV currently exposes 22 archive groups:

- BattlefieldKitDesert
- BrushifyCountryRoads
- BrushifyForestPack
- BrushifyUrban
- Carla_Town01
- Carla_Town02
- Carla_Town03
- Carla_Town04
- Carla_Town05
- Carla_Town06
- Carla_Town07
- Carla_Town10HD
- Carla_Town15
- Japanese_Street
- London_Street
- ModernCityMap
- ModularPark
- NYCEnvironmentMegapa
- NewYorkCity
- NordicHarbour
- TropicalIsland
- WesterTown

## Staged Scaling

Do not jump directly from 3-map pilot to full OpenVLA-OFT training.

Use staged scaling:

1. 3-map pilot
2. 7-map medium subset
3. larger multi-map subset or full dataset
4. OpenVLA-OFT model loading
5. action-head / LoRA-OFT experiments

## Proposed 7-Map Medium Subset

Already available:

- BrushifyCountryRoads
- BrushifyUrban
- Carla_Town02

Download next:

- Carla_Town01
- Carla_Town03
- Carla_Town04
- Carla_Town05

Proposed split:

train:

- BrushifyCountryRoads
- BrushifyUrban
- Carla_Town01
- Carla_Town03
- Carla_Town04

val:

- Carla_Town02
- Carla_Town05

## Why This Split

- mixes Brushify and CARLA style maps
- keeps Carla_Town02 as already validated val map
- adds Carla_Town05 as another validation map
- avoids downloading all 22 maps before the adapter and training code are stable

## Before OpenVLA-OFT Loading

Must complete for the 7-map subset:

- raw archives complete
- extraction complete
- JSONL conversion
- train/val split JSONL
- train stats
- image-root validation
- action recompute validation
- dataset loader smoke
- collator smoke
- optional tiny action-head smoke training

Only after these pass:

- load OpenVLA-OFT / openvla-7b
- start action head or LoRA/OFT experiments

## Current Conclusion

- PILOT_DATA_READY
- PILOT_ACTION_HEAD_SMOKE_PASS
- MEDIUM_SUBSET_PLANNED
- FULL_DATA_NOT_READY
- OPENVLA_TRAINING_NOT_STARTED
