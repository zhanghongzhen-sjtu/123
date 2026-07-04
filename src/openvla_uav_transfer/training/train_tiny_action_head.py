from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset


class PilotActionChunkDataset(Dataset):
    def __init__(self, jsonl: str | Path):
        self.rows = []
        with Path(jsonl).open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                state = row["state"]
                chunk = row["action_chunk"]
                if len(state) != 4:
                    raise ValueError("bad state dim")
                if not chunk or any(len(a) != 4 for a in chunk):
                    raise ValueError("bad action_chunk dim")
                self.rows.append((state, chunk))
        if not self.rows:
            raise ValueError("empty dataset")

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        state, chunk = self.rows[idx]
        x = torch.tensor(state, dtype=torch.float32)
        y = torch.tensor(chunk, dtype=torch.float32).reshape(-1)
        return x, y


class TinyActionHead(nn.Module):
    def __init__(self, hidden_dim: int = 128, out_dim: int = 32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(self, x):
        return self.net(x)


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    losses = []
    criterion = nn.MSELoss()
    for x, y in loader:
        x = x.to(device)
        y = y.to(device)
        pred = model(x)
        loss = criterion(pred, y)
        losses.append(float(loss.item()))
    return sum(losses) / max(1, len(losses))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-jsonl", default="data/processed/pilot_train_3maps.jsonl")
    parser.add_argument("--val-jsonl", default="data/processed/pilot_val_3maps.jsonl")
    parser.add_argument("--out", default="logs/pilot/tiny_action_head_smoke_report.json")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--hidden-dim", type=int, default=128)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("DEVICE", device)
    print("CUDA_AVAILABLE", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU", torch.cuda.get_device_name(0))

    train_ds = PilotActionChunkDataset(args.train_jsonl)
    val_ds = PilotActionChunkDataset(args.val_jsonl)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)

    model = TinyActionHead(hidden_dim=args.hidden_dim).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    criterion = nn.MSELoss()

    history = []
    initial_val = evaluate(model, val_loader, device)
    print(f"initial_val_loss={initial_val:.6f}")

    for epoch in range(1, args.epochs + 1):
        model.train()
        train_losses = []
        for x, y in train_loader:
            x = x.to(device)
            y = y.to(device)
            pred = model(x)
            loss = criterion(pred, y)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            train_losses.append(float(loss.item()))

        train_loss = sum(train_losses) / max(1, len(train_losses))
        val_loss = evaluate(model, val_loader, device)
        history.append({"epoch": epoch, "train_loss": train_loss, "val_loss": val_loss})
        print(f"epoch={epoch:03d} train_loss={train_loss:.6f} val_loss={val_loss:.6f}")

    final_train = history[-1]["train_loss"]
    final_val = history[-1]["val_loss"]
    train_decreased = final_train < history[0]["train_loss"]
    val_finite = math.isfinite(final_val)

    report = {
        "task": "tiny_action_head_smoke_training",
        "not_openvla_training": True,
        "not_lora_oft": True,
        "not_closed_loop_eval": True,
        "train_jsonl": args.train_jsonl,
        "val_jsonl": args.val_jsonl,
        "train_rows": len(train_ds),
        "val_rows": len(val_ds),
        "device": str(device),
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "hidden_dim": args.hidden_dim,
        "lr": args.lr,
        "initial_val_loss": initial_val,
        "final_train_loss": final_train,
        "final_val_loss": final_val,
        "train_loss_decreased": train_decreased,
        "val_loss_finite": val_finite,
        "history": history,
        "status": "PILOT_ACTION_HEAD_SMOKE_PASS" if train_decreased and val_finite else "PILOT_ACTION_HEAD_SMOKE_WARN",
    }

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("WROTE", args.out)
    print(report["status"])


if __name__ == "__main__":
    main()
