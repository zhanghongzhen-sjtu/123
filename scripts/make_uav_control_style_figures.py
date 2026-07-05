#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


DIMS = ["vx", "vy", "vz", "yaw_rate"]


def load_pred(path):
    targets, preds = [], []
    meta = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            target = r.get("target") or r.get("target_action_chunk") or r.get("action_chunk")
            pred = r.get("pred") or r.get("pred_action_chunk") or r.get("prediction")
            targets.append(np.asarray(target, dtype=np.float32))
            preds.append(np.asarray(pred, dtype=np.float32))
            meta.append((r.get("episode_id"), r.get("step_id")))
    return np.stack(targets), np.stack(preds), meta


def flatten_chunks(x):
    return x.reshape(-1, x.shape[-1])


def moving_average(x, w=25):
    x = np.asarray(x, dtype=np.float32)
    if len(x) == 0:
        return x
    w = int(max(1, min(w, len(x))))
    kernel = np.ones(w, dtype=np.float32) / w
    y = np.convolve(x, kernel, mode="same")
    if len(y) > len(x):
        y = y[:len(x)]
    elif len(y) < len(x):
        y = np.pad(y, (0, len(x) - len(y)), mode="edge")
    return y


def plot_action_tracking(target, preds, out):
    t = flatten_chunks(target)
    pred_flat = {k: flatten_chunks(v) for k, v in preds.items()}
    n = min(len(t), 2500)
    x = np.arange(n)

    fig, axes = plt.subplots(4, 1, figsize=(16, 10), sharex=True)
    colors = {
        "target": "black",
        "state_only": "#4C78A8",
        "frozen_openvla": "#F58518",
        "lora_full_5000step": "#54A24B",
    }

    for d, ax in enumerate(axes):
        ax.plot(x, t[:n, d], color=colors["target"], linewidth=1.4, label="target")
        for name, arr in pred_flat.items():
            ax.plot(x, arr[:n, d], linewidth=1.0, alpha=0.8, label=name, color=colors.get(name))
        ax.set_ylabel(DIMS[d])
        ax.grid(True, alpha=0.25)
        if d == 0:
            ax.legend(ncol=4, fontsize=9)
    axes[-1].set_xlabel("flattened validation action step")
    fig.suptitle("UAV Action Sequence Tracking")
    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def plot_lora_control_panel(target, pred, out):
    t = flatten_chunks(target)
    p = flatten_chunks(pred)
    n = min(len(t), 2500)
    x = np.arange(n)
    err = np.abs(p[:n] - t[:n])

    fig, axes = plt.subplots(2, 2, figsize=(16, 9))

    ax = axes[0, 0]
    for i, d in enumerate(["vx", "vy", "vz"]):
        ax.plot(x, t[:n, i], linewidth=1.1, label=f"target {d}")
        ax.plot(x, p[:n, i], linewidth=0.9, linestyle="--", label=f"pred {d}")
    speed_t = np.linalg.norm(t[:n, :3], axis=1)
    speed_p = np.linalg.norm(p[:n, :3], axis=1)
    speed_t_ma = moving_average(speed_t)
    speed_p_ma = moving_average(speed_p)
    x_speed = np.arange(len(speed_t_ma))
    ax.plot(x_speed, speed_t_ma, color="black", linewidth=2.0, label="target speed MA")
    ax.plot(x_speed, speed_p_ma, color="gray", linewidth=2.0, linestyle="--", label="pred speed MA")
    ax.set_title("Velocity Components")
    ax.set_ylabel("velocity")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=7, ncol=2)

    ax = axes[0, 1]
    ax.plot(x, t[:n, 3], color="black", linewidth=1.2, label="target yaw_rate")
    ax.plot(x, p[:n, 3], color="#54A24B", linewidth=1.0, label="pred yaw_rate")
    ax.set_title("Yaw Rate")
    ax.set_ylabel("yaw_rate")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    for i, d in enumerate(DIMS):
        e_ma = moving_average(err[:, i], 35)
        ax.plot(np.arange(len(e_ma)), e_ma, linewidth=1.5, label=d)
    ax.set_title("Absolute Error Moving Average")
    ax.set_xlabel("flattened validation action step")
    ax.set_ylabel("|error|")
    ax.grid(True, alpha=0.25)
    ax.legend(ncol=4, fontsize=8)

    ax = axes[1, 1]
    cum = np.cumsum(np.mean(err, axis=1))
    ax.plot(x, cum, color="#E45756", linewidth=1.8)
    ax.set_title("Cumulative Mean Absolute Error")
    ax.set_xlabel("flattened validation action step")
    ax.set_ylabel("cumulative MAE")
    ax.grid(True, alpha=0.25)

    fig.suptitle("LoRA Full 5000-Step UAV Control-Style Prediction View")
    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def plot_scatter_fit(target, pred, out):
    t = flatten_chunks(target)
    p = flatten_chunks(pred)
    max_points = min(len(t), 12000)
    idx = np.linspace(0, len(t) - 1, max_points).astype(int)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.reshape(-1)

    for i, ax in enumerate(axes):
        tt = t[idx, i]
        pp = p[idx, i]
        ax.scatter(tt, pp, s=4, alpha=0.25, color="#4C78A8")
        lo = min(tt.min(), pp.min())
        hi = max(tt.max(), pp.max())
        ax.plot([lo, hi], [lo, hi], color="red", linewidth=1.5, label="y=x")
        if len(tt) > 1:
            corr = np.corrcoef(tt, pp)[0, 1]
        else:
            corr = np.nan
        ax.set_title(f"{DIMS[i]} target vs prediction (r={corr:.3f})")
        ax.set_xlabel("target")
        ax.set_ylabel("prediction")
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def plot_error_distribution(target, preds, out):
    t = flatten_chunks(target)
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axes = axes.reshape(-1)

    for d, ax in enumerate(axes):
        for name, pred in preds.items():
            p = flatten_chunks(pred)
            e = np.abs(p[:, d] - t[:, d])
            e = e[np.isfinite(e)]
            ax.hist(e, bins=70, alpha=0.45, density=True, label=name)
        ax.set_title(f"{DIMS[d]} absolute error distribution")
        ax.set_xlabel("|error|")
        ax.set_ylabel("density")
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(out, dpi=220)
    plt.close()


