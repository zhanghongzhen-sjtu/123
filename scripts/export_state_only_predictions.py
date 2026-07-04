import argparse
import json
import math
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

ACTION_NAMES = ["vx", "vy", "vz", "yaw_rate"]


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def vec(x, n, name):
    if not isinstance(x, list) or len(x) != n:
        raise ValueError(f"{name} must be length {n}")
    if not all(is_num(v) for v in x):
        raise ValueError(f"{name} invalid")
    return np.asarray(x, dtype=np.float32)


class StateOnlyActionHead(nn.Module):
    def __init__(self, hidden_dim=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.LayerNorm(4),
            nn.Linear(4, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 32),
        )

    def forward(self, state):
        return self.net(state).reshape(state.shape[0], 8, 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", default="data/processed/clean_val_timestamp_maps.jsonl")
    ap.add_argument("--ckpt", default="checkpoints/uav_action_head/state_only_action_head_baseline.pt")
    ap.add_argument("--max-rows", type=int, default=64)
    ap.add_argument("--out", default="data/debug/predictions/state_only_val_predictions.jsonl")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"

    ck = torch.load(args.ckpt, map_location=device)
    hidden_dim = ck.get("hidden_dim", 256)

    model = StateOnlyActionHead(hidden_dim).to(device)
    model.load_state_dict(ck["model_state_dict"])
    model.eval()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with Path(args.jsonl).open("r", encoding="utf-8") as f, out.open("w", encoding="utf-8") as w:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            state = vec(row["state"], 4, "state")
            target = np.stack([vec(a, 4, "action") for a in row["action_chunk"]], axis=0)

            with torch.no_grad():
                pred = model(torch.tensor(state, dtype=torch.float32, device=device).reshape(1, 4))[0].cpu().numpy()

            rec = {
                "dataset": row.get("dataset"),
                "episode_id": row.get("episode_id"),
                "step_id": row.get("step_id"),
                "source": row.get("source", {}),
                "state": state.tolist(),
                "target_action_chunk": target.tolist(),
                "pred_action_chunk": pred.tolist(),
                "abs_error": np.abs(pred - target).tolist(),
            }
            w.write(json.dumps(rec, ensure_ascii=False) + "\n")

            count += 1
            if count >= args.max_rows:
                break

    print(f"WROTE {out}")
    print(f"ROWS {count}")
    print("STATE_ONLY_PREDICTION_EXPORT_PASS")


if __name__ == "__main__":
    main()
