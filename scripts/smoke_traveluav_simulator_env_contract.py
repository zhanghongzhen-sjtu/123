from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.openvla_uav_transfer.rl.traveluav_simulator_env import (
    ReplayTravelUAVJsonlEnv,
    TravelUAVSimulatorEnv,
    compute_navigation_reward,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", default="data/processed/full_clean_val_timestamp.jsonl")
    ap.add_argument("--max-rows", type=int, default=500)
    ap.add_argument("--rollout-episodes", type=int, default=5)
    ap.add_argument("--out-json", default="logs/rl/traveluav_simulator_env_contract_report.json")
    ap.add_argument("--out-md", default="docs/traveluav_simulator_env_contract_report.md")
    args = ap.parse_args()

    # Real wrapper must refuse to run without backend.
    missing_backend_ok = False
    try:
        TravelUAVSimulatorEnv().reset()
    except RuntimeError as e:
        missing_backend_ok = "REAL_TRAVELUAV_SIMULATOR_BACKEND_NOT_CONFIGURED" in str(e)

    # Reward sanity check.
    prev_state = [0, 0, 0, 0]
    goal = [5, 0, 0]
    toward_state = [1, 0, 0, 0]
    away_state = [-1, 0, 0, 0]
    reward_toward = compute_navigation_reward(prev_state, toward_state, goal)
    reward_away = compute_navigation_reward(prev_state, away_state, goal)
    reward_sanity_ok = reward_toward > reward_away

    replay = ReplayTravelUAVJsonlEnv(args.jsonl, max_rows=args.max_rows)
    rewards = []
    distances = []
    episodes = 0
    rows = 0

    for _ in range(args.rollout_episodes):
        obs = replay.reset()
        done = False
        episodes += 1
        while not done:
            obs, reward, done, info = replay.step()
            rewards.append(float(reward))
            distances.append(float(info["distance"]))
            rows += 1

    report = {
        "status": "TRAVELUAV_SIMULATOR_ENV_CONTRACT_PASS",
        "jsonl": args.jsonl,
        "max_rows": args.max_rows,
        "missing_backend_guard_ok": missing_backend_ok,
        "reward_sanity_ok": reward_sanity_ok,
        "reward_toward": reward_toward,
        "reward_away": reward_away,
        "replay_episodes": episodes,
        "replay_steps": rows,
        "reward_mean": float(np.mean(rewards)) if rewards else None,
        "reward_min": float(np.min(rewards)) if rewards else None,
        "reward_max": float(np.max(rewards)) if rewards else None,
        "distance_mean": float(np.mean(distances)) if distances else None,
        "real_simulator_started": False,
        "ppo_training_started": False,
        "openvla_training_started": False,
    }

    assert missing_backend_ok
    assert reward_sanity_ok

    Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = "# TravelUAV Simulator Env Contract Report\n\n"
    md += "```json\n" + json.dumps(report, ensure_ascii=False, indent=2) + "\n```\n\n"
    md += "## Interpretation\n\n"
    md += "This validates the interface contract for replacing the toy PPO environment with a real TravelUAV simulator backend.\n\n"
    md += "The replay environment is only for interface and reward sanity checks. It must not be treated as interactive PPO training.\n"
    Path(args.out_md).write_text(md, encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("TRAVELUAV_SIMULATOR_ENV_CONTRACT_PASS")
    print("REAL_SIMULATOR_NOT_STARTED")
    print("PPO_NOT_STARTED")


if __name__ == "__main__":
    main()
