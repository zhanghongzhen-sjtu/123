from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    episodes = defaultdict(list)

    with open(args.jsonl, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            state = r["state"]
            episodes[r["episode_id"]].append((float(state[0]), float(state[1])))

    if not episodes:
        raise SystemExit("No episodes found.")

    w, h = 1000, 1000
    margin = 70
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)

    xs = [p[0] for pts in episodes.values() for p in pts]
    ys = [p[1] for pts in episodes.values() for p in pts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    def map_xy(x, y):
        sx = margin + (x - xmin) / max(1e-6, xmax - xmin) * (w - 2 * margin)
        sy = h - margin - (y - ymin) / max(1e-6, ymax - ymin) * (h - 2 * margin)
        return sx, sy

    for i in range(11):
        x = margin + i * (w - 2 * margin) / 10
        y = margin + i * (h - 2 * margin) / 10
        draw.line((x, margin, x, h - margin), fill=(225, 225, 225))
        draw.line((margin, y, w - margin, y), fill=(225, 225, 225))

    colors = [
        "blue", "orange", "green", "red", "purple", "brown",
        "magenta", "gray", "cyan", "black",
    ]

    for idx, (ep, pts) in enumerate(sorted(episodes.items())):
        color = colors[idx % len(colors)]
        mapped = [map_xy(x, y) for x, y in pts]
        if len(mapped) >= 2:
            draw.line(mapped, fill=color, width=4)
        for p in mapped:
            draw.ellipse((p[0]-4, p[1]-4, p[0]+4, p[1]+4), fill=color)
        if mapped:
            s = mapped[0]
            g = mapped[-1]
            draw.ellipse((s[0]-8, s[1]-8, s[0]+8, s[1]+8), outline="black", width=3)
            draw.text((s[0]+8, s[1]-12), "S", fill="black")
            draw.rectangle((g[0]-8, g[1]-8, g[0]+8, g[1]+8), outline=color, width=3)
            draw.text((g[0]+8, g[1]-12), "G", fill=color)

    draw.rectangle((margin, margin, w-margin, h-margin), outline="black", width=2)
    draw.text((margin, h-35), "PPO expert trajectories: toy SimpleUAVNavigationEnv", fill="black")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print("WROTE", out)
    print("RL_EXPERT_TRAJECTORY_PLOT_PASS")

if __name__ == "__main__":
    main()
