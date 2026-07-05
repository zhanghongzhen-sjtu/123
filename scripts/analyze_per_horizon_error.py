#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DIM_NAMES = ["vx", "vy", "vz", "yaw_rate"]


def load_pred(path):
    targets, preds = [], []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            target = r.get("target") or r.get("target_action_chunk") or r.get("action_chunk")
            pred = r.get("pred") or r.get("pred_action_chunk") or r.get("prediction")
            targets.append(np.asarray(target, dtype=np.float32))
            preds.append(np.asarray(pred, dtype=np.float32))
    return np.stack(targets), np.stack(preds)


def metrics_by_horizon(target, pred):
    err = pred - target
    abs_err = np.abs(err)
    mae_h = abs_err.mean(axis=0)          # [H,4]
    rmse_h = np.sqrt((err ** 2).mean(axis=0))
    overall_mae_h = abs_err.mean(axis=(0, 2))
    overall_rmse_h = np.sqrt((err ** 2).mean(axis=(0, 2)))
    return mae_h, rmse_h, overall_mae_h, overall_rmse_h


def plot_overall(results, out_path):
    plt.figure(figsize=(10, 5))
    for label, r in results.items():
        h = np.arange(1, len(r["overall_mae_h"]) + 1)
        plt.plot(h, r["overall_mae_h"], marker="o", label=f"{label} MAE")
    plt.xlabel("action_chunk horizon step")
    plt.ylabel("overall MAE")
    plt.title("Per-horizon overall MAE")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def plot_dim(results, metric_key, out_path, title):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.reshape(-1)
    for d, ax in enumerate(axes):
        for label, r in results.items():
            arr = r[metric_key][:, d]
            h = np.arange(1, len(arr) + 1)
            ax.plot(h, arr, marker="o", label=label)
        ax.set_title(DIM_NAMES[d])
        ax.set_xlabel("horizon")
        ax.set_ylabel(metric_key)
        ax.grid(True, alpha=0.3)
    axes[0].legend()
    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", action="append", required=True)
    ap.add_argument("--label", action="append", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    if len(args.predictions) != len(args.label):
        raise ValueError("predictions and label count mismatch")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for label, path in zip(args.label, args.predictions):
        target, pred = load_pred(path)
        mae_h, rmse_h, overall_mae_h, overall_rmse_h = metrics_by_horizon(target, pred)
        results[label] = {
            "path": path,
            "rows": int(target.shape[0]),
            "horizon": int(target.shape[1]),
            "mae_h": mae_h,
            "rmse_h": rmse_h,
            "overall_mae_h": overall_mae_h,
            "overall_rmse_h": overall_rmse_h,
        }

    plot_overall(results, out_dir / "per_horizon_overall_mae.png")
    plot_dim(results, "mae_h", out_dir / "per_horizon_dim_mae.png", "Per-horizon per-dimension MAE")
    plot_dim(results, "rmse_h", out_dir / "per_horizon_dim_rmse.png", "Per-horizon per-dimension RMSE")

    lines = ["# Per-Horizon Action Chunk Error Analysis", ""]
    lines.append("## Status")
    lines.append("")
    lines.append("- `PER_HORIZON_ERROR_ANALYSIS_PASS`")
    lines.append("")
    lines.append("## Overall MAE By Horizon")
    lines.append("")
    header = "| model | " + " | ".join([f"h{i}" for i in range(1, 9)]) + " |"
    sep = "|---|" + "|".join(["---:"] * 8) + "|"
    lines.extend([header, sep])
    for label, r in results.items():
        vals = " | ".join(f"{x:.6f}" for x in r["overall_mae_h"])
        lines.append(f"| {label} | {vals} |")

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This analysis shows how action_chunk prediction error changes from near-term to farther-horizon actions.")
    lines.append("If errors grow with horizon, it motivates a sequence modeling module such as Diffusion Policy for low-level control.")
    lines.append("")
    lines.append("## Plots")
    lines.append("")
    for name in ["per_horizon_overall_mae.png", "per_horizon_dim_mae.png", "per_horizon_dim_rmse.png"]:
        lines.append(f"- `{out_dir / name}`")

    Path(args.out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("WROTE", args.out_md)
    print("WROTE", out_dir)
    print("PER_HORIZON_ERROR_ANALYSIS_PASS")


if __name__ == "__main__":
    main()
