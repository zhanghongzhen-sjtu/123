import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DIMS = ["vx", "vy", "vz", "yaw_rate"]

PRED_FILES = {
    "state_only": "data/debug/predictions/state_only_full_clean_val_predictions.jsonl",
    "frozen_openvla": "data/debug/predictions/frozen_openvla_full_clean_val_predictions.jsonl",
    "lora_full_5000step": "data/debug/predictions/lora_full_clean_5000step_val_predictions.jsonl",
}

OUT_DIR = Path("data/debug/plots/clean_action_lines")
REPORT = Path("docs/clean_action_line_figures_report.md")


def first_existing(row, keys):
    for k in keys:
        if k in row:
            return row[k]
    return None


def extract_arrays(row):
    target = first_existing(row, [
        "target", "target_action_chunk", "target_actions",
        "action_chunk", "actions"
    ])
    pred = first_existing(row, [
        "prediction", "pred", "pred_action_chunk", "pred_actions",
        "action_prediction", "predicted_action_chunk"
    ])

    if isinstance(target, dict):
        target = first_existing(target, ["action_chunk", "actions", "action"])
    if isinstance(pred, dict):
        pred = first_existing(pred, ["action_chunk", "actions", "action"])

    if target is None or pred is None:
        raise KeyError(f"Cannot find target/pred keys in row keys={list(row.keys())}")

    target = np.asarray(target, dtype=np.float32)
    pred = np.asarray(pred, dtype=np.float32)

    if target.ndim == 1:
        target = target.reshape(1, -1)
    if pred.ndim == 1:
        pred = pred.reshape(1, -1)

    target = target[:, :4]
    pred = pred[:, :4]
    return target, pred


def load_prediction_file(path):
    targets, preds = [], []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            t, p = extract_arrays(row)
            targets.append(t)
            preds.append(p)

    if not targets:
        raise RuntimeError(f"No rows loaded from {path}")

    return np.concatenate(targets, axis=0), np.concatenate(preds, axis=0)


def bin_mean(arr, bins=180):
    arr = np.asarray(arr, dtype=np.float32)
    n = len(arr)
    if n <= bins:
        return arr
    edges = np.linspace(0, n, bins + 1, dtype=int)
    out = []
    for a, b in zip(edges[:-1], edges[1:]):
        if b <= a:
            continue
        out.append(np.nanmean(arr[a:b], axis=0))
    return np.asarray(out, dtype=np.float32)


def smooth_1d(y, w=5):
    y = np.asarray(y, dtype=np.float32)
    if len(y) < 3:
        return y
    w = max(1, min(int(w), len(y)))
    if w <= 1:
        return y
    kernel = np.ones(w, dtype=np.float32) / w
    return np.convolve(y, kernel, mode="same")


def plot_global_action_lines(target, preds):
    fig, axes = plt.subplots(4, 1, figsize=(15, 12), sharex=True)
    fig.suptitle("UAV Action Sequence Trend (downsampled line view)", fontsize=16)

    target_b = bin_mean(target, bins=180)

    for i, dim in enumerate(DIMS):
        ax = axes[i]
        x = np.arange(len(target_b))
        ax.plot(x, smooth_1d(target_b[:, i]), color="black", linewidth=2.2, label="target")

        for name, pred in preds.items():
            pred_b = bin_mean(pred, bins=180)
            ax.plot(np.arange(len(pred_b)), smooth_1d(pred_b[:, i]), linewidth=1.8, label=name)

        ax.set_ylabel(dim)
        ax.grid(True, alpha=0.25)
        if i == 0:
            ax.legend(ncol=4, fontsize=9)

    axes[-1].set_xlabel("downsampled validation action step")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "global_action_trend_lines.png", dpi=220)
    plt.close(fig)


def plot_error_lines(target, preds):
    fig, axes = plt.subplots(4, 1, figsize=(15, 12), sharex=True)
    fig.suptitle("Absolute Error Trend by Action Dimension", fontsize=16)

    for i, dim in enumerate(DIMS):
        ax = axes[i]
        for name, pred in preds.items():
            err = np.abs(pred - target)[:, i]
            err_b = bin_mean(err.reshape(-1, 1), bins=180).reshape(-1)
            ax.plot(np.arange(len(err_b)), smooth_1d(err_b), linewidth=1.9, label=name)

        ax.set_ylabel(f"|{dim} error|")
        ax.grid(True, alpha=0.25)
        if i == 0:
            ax.legend(ncol=3, fontsize=9)

    axes[-1].set_xlabel("downsampled validation action step")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "per_dim_error_trend_lines.png", dpi=220)
    plt.close(fig)


def plot_overall_error_lines(target, preds):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_title("Overall Action-Chunk Absolute Error Trend")

    for name, pred in preds.items():
        err = np.mean(np.abs(pred - target), axis=1)
        err_b = bin_mean(err.reshape(-1, 1), bins=180).reshape(-1)
        ax.plot(np.arange(len(err_b)), smooth_1d(err_b), linewidth=2.0, label=name)

    ax.set_xlabel("downsampled validation action step")
    ax.set_ylabel("mean absolute error")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "overall_error_trend_lines.png", dpi=220)
    plt.close(fig)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    loaded = {}
    row_counts = {}

    for name, path in PRED_FILES.items():
        if not Path(path).exists():
            print(f"SKIP missing: {path}")
            continue
        target, pred = load_prediction_file(path)
        loaded[name] = (target, pred)
        row_counts[name] = int(len(target))

    if not loaded:
        raise RuntimeError("No prediction files found.")

    min_len = min(len(v[0]) for v in loaded.values())
    target = next(iter(loaded.values()))[0][:min_len]
    preds = {name: pred[:min_len] for name, (_, pred) in loaded.items()}

    plot_global_action_lines(target, preds)
    plot_error_lines(target, preds)
    plot_overall_error_lines(target, preds)

    REPORT.write_text(
        "# Clean Action Line Figures Report\n\n"
        "Generated cleaner line-based figures with downsampled validation action steps.\n\n"
        "## Files\n\n"
        "- `data/debug/plots/clean_action_lines/global_action_trend_lines.png`\n"
        "- `data/debug/plots/clean_action_lines/per_dim_error_trend_lines.png`\n"
        "- `data/debug/plots/clean_action_lines/overall_error_trend_lines.png`\n\n"
        "## Row Counts\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in row_counts.items())
        + f"\n\nAligned flattened action steps: `{min_len}`\n\n"
        "These figures are intended for paper-style qualitative visualization. "
        "They avoid dense scatter plots and use downsampled line trends instead.\n",
        encoding="utf-8",
    )

    print("CLEAN_ACTION_LINE_FIGURES_PASS")
    print("WROTE", OUT_DIR)
    print("WROTE", REPORT)


if __name__ == "__main__":
    main()
