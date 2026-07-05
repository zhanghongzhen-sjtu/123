#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path
from collections import defaultdict

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


WORLD_DIMS = ["vx", "vy", "vz", "yaw_rate"]
BODY_DIMS = ["v_forward", "v_right", "vz", "yaw_rate"]


def world_to_body(action, yaw):
    vx, vy, vz, yaw_rate = action
    c = math.cos(yaw)
    s = math.sin(yaw)
    v_forward = c * vx + s * vy
    v_right = -s * vx + c * vy
    return [v_forward, v_right, vz, yaw_rate]


def convert_chunk(chunk, state):
    yaw = float(state[3])
    return [world_to_body(a, yaw) for a in chunk]


def read_rows(path):
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def write_body_jsonl(src_path, out_path):
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    n = 0
    with out.open("w", encoding="utf-8") as w:
        for r in read_rows(src_path):
            rr = dict(r)
            rr["action_world"] = r["action"]
            rr["action_chunk_world"] = r["action_chunk"]
            rr["action"] = world_to_body(r["action"], r["state"][3])
            rr["action_chunk"] = convert_chunk(r["action_chunk"], r["state"])
            src = dict(rr.get("source", {}))
            src["action_frame"] = "body"
            src["original_action_frame"] = "world"
            rr["source"] = src
            w.write(json.dumps(rr, ensure_ascii=False) + "\n")
            n += 1
    return n


def collect_by_map(path, body=False):
    data = defaultdict(list)
    for r in read_rows(path):
        m = r.get("source", {}).get("map", "unknown")
        chunk = np.asarray(r["action_chunk"], dtype=np.float32)
        data[m].append(chunk.reshape(-1, 4))
    return {k: np.concatenate(v, axis=0) for k, v in data.items() if v}


def stats_table(data, dims):
    rows = []
    for m, arr in data.items():
        mean = arr.mean(axis=0)
        std = arr.std(axis=0)
        mn = arr.min(axis=0)
        mx = arr.max(axis=0)
        rows.append((m, mean, std, mn, mx))
    return rows


def plot_std(data, dims, out_path, title):
    maps = list(data.keys())
    x = np.arange(len(dims))
    width = 0.8 / max(1, len(maps))

    plt.figure(figsize=(14, 6))
    for i, m in enumerate(maps):
        std = data[m].std(axis=0)
        plt.bar(x - 0.4 + width / 2 + i * width, std, width, label=m)

    plt.xticks(x, dims)
    plt.ylabel("std")
    plt.title(title)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180)
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-jsonl", required=True)
    ap.add_argument("--val-jsonl", required=True)
    ap.add_argument("--out-train-body", required=True)
    ap.add_argument("--out-val-body", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    train_n = write_body_jsonl(args.train_jsonl, args.out_train_body)
    val_n = write_body_jsonl(args.val_jsonl, args.out_val_body)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    world_train = collect_by_map(args.train_jsonl)
    body_train = collect_by_map(args.out_train_body)
    world_val = collect_by_map(args.val_jsonl)
    body_val = collect_by_map(args.out_val_body)

    plot_std(world_train, WORLD_DIMS, out_dir / "train_world_action_std_by_map.png", "Train world-frame action std by map")
    plot_std(body_train, BODY_DIMS, out_dir / "train_body_action_std_by_map.png", "Train body-frame action std by map")
    plot_std(world_val, WORLD_DIMS, out_dir / "val_world_action_std_by_map.png", "Val world-frame action std by map")
    plot_std(body_val, BODY_DIMS, out_dir / "val_body_action_std_by_map.png", "Val body-frame action std by map")

    md = []
    md.append("# Body-Frame UAV Action Analysis")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- `BODY_FRAME_ACTION_ANALYSIS_PASS`")
    md.append("- training started: `false`")
    md.append("- model loaded: `false`")
    md.append("")
    md.append("## Converted Files")
    md.append("")
    md.append(f"- train body JSONL: `{args.out_train_body}` rows={train_n}")
    md.append(f"- val body JSONL: `{args.out_val_body}` rows={val_n}")
    md.append("")
    md.append("## Action Definitions")
    md.append("")
    md.append("World-frame action:")
    md.append("")
    md.append("```text")
    md.append("action_world = [vx, vy, vz, yaw_rate]")
    md.append("```")
    md.append("")
    md.append("Body-frame action:")
    md.append("")
    md.append("```text")
    md.append("v_forward = cos(yaw) * vx + sin(yaw) * vy")
    md.append("v_right   = -sin(yaw) * vx + cos(yaw) * vy")
    md.append("action_body = [v_forward, v_right, vz, yaw_rate]")
    md.append("```")
    md.append("")
    md.append("## Motivation")
    md.append("")
    md.append("World-frame vx/vy depend on global map axes. For UAV navigation, the same forward motion may appear as different world-frame vx/vy values depending on yaw and map orientation.")
    md.append("")
    md.append("Body-frame actions are ego-centric and therefore better aligned with cross-map and cross-heading transfer.")
    md.append("")
    md.append("## Plots")
    md.append("")
    for name in [
        "train_world_action_std_by_map.png",
        "train_body_action_std_by_map.png",
        "val_world_action_std_by_map.png",
        "val_body_action_std_by_map.png",
    ]:
        md.append(f"- `{out_dir / name}`")
    md.append("")
    md.append("## Train World-Frame Stats")
    md.append("")
    md.append("| map | dim | mean | std | min | max |")
    md.append("|---|---|---:|---:|---:|---:|")
    for m, mean, std, mn, mx in stats_table(world_train, WORLD_DIMS):
        for i, d in enumerate(WORLD_DIMS):
            md.append(f"| {m} | {d} | {mean[i]:.6f} | {std[i]:.6f} | {mn[i]:.6f} | {mx[i]:.6f} |")
    md.append("")
    md.append("## Train Body-Frame Stats")
    md.append("")
    md.append("| map | dim | mean | std | min | max |")
    md.append("|---|---|---:|---:|---:|---:|")
    for m, mean, std, mn, mx in stats_table(body_train, BODY_DIMS):
        for i, d in enumerate(BODY_DIMS):
            md.append(f"| {m} | {d} | {mean[i]:.6f} | {std[i]:.6f} | {mn[i]:.6f} | {mx[i]:.6f} |")

    Path(args.out_md).write_text("\n".join(md) + "\n", encoding="utf-8")

    print("WROTE", args.out_train_body, train_n)
    print("WROTE", args.out_val_body, val_n)
    print("WROTE", args.out_md)
    print("BODY_FRAME_ACTION_ANALYSIS_PASS")


if __name__ == "__main__":
    main()
