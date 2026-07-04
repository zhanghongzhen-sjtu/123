import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ACTION_NAMES = ["vx", "vy", "vz", "yaw_rate"]


def load_pred(path):
    targets, preds = [], []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            targets.append(np.asarray(r["target_action_chunk"], dtype=np.float32))
            preds.append(np.asarray(r["pred_action_chunk"], dtype=np.float32))

    target = np.asarray(targets)
    pred = np.asarray(preds)
    err = pred - target
    abs_err = np.abs(err)
    mae = abs_err.mean(axis=(0, 1))
    rmse = np.sqrt((err ** 2).mean(axis=(0, 1)))

    return {
        "rows": int(target.shape[0]),
        "chunk": int(target.shape[1]),
        "dim": int(target.shape[2]),
        "mae": mae,
        "rmse": rmse,
        "overall_mae": float(abs_err.mean()),
        "overall_rmse": float(np.sqrt((err ** 2).mean())),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state-jsonl", default="data/debug/predictions/state_only_val_predictions.jsonl")
    ap.add_argument("--openvla-jsonl", default="data/debug/predictions/frozen_openvla_val_predictions.jsonl")
    ap.add_argument("--out-dir", default="data/debug/plots/combined")
    ap.add_argument("--out-md", default="docs/action_head_combined_comparison_report.md")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    state = load_pred(args.state_jsonl)
    openvla = load_pred(args.openvla_jsonl)

    x = np.arange(len(ACTION_NAMES))
    width = 0.2

    plt.figure(figsize=(10, 5))
    plt.bar(x - 1.5 * width, state["mae"], width, label="state MAE")
    plt.bar(x - 0.5 * width, state["rmse"], width, label="state RMSE")
    plt.bar(x + 0.5 * width, openvla["mae"], width, label="frozen OpenVLA MAE")
    plt.bar(x + 1.5 * width, openvla["rmse"], width, label="frozen OpenVLA RMSE")
    plt.xticks(x, ACTION_NAMES)
    plt.ylabel("error")
    plt.title("Action head per-dimension error comparison")
    plt.legend()
    plt.tight_layout()
    per_dim_path = out_dir / "combined_per_dim_error_bar.png"
    plt.savefig(per_dim_path, dpi=180)
    plt.close()

    labels = ["MAE", "RMSE"]
    state_vals = [state["overall_mae"], state["overall_rmse"]]
    openvla_vals = [openvla["overall_mae"], openvla["overall_rmse"]]

    xx = np.arange(len(labels))
    plt.figure(figsize=(6, 5))
    plt.bar(xx - 0.18, state_vals, 0.36, label="state-only")
    plt.bar(xx + 0.18, openvla_vals, 0.36, label="frozen OpenVLA + state")
    plt.xticks(xx, labels)
    plt.ylabel("error")
    plt.title("Overall action prediction error")
    plt.legend()
    plt.tight_layout()
    overall_path = out_dir / "combined_overall_error_bar.png"
    plt.savefig(overall_path, dpi=180)
    plt.close()

    diff_mae = openvla["mae"] - state["mae"]
    diff_rmse = openvla["rmse"] - state["rmse"]

    plt.figure(figsize=(8, 4))
    plt.axhline(0, color="black", linewidth=1)
    plt.bar(x - 0.18, diff_mae, 0.36, label="MAE diff")
    plt.bar(x + 0.18, diff_rmse, 0.36, label="RMSE diff")
    plt.xticks(x, ACTION_NAMES)
    plt.ylabel("frozen OpenVLA error - state-only error")
    plt.title("Error difference by action dimension")
    plt.legend()
    plt.tight_layout()
    diff_path = out_dir / "combined_error_difference_bar.png"
    plt.savefig(diff_path, dpi=180)
    plt.close()

    report = {
        "status": "ACTION_HEAD_COMBINED_COMPARISON_PASS",
        "state_only": {
            "rows": state["rows"],
            "overall_mae": state["overall_mae"],
            "overall_rmse": state["overall_rmse"],
            "per_dim_mae": {ACTION_NAMES[i]: float(state["mae"][i]) for i in range(4)},
            "per_dim_rmse": {ACTION_NAMES[i]: float(state["rmse"][i]) for i in range(4)},
        },
        "frozen_openvla_plus_state": {
            "rows": openvla["rows"],
            "overall_mae": openvla["overall_mae"],
            "overall_rmse": openvla["overall_rmse"],
            "per_dim_mae": {ACTION_NAMES[i]: float(openvla["mae"][i]) for i in range(4)},
            "per_dim_rmse": {ACTION_NAMES[i]: float(openvla["rmse"][i]) for i in range(4)},
        },
        "plots": {
            "per_dim": str(per_dim_path),
            "overall": str(overall_path),
            "difference": str(diff_path),
        },
    }

    report_json = out_dir / "combined_comparison_report.json"
    report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Action Head Combined Comparison Report",
        "",
        "## Status",
        "",
        "- ACTION_HEAD_COMBINED_COMPARISON_PASS",
        "- LORA_OFT_NOT_STARTED",
        "- FULL_TRAINING_NOT_STARTED",
        "",
        "## Plots",
        "",
        f"- `{per_dim_path}`",
        f"- `{overall_path}`",
        f"- `{diff_path}`",
        "",
        "## Result",
        "",
        "```json",
        json.dumps(report, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Interpretation",
        "",
        "Positive values in the error-difference plot mean the frozen OpenVLA + state model has higher error than the state-only baseline.",
        "",
        "This pilot comparison should be interpreted as an engineering-stage result, not final thesis performance.",
    ]
    Path(args.out_md).write_text("\n".join(md), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {report_json}")
    print(f"WROTE {args.out_md}")
    print("ACTION_HEAD_COMBINED_COMPARISON_PASS")


if __name__ == "__main__":
    main()
