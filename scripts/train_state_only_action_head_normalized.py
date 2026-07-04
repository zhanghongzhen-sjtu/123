import argparse, json, math
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

ACTION_NAMES = ["vx", "vy", "vz", "yaw_rate"]

def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))

def vec(x, n, name):
    if not isinstance(x, list) or len(x) != n:
        raise ValueError(f"{name} must be length {n}")
    if not all(is_num(v) for v in x):
        raise ValueError(f"{name} invalid")
    return np.asarray(x, dtype=np.float32)

def load_stats(path):
    s = json.loads(Path(path).read_text(encoding="utf-8"))
    mean = np.asarray(s["mean"], dtype=np.float32)
    std = np.asarray(s["std"], dtype=np.float32)
    return mean, std, s

class DatasetNorm(Dataset):
    def __init__(self, jsonl, mean, std, max_rows=None):
        self.rows = []
        with Path(jsonl).open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                state = vec(r["state"], 4, "state")
                actions = np.stack([vec(a, 4, "action") for a in r["action_chunk"]], axis=0)
                actions_norm = (actions - mean) / std
                self.rows.append((torch.tensor(state), torch.tensor(actions), torch.tensor(actions_norm)))
                if max_rows is not None and len(self.rows) >= max_rows:
                    break

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, i):
        s, a, an = self.rows[i]
        return {"state": s.float(), "actions": a.float(), "actions_norm": an.float()}

class Head(nn.Module):
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

def collect_metrics(pred, target):
    err = pred - target
    mae = err.abs().mean(dim=(0,1)).cpu().numpy()
    rmse = err.pow(2).mean(dim=(0,1)).sqrt().cpu().numpy()
    return {
        "overall_mae": float(err.abs().mean().cpu()),
        "overall_rmse": float(err.pow(2).mean().sqrt().cpu()),
        "per_dim_mae": {n: float(mae[i]) for i, n in enumerate(ACTION_NAMES)},
        "per_dim_rmse": {n: float(rmse[i]) for i, n in enumerate(ACTION_NAMES)},
    }

def eval_loop(model, loader, device, mean_t, std_t):
    model.eval()
    norm_losses, preds, targets = [], [], []
    with torch.no_grad():
        for b in loader:
            s = b["state"].to(device)
            target = b["actions"].to(device)
            target_norm = b["actions_norm"].to(device)
            pred_norm = model(s)
            norm_losses.append(float(F.smooth_l1_loss(pred_norm, target_norm).cpu()))
            pred = pred_norm * std_t + mean_t
            preds.append(pred.cpu())
            targets.append(target.cpu())
    model.train()
    metric = collect_metrics(torch.cat(preds), torch.cat(targets))
    metric["normalized_loss"] = sum(norm_losses) / max(1, len(norm_losses))
    return metric

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-jsonl", default="data/processed/clean_train_timestamp_maps.jsonl")
    ap.add_argument("--val-jsonl", default="data/processed/clean_val_timestamp_maps.jsonl")
    ap.add_argument("--stats", default="data/processed/clean_train_action_stats.json")
    ap.add_argument("--max-train-rows", type=int, default=120)
    ap.add_argument("--max-val-rows", type=int, default=64)
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--hidden-dim", type=int, default=256)
    ap.add_argument("--out-json", default="logs/pilot/state_only_action_head_normalized_report.json")
    ap.add_argument("--out-md", default="docs/state_only_action_head_normalized_report.md")
    ap.add_argument("--ckpt", default="checkpoints/uav_action_head/state_only_action_head_normalized.pt")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    mean, std, stats = load_stats(args.stats)
    mean_t = torch.tensor(mean, device=device).reshape(1,1,4)
    std_t = torch.tensor(std, device=device).reshape(1,1,4)

    train_ds = DatasetNorm(args.train_jsonl, mean, std, args.max_train_rows)
    val_ds = DatasetNorm(args.val_jsonl, mean, std, args.max_val_rows)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)

    model = Head(args.hidden_dim).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)

    initial_val = eval_loop(model, val_loader, device, mean_t, std_t)
    history = []

    for epoch in range(1, args.epochs + 1):
        losses = []
        for b in train_loader:
            s = b["state"].to(device)
            target_norm = b["actions_norm"].to(device)
            pred_norm = model(s)
            loss = F.smooth_l1_loss(pred_norm, target_norm)
            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(float(loss.detach().cpu()))

        val = eval_loop(model, val_loader, device, mean_t, std_t)
        item = {
            "epoch": epoch,
            "train_normalized_loss": sum(losses) / max(1, len(losses)),
            "val_normalized_loss": val["normalized_loss"],
            "val_overall_mae": val["overall_mae"],
            "val_overall_rmse": val["overall_rmse"],
            "val_per_dim_mae": val["per_dim_mae"],
            "val_per_dim_rmse": val["per_dim_rmse"],
        }
        history.append(item)
        print(json.dumps(item, ensure_ascii=False))

    Path(args.ckpt).parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state_dict": model.state_dict(), "hidden_dim": args.hidden_dim, "stats": stats}, args.ckpt)

    report = {
        "status": "STATE_ONLY_NORMALIZED_ACTION_HEAD_PASS",
        "train_rows": len(train_ds),
        "val_rows": len(val_ds),
        "stats": args.stats,
        "initial_val": initial_val,
        "history": history,
        "checkpoint": args.ckpt,
        "cuda_max_memory_gb": round(torch.cuda.max_memory_allocated() / 1024**3, 3) if torch.cuda.is_available() else 0,
    }

    Path(args.out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_md).write_text("# State-Only Normalized Action Head Report\n\n```json\n" + json.dumps(report, ensure_ascii=False, indent=2) + "\n```\n", encoding="utf-8")
    print(f"WROTE {args.out_json}")
    print(f"WROTE {args.out_md}")
    print("STATE_ONLY_NORMALIZED_ACTION_HEAD_PASS")

if __name__ == "__main__":
    main()
