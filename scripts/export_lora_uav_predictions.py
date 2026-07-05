#!/usr/bin/env python3
import argparse
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from transformers import AutoModelForVision2Seq, AutoProcessor
from peft import PeftModel


DIM_NAMES = ["vx", "vy", "vz", "yaw_rate"]


def load_jsonl(path, max_rows=None):
    rows = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
                if max_rows is not None and len(rows) >= max_rows:
                    break
    return rows


def resolve_image_path(image, image_root):
    p = Path(image)
    if p.is_absolute():
        return p
    return Path(image_root) / p


def build_prompt(instruction):
    return f"In: What action should the UAV take to {instruction}?\nOut:"


class FlexibleActionHead(nn.Module):
    def __init__(self, checkpoint_obj):
        super().__init__()

        if isinstance(checkpoint_obj, dict) and "head_state_dict" in checkpoint_obj:
            raw_sd = checkpoint_obj["head_state_dict"]
            sd = {
                (k[len("net."):] if str(k).startswith("net.") else k): v
                for k, v in raw_sd.items()
            }

            # Infer dimensions from saved weights. In this checkpoint, input_dim already
            # includes OpenVLA hidden features plus UAV state, e.g. 4096 + 4 = 4100.
            self.input_dim = int(sd["1.weight"].shape[1])
            hidden_dim = int(sd["1.weight"].shape[0])
            self.output_dim = int(sd["6.weight"].shape[0])

            self.net = nn.Sequential(
                nn.LayerNorm(self.input_dim),
                nn.Linear(self.input_dim, hidden_dim),
                nn.GELU(),
                nn.Dropout(0.0),
                nn.Linear(hidden_dim, hidden_dim),
                nn.GELU(),
                nn.Linear(hidden_dim, self.output_dim),
            )
            self.net.load_state_dict(sd, strict=True)
            self.feature_source = checkpoint_obj.get("feature_source", "unknown")
            return

        if hasattr(checkpoint_obj, "state_dict"):
            sd = checkpoint_obj.state_dict()
        elif isinstance(checkpoint_obj, dict):
            sd = checkpoint_obj
        else:
            raise ValueError(f"Unsupported action head checkpoint type: {type(checkpoint_obj)}")

        linear_keys = [
            k for k, v in sd.items()
            if str(k).endswith(".weight") and hasattr(v, "ndim") and v.ndim == 2
        ]
        if not linear_keys:
            raise ValueError("No Linear weights found in action head checkpoint.")

        linear_keys = sorted(linear_keys, key=lambda k: [int(x) for x in re.findall(r"\d+", k)] or [999999])
        layers = []
        for i, wk in enumerate(linear_keys):
            w = sd[wk]
            in_dim = int(w.shape[1])
            out_dim = int(w.shape[0])
            layers.append(nn.Linear(in_dim, out_dim))
            if i != len(linear_keys) - 1:
                layers.append(nn.ReLU())

        self.net = nn.Sequential(*layers)
        own_sd = self.net.state_dict()
        mapped = {}
        for i, wk in enumerate(linear_keys):
            layer_idx = i * 2
            prefix = wk[:-len(".weight")]
            mapped[f"{layer_idx}.weight"] = sd[wk]
            bk = prefix + ".bias"
            mapped[f"{layer_idx}.bias"] = sd.get(bk, torch.zeros(sd[wk].shape[0]))
        self.net.load_state_dict(mapped, strict=False)
        self.input_dim = int(self.net[0].in_features)
        self.output_dim = int(self.net[-1].out_features)
        self.feature_source = "generic_state_dict"

    def forward(self, x):
        return self.net(x)


def load_action_head(path, device):
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    head = FlexibleActionHead(ckpt).to(device)
    head.eval()
    print(
        f"[action_head] input_dim={head.input_dim} output_dim={head.output_dim} "
        f"feature_source={getattr(head, 'feature_source', 'unknown')}",
        flush=True,
    )
    return head

