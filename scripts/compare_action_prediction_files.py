#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DIM_NAMES = ["vx", "vy", "vz", "yaw_rate"]


def load_predictions(path):
    targets = []
    preds = []
    rows = 0

    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            target = (
                r.get("target")
                or r.get("target_action_chunk")
                or r.get("action_chunk")
            )
            pred = (
                r.get("pred")
                or r.get("pred_action_chunk")
                or r.get("prediction")
                or r.get("predicted_action_chunk")
            )

            if target is None or pred is None:
                raise ValueError(f"{path}: row missing target/pred keys")

            target = np.asarray(target, dtype=np.float32)
            pred = np.asarray(pred, dtype=np.float32)

            if target.shape != pred.shape:
                raise ValueError(f"{path}: target shape {target.shape} != pred shape {pred.shape}")
            if target.shape[-1] != 4:
                raise ValueError(f"{path}: expected last dim 4, got {target.shape}")

            targets.append(target)
            preds.append(pred)
            rows += 1

    if not targets:
        raise ValueError(f"No rows loaded from {path}")

    return np.stack(targets), np.stack(preds), rows


def metrics_for(target, pred):
    err = pred - target
    abs_err = np.abs(err)
    mae = abs_err.mean(axis=(0, 1))
    rmse = np.sqrt((err ** 2).mean(axis=(0, 1)))
    return {
        "overall_mae": float(abs_err.mean()),
        "overall_rmse": float(np.sqrt((err ** 2).mean())),
        "per_dim_mae": {DIM_NAMES[i]: float(mae[i]) for i in range(4)},
        "per_dim_rmse": {DIM_NAMES[i]: float(rmse[i]) for i in range(4)},
        "rows": int(target.shape[0]),
        "action_chunk_shape": list(target.shape[1:]),
    }


def plot_grouped_bar(results, metric_key, out_path, title):
    labels = list(results.keys())
    x = np.arange(len(DIM_NAMES))
    width = 0.8 / max(1, len(labels))

    plt.figure(figsize=(12, 6))
    for i, label in enumerate(labels):
        values = [results[label][metric_key][d] for d in DIM_NAMES]
        plt.bar(x - 0.4 + width / 2 + i * width, values, width, label=label)

    plt.xticks(x, DIM_NAMES)
    plt.ylabel(metric_key)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def plot_overall(results, out_path):
    labels = list(results.keys())
    mae = [results[k]["overall_mae"] for k in labels]
    rmse = [results[k]["overall_rmse"] for k in labels]
    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x - width / 2, mae, width, label="MAE")
    plt.bar(x + width / 2, rmse, width, label="RMSE")
    plt.xticks(x, labels, rotation=15)
    plt.ylabel("error")
    plt.title("Overall action_chunk prediction error")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def markdown_report(results, out_dir):
    lines = []
    lines.append("# Action Head 3-Way Comparison Report")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("- `ACTION_HEAD_3WAY_COMPARISON_PASS`")
    lines.append("- full LoRA/OFT training: `false`")
    lines.append("- closed-loop simulation: `false`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| model | rows | overall MAE | overall RMSE |")
    lines.append("|---|---:|---:|---:|")
    for label, m in results.items():
        lines.append(f"| {label} | {m['rows']} | {m['overall_mae']:.6f} | {m['overall_rmse']:.6f} |")
    lines.append("")
    lines.append("## Per-Dimension MAE")
    lines.append("")
    lines.append("| model | vx | vy | vz | yaw_rate |")
    lines.append("|---|---:|---:|---:|---:|")
    for label, m in results.items():
        v = m["per_dim_mae"]
        lines.append(f"| {label} | {v['vx']:.6f} | {v['vy']:.6f} | {v['vz']:.6f} | {v['yaw_rate']:.6f} |")
    lines.append("")
    lines.append("## Per-Dimension RMSE")
    lines.append("")
    lines.append("| model | vx | vy | vz | yaw_rate |")
    lines.append("|---|---:|---:|---:|---:|")
    for label, m in results.items():
        v = m["per_dim_rmse"]
        lines.append(f"| {label} | {v['vx']:.6f} | {v['vy']:.6f} | {v['vz']:.6f} | {v['yaw_rate']:.6f} |")
    lines.append("")
    lines.append("## Plots")
    lines.append("")
    lines.append(f"- `{out_dir}/overall_error_bar.png`")
    lines.append(f"- `{out_dir}/per_dim_mae_bar.png`")
    lines.append(f"- `{out_dir}/per_dim_rmse_bar.png`")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This comparison evaluates action_chunk prediction on the same validation subset.")
    lines.append("The LoRA 100-step result verifies the trainable OpenVLA transfer path, but it should still be treated as a pilot result rather than final OpenVLA-OFT training.")
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", action="append", required=True)
    ap.add_argument("--label", action="append", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    if len(args.predictions) != len(args.label):
        raise ValueError("--predictions and --label counts must match")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    for label, path in zip(args.label, args.predictions):
        target, pred, rows = load_predictions(path)
        m = metrics_for(target, pred)
        m["path"] = path
        m["rows"] = rows
        results[label] = m

    plot_overall(results, out_dir / "overall_error_bar.png")
    plot_grouped_bar(results, "per_dim_mae", out_dir / "per_dim_mae_bar.png", "Per-dimension MAE")
    plot_grouped_bar(results, "per_dim_rmse", out_dir / "per_dim_rmse_bar.png", "Per-dimension RMSE")

    out_md = Path(args.out_md)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(markdown_report(results, out_dir), encoding="utf-8")

    print("WROTE", out_md)
    print("WROTE", out_dir)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    print("ACTION_HEAD_3WAY_COMPARISON_PASS")


if __name__ == "__main__":
    main()