def main():
    out_dir = Path("data/debug/plots/uav_control_style")
    out_dir.mkdir(parents=True, exist_ok=True)

    target, state_pred, _ = load_pred("data/debug/predictions/state_only_full_clean_val_predictions.jsonl")
    _, frozen_pred, _ = load_pred("data/debug/predictions/frozen_openvla_full_clean_val_predictions.jsonl")
    _, lora_pred, _ = load_pred("data/debug/predictions/lora_full_clean_5000step_val_predictions.jsonl")

    preds = {
        "state_only": state_pred,
        "frozen_openvla": frozen_pred,
        "lora_full_5000step": lora_pred,
    }

    plot_action_tracking(target, preds, out_dir / "action_sequence_tracking.png")
    plot_lora_control_panel(target, lora_pred, out_dir / "lora_control_panel.png")
    plot_scatter_fit(target, lora_pred, out_dir / "lora_target_prediction_scatter.png")
    plot_error_distribution(target, preds, out_dir / "absolute_error_distribution.png")

    report = Path("docs/uav_control_style_figures_report.md")
    report.write_text(
        "# UAV Control-Style Figures Report\n\n"
        "## Figures\n\n"
        "- `data/debug/plots/uav_control_style/action_sequence_tracking.png`\n"
        "- `data/debug/plots/uav_control_style/lora_control_panel.png`\n"
        "- `data/debug/plots/uav_control_style/lora_target_prediction_scatter.png`\n"
        "- `data/debug/plots/uav_control_style/absolute_error_distribution.png`\n\n"
        "## Interpretation\n\n"
        "These figures visualize action prediction as UAV control time-series rather than only aggregate bars. "
        "They are intended for thesis presentation and qualitative analysis of action tracking, error accumulation, and prediction-target alignment.\n",
        encoding="utf-8",
    )

    print("WROTE", out_dir)
    print("WROTE", report)
    print("UAV_CONTROL_STYLE_FIGURES_PASS")


if __name__ == "__main__":
    main()
