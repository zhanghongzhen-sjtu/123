#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m src.openvla_uav_transfer.checks.audit_uav_jsonl \
  --jsonl \
    data/debug/traveluav_BrushifyCountryRoads_debug.jsonl \
    data/debug/traveluav_BrushifyUrban_debug.jsonl \
    data/debug/traveluav_Carla_Town02_debug.jsonl \
  --image-root . \
  --out docs/traveluav_3maps_audit.md

"$PYTHON_BIN" -m src.openvla_uav_transfer.checks.audit_uav_jsonl \
  --jsonl data/debug/traveluav_3maps_debug.jsonl \
  --image-root . \
  --out docs/traveluav_3maps_debug_audit.md
