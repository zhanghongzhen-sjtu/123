import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ACTION_NAMES = ["vx", "vy", "vz", "yaw_rate"]


def load_predictions(path):
    targets, preds = [], []
    meta = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            targets.append(np.asarray(r["target_action_chunk"], dtype=np.float32))
            preds.append(np.asarray(r["pred_action_chunk"], dtype=np.float32))
            meta.append({"episode_id": r.get("episode_id"), "step_id": r.get("step_id"), "source": r.get("source", {})})
    return np.asarray(targets), np.asarray(preds), meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred-jsonl", default="data/debug/predictions/state_only_val_predictions.jsonl")
    ap.add_argument("--out-dir", default="data/debug/plots/state_only")
    ap.add_argument("--prefix", default="state_only")
    ap.add_argument("--max-samples-line", type=int, default=64)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    target, pred, meta = load_predictions(args.pred_jsonl)
    err = pred - target
    abs_err = np.abs(err)

    # Flatten sample and chunk dimensions for curve plots.
    n, chunk, dim = target.shape
    x = np.arange(n * chunk)
    target_f = target.reshape(n * chunk, dim)
    pred_f = pred.reshape(n * chunk, dim)
    abs_f = abs_err.reshape(n * chunk, dim)

    limit = min(args.max_samples_line * chunk, len(x))

    for d, name in enumerate(ACTION_NAMES):
        plt.figure(figsize=(12, 4))
        plt.plot(x[:limit], target_f[:limit, d], label="target", linewidth=1)
        plt.plot(x[:limit], pred_f[:limit, d], label="pred", linewidth=1)
        plt.title(f"{args.prefix} {name}: target vs prediction")
        plt.xlabel("flattened validation action step")
        plt.ylabel(name)
        plt.legend()
        plt.tight_layout()
        p = out_dir / f"{args.prefix}_{name}_target_vs_pred.png"
        plt.savefig(p, dpi=160)
        plt.close()

        plt.figure(figsize=(12, 4))
        plt.plot(x[:limit], abs_f[:limit, d], label="abs error", linewidth=1)
        plt.title(f"{args.prefix} {name}: absolute error")
        plt.xlabel("flattened validation action step")
        plt.ylabel(f"|error {name}|")
        plt.legend()
        plt.tight_layout()
        p = out_dir / f"{args.prefix}_{name}_abs_error.png"
        plt.savefig(p, dpi=160)
        plt.close()

    mae = abs_err.mean(axis=(0, 1))
    rmse = np.sqrt((err ** 2).mean(axis=(0, 1)))

    plt.figure(figsize=(7, 4))
    xs = np.arange(len(ACTION_NAMES))
    plt.bar(xs - 0.18, mae, width=0.36, label="MAE")
    plt.bar(xs + 0.18, rmse, width=0.36, label="RMSE")
    plt.xticks(xs, ACTION_NAMES)
    plt.title(f"{args.prefix}: per-dimension error")
    plt.ylabel("error")
    plt.legend()
    plt.tight_layout()
    p = out_dir / f"{args.prefix}_per_dim_error_bar.png"
    plt.savefig(p, dpi=180)
    plt.close()

    report = {
        "status": "ACTION_PREDICTION_PLOT_PASS",
        "pred_jsonl": args.pred_jsonl,
        "rows": int(n),
        "action_chunk": int(chunk),
        "per_dim_mae": {ACTION_NAMES[i]: float(mae[i]) for i in range(dim)},
        "per_dim_rmse": {ACTION_NAMES[i]: float(rmse[i]) for i in range(dim)},
        "out_dir": str(out_dir),
    }

    (out_dir / f"{args.prefix}_plot_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("ACTION_PREDICTION_PLOT_PASS")


if __name__ == "__main__":
    main()
