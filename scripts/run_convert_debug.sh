#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m src.openvla_uav_transfer.converters.convert_traveluav_to_openvla_jsonl \
  --traveluav-root external/TravelUAV \
  --dataset-root data/raw/TravelUAV \
  --out data/debug/traveluav_debug.jsonl \
  --max-episodes 3 \
  --max-steps-per-episode 20 \
  --dt 1.0 \
  --action-chunk-size 8
