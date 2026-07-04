#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m src.openvla_uav_transfer.converters.inspect_traveluav \
  --traveluav-root external/TravelUAV \
  --dataset-root data/raw/TravelUAV \
  --out docs/traveluav_data_notes.md
