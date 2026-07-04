#!/usr/bin/env bash
set -euo pipefail

cd /root/autodl-tmp/vla-uav-diffusion

export HF_HOME=/root/autodl-tmp/hf-cache
export HF_HUB_DISABLE_XET=1
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

mkdir -p logs/pipeline logs/pilot docs checkpoints/uav_action_head data/debug/predictions

echo "===== STEP 1: check data ====="
python3 -m src.openvla_uav_transfer.checks.check_uav_jsonl \
  --jsonl data/processed/clean_train_timestamp_maps.jsonl \
  --image-root . \
  --max-show 0 | tee logs/pipeline/01_check_train.log

python3 -m src.openvla_uav_transfer.checks.check_uav_jsonl \
  --jsonl data/processed/clean_val_timestamp_maps.jsonl \
  --image-root . \
  --max-show 0 | tee logs/pipeline/02_check_val.log

echo "===== STEP 2: compute action stats ====="
python3 - <<'PY' | tee logs/pipeline/03_action_stats.log
import json
import numpy as np
from pathlib import Path

jsonl = Path("data/processed/clean_train_timestamp_maps.jsonl")
actions = []
with jsonl.open("r", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            actions.extend(json.loads(line)["action_chunk"])

arr = np.asarray(actions, dtype=np.float32)
stats = {
    "source": str(jsonl),
    "shape": list(arr.shape),
    "action_names": ["vx", "vy", "vz", "yaw_rate"],
    "mean": arr.mean(axis=0).tolist(),
    "std": np.maximum(arr.std(axis=0), 1e-6).tolist(),
    "min": arr.min(axis=0).tolist(),
    "max": arr.max(axis=0).tolist(),
}
Path("data/processed/clean_train_action_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(stats, ensure_ascii=False, indent=2))
print("ACTION_STATS_PASS")
PY

echo "===== STEP 3: state-only baseline ====="
python3 scripts/train_state_only_action_head_baseline.py \
  --train-jsonl data/processed/clean_train_timestamp_maps.jsonl \
  --val-jsonl data/processed/clean_val_timestamp_maps.jsonl \
  --max-train-rows 120 \
  --max-val-rows 64 \
  --batch-size 1 \
  --epochs 3 \
  --lr 1e-4 \
  --hidden-dim 256 \
  --out-json logs/pilot/state_only_action_head_baseline_report.json \
  --out-md docs/state_only_action_head_baseline_report.md \
  --ckpt checkpoints/uav_action_head/state_only_action_head_baseline.pt \
  | tee logs/pipeline/04_state_only_baseline.log

echo "===== STEP 4: state-only normalized baseline ====="
python3 scripts/train_state_only_action_head_normalized.py \
  --train-jsonl data/processed/clean_train_timestamp_maps.jsonl \
  --val-jsonl data/processed/clean_val_timestamp_maps.jsonl \
  --stats data/processed/clean_train_action_stats.json \
  --max-train-rows 120 \
  --max-val-rows 64 \
  --batch-size 1 \
  --epochs 3 \
  --lr 1e-4 \
  --hidden-dim 256 \
  --out-json logs/pilot/state_only_action_head_normalized_report.json \
  --out-md docs/state_only_action_head_normalized_report.md \
  --ckpt checkpoints/uav_action_head/state_only_action_head_normalized.pt \
  | tee logs/pipeline/05_state_only_normalized.log

echo "===== STEP 5: frozen OpenVLA action head pilot ====="
python3 scripts/train_frozen_openvla_uav_action_head_pilot.py \
  --train-jsonl data/processed/clean_train_timestamp_maps.jsonl \
  --val-jsonl data/processed/clean_val_timestamp_maps.jsonl \
  --image-root . \
  --model-id openvla/openvla-7b \
  --cache-dir /root/autodl-tmp/hf-cache \
  --batch-size 1 \
  --max-train-rows 120 \
  --max-val-rows 64 \
  --epochs 3 \
  --lr 1e-4 \
  --hidden-dim 256 \
  --val-max-batches 32 \
  --out-json logs/pilot/frozen_openvla_uav_action_head_pilot_report.json \
  --out-md docs/frozen_openvla_uav_action_head_pilot_report.md \
  --ckpt checkpoints/uav_action_head/frozen_openvla_uav_action_head_pilot.pt \
  | tee logs/pipeline/06_frozen_openvla_pilot.log

echo "===== STEP 6: frozen OpenVLA normalized pilot ====="
python3 scripts/train_frozen_openvla_uav_action_head_normalized.py \
  --train-jsonl data/processed/clean_train_timestamp_maps.jsonl \
  --val-jsonl data/processed/clean_val_timestamp_maps.jsonl \
  --stats data/processed/clean_train_action_stats.json \
  --image-root . \
  --model-id openvla/openvla-7b \
  --cache-dir /root/autodl-tmp/hf-cache \
  --batch-size 1 \
  --max-train-rows 120 \
  --max-val-rows 64 \
  --epochs 3 \
  --lr 1e-4 \
  --hidden-dim 256 \
  --val-max-batches 64 \
  --out-json logs/pilot/frozen_openvla_uav_action_head_normalized_report.json \
  --out-md docs/frozen_openvla_uav_action_head_normalized_report.md \
  --ckpt checkpoints/uav_action_head/frozen_openvla_uav_action_head_normalized.pt \
  | tee logs/pipeline/07_frozen_openvla_normalized.log

echo "===== STEP 7: per-dim eval ====="
python3 scripts/eval_action_head_per_dim.py \
  --val-jsonl data/processed/clean_val_timestamp_maps.jsonl \
  --image-root . \
  --max-rows 64 \
  --batch-size 1 \
  --model-id openvla/openvla-7b \
  --cache-dir /root/autodl-tmp/hf-cache \
  --state-ckpt checkpoints/uav_action_head/state_only_action_head_baseline.pt \
  --openvla-ckpt checkpoints/uav_action_head/frozen_openvla_uav_action_head_pilot.pt \
  --out-json logs/pilot/action_head_per_dim_eval.json \
  --out-md docs/action_head_per_dim_eval.md \
  | tee logs/pipeline/08_per_dim_eval.log

echo "===== STEP 8: export predictions ====="
python3 scripts/export_state_only_predictions.py \
  --jsonl data/processed/clean_val_timestamp_maps.jsonl \
  --ckpt checkpoints/uav_action_head/state_only_action_head_baseline.pt \
  --max-rows 64 \
  --out data/debug/predictions/state_only_val_predictions.jsonl \
  | tee logs/pipeline/09_export_state_predictions.log

python3 scripts/export_frozen_openvla_predictions.py \
  --jsonl data/processed/clean_val_timestamp_maps.jsonl \
  --image-root . \
  --model-id openvla/openvla-7b \
  --cache-dir /root/autodl-tmp/hf-cache \
  --ckpt checkpoints/uav_action_head/frozen_openvla_uav_action_head_pilot.pt \
  --max-rows 64 \
  --batch-size 1 \
  --out data/debug/predictions/frozen_openvla_val_predictions.jsonl \
  | tee logs/pipeline/10_export_openvla_predictions.log

echo "PILOT_PIPELINE_PASS"
