#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
PYTHON_BIN="${PYTHON_BIN:-python3}"

"$PYTHON_BIN" -m src.openvla_uav_transfer.checks.check_pseudo_config \
  --config configs/openvla_oft_uav_debug.yaml \
  --out docs/openvla_oft_uav_pseudo_config_check_report.md
