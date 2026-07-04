import argparse, json, math
from pathlib import Path
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))

def vec(x, n, name):
    if not isinstance(x, list) or len(x) != n:
        raise ValueError(f"{name} must be length {n}")
    if not all(is_num(v) for v in x):
        raise ValueError(f"{name} invalid numeric values")
    return torch.tensor(x, dtype=torch.float32)

class StateActionChunkDataset(Dataset):
    def __init__(self, jsonl, max_rows=None):
        self.rows = []
        with Path(jsonl).open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if not line.strip():
                    continue
                r = json.loads(line)
                state = vec(r["state"], 4, "state")
                actions = torch.stack([vec(a, 4, "action_chunk step") for a in r["action_chunk"]])
                self.rows.append((state, actions))
                if max_rows is not None and len(self.rows) >= max_rows:
                    break
        if not self.rows:
            raise ValueError(f"empty dataset: {jsonl}")

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        state, actions = self.rows[idx]
        return {"state": state, "actions": actions}

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

def eval_loop(model, loader, device):
    model.eval()
    losses = []
    with torch.no_grad():
        for batch in loader:
            state = batch["state"].to(device)
            target = batch["actions"].to(device)
            pred = model(state)
            losses.append(float(F.smooth_l1_loss(pred, target).cpu()))
    model.train()
    return sum(losses) / max(1, len(losses))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-jsonl", default="data/processed/clean_train_timestamp_maps.jsonl")
    ap.add_argument("--val-jsonl", default="data/processed/clean_val_timestamp_maps.jsonl")
    ap.add_argument("--max-train-rows", type=int, default=120)
    ap.add_argument("--max-val-rows", type=int, default=64)
    ap.add_argument("--batch-size", type=int, default=1)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--hidden-dim", type=int, default=256)
    ap.add_argument("--out-json", default="logs/pilot/state_only_action_head_baseline_report.json")
    ap.add_argument("--out-md", default="docs/state_only_action_head_baseline_report.md")
    ap.add_argument("--ckpt", default="checkpoints/uav_action_head/state_only_action_head_baseline.pt")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"

    train_ds = StateActionChunkDataset(args.train_jsonl, args.max_train_rows)
    val_ds = StateActionChunkDataset(args.val_jsonl, args.max_val_rows)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)

    model = StateOnlyActionHead(args.hidden_dim).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)

    initial_val = eval_loop(model, val_loader, device)
    history = []

    for epoch in range(1, args.epochs + 1):
        losses = []
        for batch in train_loader:
            state = batch["state"].to(device)
            target = batch["actions"].to(device)
            pred = model(state)
            loss = F.smooth_l1_loss(pred, target)
            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(float(loss.detach().cpu()))

        train_loss = sum(losses) / max(1, len(losses))
        val_loss = eval_loop(model, val_loader, device)
        history.append({"epoch": epoch, "train_loss": train_loss, "val_loss": val_loss, "train_steps": len(losses), "val_batches": len(val_loader)})
        print(f"epoch={epoch} train_loss={train_loss:.6f} val_loss={val_loss:.6f}")

    Path(args.ckpt).parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state_dict": model.state_dict(), "hidden_dim": args.hidden_dim}, args.ckpt)

    report = {
        "status": "STATE_ONLY_ACTION_HEAD_BASELINE_PASS",
        "model": "state_only_mlp",
        "train_rows": len(train_ds),
        "val_rows": len(val_ds),
        "batch_size": args.batch_size,
        "epochs": args.epochs,
        "lr": args.lr,
        "initial_val_loss": initial_val,
        "history": history,
        "checkpoint": args.ckpt,
        "cuda_max_memory_gb": round(torch.cuda.max_memory_allocated() / 1024**3, 3) if torch.cuda.is_available() else 0,
    }

    Path(args.out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.out_md).write_text("# State-Only Action Head Baseline Report\n\n```json\n" + json.dumps(report, ensure_ascii=False, indent=2) + "\n```\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"WROTE {args.out_json}")
    print(f"WROTE {args.out_md}")
    print(f"WROTE {args.ckpt}")
    print("STATE_ONLY_ACTION_HEAD_BASELINE_PASS")

if __name__ == "__main__":
    main()
