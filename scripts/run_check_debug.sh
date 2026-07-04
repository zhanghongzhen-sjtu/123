#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m src.openvla_uav_transfer.checks.check_uav_jsonl \
  --jsonl data/debug/traveluav_debug.jsonl \
  --max-show 5