def compute_metrics(targets, preds):
    t = np.asarray(targets, dtype=np.float32)
    p = np.asarray(preds, dtype=np.float32)
    err = p - t
    mae = np.abs(err).mean(axis=(0, 1))
    rmse = np.sqrt((err ** 2).mean(axis=(0, 1)))
    return {
        "overall_mae": float(np.abs(err).mean()),
        "overall_rmse": float(np.sqrt((err ** 2).mean())),
        "per_dim_mae": {DIM_NAMES[i]: float(mae[i]) for i in range(4)},
        "per_dim_rmse": {DIM_NAMES[i]: float(rmse[i]) for i in range(4)},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", required=True)
    ap.add_argument("--image-root", default=".")
    ap.add_argument("--model-id", default="openvla/openvla-7b")
    ap.add_argument("--cache-dir", default=None)
    ap.add_argument("--lora-adapter", required=True)
    ap.add_argument("--action-head", required=True)
    ap.add_argument("--max-rows", type=int, default=64)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "cuda" else torch.float32

    rows = load_jsonl(args.jsonl, args.max_rows)
    if not rows:
        raise RuntimeError(f"No rows loaded from {args.jsonl}")

    processor = AutoProcessor.from_pretrained(
        args.model_id,
        trust_remote_code=True,
        cache_dir=args.cache_dir,
    )

    base_model = AutoModelForVision2Seq.from_pretrained(
        args.model_id,
        trust_remote_code=True,
        cache_dir=args.cache_dir,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
    ).to(device)

    model = PeftModel.from_pretrained(base_model, args.lora_adapter).to(device)
    model.eval()

    action_head = load_action_head(args.action_head, device)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    all_targets = []
    all_preds = []

    with out_path.open("w", encoding="utf-8") as w, torch.no_grad():
        for idx, row in enumerate(rows):
            print(f"[export] {idx + 1}/{len(rows)}", flush=True)
            image_path = resolve_image_path(row["image"], args.image_root)
            if not image_path.exists():
                raise FileNotFoundError(f"image not found: {image_path}")

            image = Image.open(image_path).convert("RGB")
            instruction = str(row.get("instruction", ""))
            prompt = build_prompt(instruction)

            inputs = processor(prompt, image, return_tensors="pt")
            proc_inputs = {}
            for k, v in inputs.items():
                if torch.is_tensor(v):
                    if k == "pixel_values":
                        proc_inputs[k] = v.to(device=device, dtype=dtype)
                    else:
                        proc_inputs[k] = v.to(device=device)
                else:
                    proc_inputs[k] = v

            outputs = model(
                **proc_inputs,
                output_hidden_states=True,
                return_dict=True,
                use_cache=False,
            )
            hidden = outputs.hidden_states[-1][:, -1, :].float()

            state = torch.tensor(row["state"], dtype=torch.float32, device=device).view(1, 4)

            if action_head.input_dim == hidden.shape[-1] + 4:
                head_in = torch.cat([hidden, state], dim=-1)
            elif action_head.input_dim == hidden.shape[-1]:
                head_in = hidden
            elif action_head.input_dim == 4:
                head_in = state
            else:
                raise ValueError(
                    f"Unsupported action head input_dim={action_head.input_dim}, "
                    f"hidden_dim={hidden.shape[-1]}, state_dim=4"
                )

            pred_flat = action_head(head_in)
            if pred_flat.shape[-1] != 32:
                raise ValueError(f"Expected action head output dim 32, got {pred_flat.shape}")
            pred = pred_flat.view(8, 4).detach().cpu().numpy().astype(float).tolist()

            target = row["action_chunk"]
            if len(target) != 8 or any(len(x) != 4 for x in target):
                raise ValueError(f"bad action_chunk at row {idx}")

            all_targets.append(target)
            all_preds.append(pred)

            item = {
                "dataset": row.get("dataset", "TravelUAV"),
                "episode_id": row.get("episode_id"),
                "step_id": row.get("step_id"),
                "image": row.get("image"),
                "instruction": instruction,
                "state": row.get("state"),
                "target": target,
                "pred": pred,
                "target_action_chunk": target,
                "pred_action_chunk": pred,
                "source": row.get("source", {}),
                "model": "lora_100step",
                "feature_source": "openvla_lora_last_hidden_state",
            }
            w.write(json.dumps(item, ensure_ascii=False) + "\n")

    metrics = compute_metrics(all_targets, all_preds)
    cuda_mem = None
    if torch.cuda.is_available():
        cuda_mem = round(torch.cuda.max_memory_allocated() / (1024 ** 3), 3)

    report = {
        "status": "LORA_UAV_PREDICTION_EXPORT_PASS",
        "jsonl": args.jsonl,
        "rows": len(rows),
        "out": str(out_path),
        "lora_adapter": args.lora_adapter,
        "action_head": args.action_head,
        "metrics": metrics,
        "cuda_max_memory_gb": cuda_mem,
        "full_training_started": False,
        "closed_loop_eval_started": False,
    }

    report_path.write_text(
        "# LoRA 100-Step UAV Prediction Export Report\n\n"
        "```json\n"
        + json.dumps(report, ensure_ascii=False, indent=2)
        + "\n```\n",
        encoding="utf-8",
    )

    print("WROTE", out_path)
    print("WROTE", report_path)
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    print("LORA_UAV_PREDICTION_EXPORT_PASS")


if __name__ == "__main__":
    main()
