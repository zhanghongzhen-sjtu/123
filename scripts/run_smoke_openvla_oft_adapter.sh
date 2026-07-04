#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m src.openvla_uav_transfer.checks.smoke_openvla_oft_adapter \
  --jsonl data/debug/traveluav_BrushifyCountryRoads_debug.jsonl \
  --image-root . \
  --stats data/debug/traveluav_3maps_stats.json \
  --normalize \
  --check-images \
  --batch-size 8 \
  --action-chunk-size 8 \
  --out docs/openvla_oft_adapter_smoke_report.md
