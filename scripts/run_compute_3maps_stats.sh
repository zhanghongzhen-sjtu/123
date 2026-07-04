#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m src.openvla_uav_transfer.checks.compute_uav_stats \
  --jsonl \
    data/debug/traveluav_BrushifyCountryRoads_debug.jsonl \
    data/debug/traveluav_BrushifyUrban_debug.jsonl \
    data/debug/traveluav_Carla_Town02_debug.jsonl \
  --out-json data/debug/traveluav_3maps_stats.json \
  --out-md docs/traveluav_3maps_stats.md
