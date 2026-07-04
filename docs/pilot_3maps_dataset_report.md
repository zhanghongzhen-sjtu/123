# Pilot 3-Map Dataset Report

## Status

This is a pilot / sanity dataset, not the final OpenVLA-OFT training dataset.

## Split

- train: BrushifyCountryRoads + BrushifyUrban
- val: Carla_Town02

## Files

- data/processed/pilot_train_3maps.jsonl
- data/processed/pilot_val_3maps.jsonl
- data/processed/pilot_train_3maps_stats.json
- docs/pilot_train_3maps_stats.md
- docs/pilot_openvla_oft_adapter_smoke_report.md

## Purpose

This split can be used to test:

- data loading
- image path resolution
- instruction/state/action/action_chunk format
- action chunk shape
- normalization loading
- future action head smoke training

It cannot be used as final thesis evidence.

## Final Marker

- PILOT_DATA_READY
- NOT_FINAL_TRAINING_DATA
