from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import gymnasium as gym
import numpy as np
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy

from src.openvla_uav_transfer.rl.simple_uav_env import SimpleUAVEnvConfig, SimpleUAVNavigationEnv
from src.openvla_uav_transfer.adapters.uav_action_adapter import build_action_chunk


class GymSimpleUAVEnv(gym.Env):
    metadata = {}

    def __init__(self, seed: int = 0):
        super().__init__()
        cfg = SimpleUAVEnvConfig(seed=seed, max_steps=45)
        self.core = SimpleUAVNavigationEnv(cfg)
        self.action_space = spaces.Discrete(self.core.n_actions)
        self.observation_space = spaces.Box(low=-1.0, high=1.0, shape=(12,), dtype=np.float32)

    def _to_obs(self, obs):
        cfg = self.core.config
        state = np.asarray(obs["state"], dtype=np.float32)
        goal = np.asarray(obs["goal"], dtype=np.float32)
        rel = np.asarray(obs["relative_goal"], dtype=np.float32)

        max_xy = max(1.0, float(cfg.grid_size - 1))
        max_z = max(1.0, float(cfg.z_levels - 1))
        max_rel = max_xy

        x = (state[0] / max_xy) * 2.0 - 1.0
        y = (state[1] / max_xy) * 2.0 - 1.0
        z = (state[2] / max_z) * 2.0 - 1.0
        yaw = float(state[3])

        gx = (goal[0] / max_xy) * 2.0 - 1.0
        gy = (goal[1] / max_xy) * 2.0 - 1.0
        gz = (goal[2] / max_z) * 2.0 - 1.0

        rx = np.clip(rel[0] / max_rel, -1.0, 1.0)
        ry = np.clip(rel[1] / max_rel, -1.0, 1.0)
        rz = np.clip(rel[2] / max_z, -1.0, 1.0)
        step = np.clip(float(obs["step"]) / float(cfg.max_steps), 0.0, 1.0)

        return np.asarray(
            [x, y, z, math.sin(yaw), math.cos(yaw), gx, gy, gz, rx, ry, rz, step],
            dtype=np.float32,
        )

    def reset(self, seed=None, options=None):
        obs = self.core.reset(seed=seed)
        return self._to_obs(obs), {}

    def step(self, action):
        obs, reward, done, info = self.core.step(int(action))
        return self._to_obs(obs), float(reward), bool(done), False, info


def export_success_rollouts(model, out_path, requested_episodes=32, max_attempts=256, seed=1000, chunk_size=8):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    exported = 0
    attempts = 0

    while exported < requested_episodes and attempts < max_attempts:
        env = GymSimpleUAVEnv(seed=seed + attempts)
        obs, _ = env.reset(seed=seed + attempts)
        episode_rows = []
        actions = []
        done = False
        last_info = {}
        step_id = 0
        episode_id = f"ppo_simple_uav_{exported:04d}"

        while not done:
            state_before = env.core.state.astype(float).tolist()
            action_idx, _ = model.predict(obs, deterministic=True)
            action_idx = int(action_idx)
            action_vec = env.core.action_vector(action_idx)

            obs, reward, terminated, truncated, info = env.step(action_idx)
            done = bool(terminated or truncated)
            last_info = info
            actions.append(action_vec)

            episode_rows.append(
                {
                    "dataset": "PPOExpertToy",
                    "episode_id": episode_id,
                    "step_id": step_id,
                    "image": "synthetic://ppo_simple_uav/no_image.png",
                    "instruction": "Navigate the UAV to the goal position in the toy RL environment.",
                    "state": state_before,
                    "action": action_vec,
                    "action_chunk": [],
                    "dt": 1.0,
                    "source": {
                        "stage": "rl_ppo_expert_smoke",
                        "algorithm": "ppo",
                        "environment": "SimpleUAVNavigationEnv",
                        "simulator": "toy_point_mass",
                        "success": bool(info.get("success", False)),
                        "distance": float(info.get("distance", 0.0)),
                    },
                }
            )
            step_id += 1

        attempts += 1
        if not last_info.get("success", False):
            continue

        for i, row in enumerate(episode_rows):
            row["action_chunk"] = build_action_chunk(actions, i, chunk_size)
            rows.append(row)
        exported += 1

    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return {"requested": requested_episodes, "exported": exported, "attempts": attempts, "rows": len(rows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--total-timesteps", type=int, default=500000)
    ap.add_argument("--eval-episodes", type=int, default=32)
    ap.add_argument("--export-episodes", type=int, default=32)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--model-dir", default="checkpoints/rl/ppo_simple_uav_full")
    ap.add_argument("--out", default="data/rl_debug/ppo_simple_uav_expert_full.jsonl")
    ap.add_argument("--report-json", default="logs/rl/ppo_simple_uav_full_report.json")
    ap.add_argument("--report-md", default="docs/ppo_simple_uav_full_report.md")
    args = ap.parse_args()

    model_dir = Path(args.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)

    env = Monitor(GymSimpleUAVEnv(seed=args.seed))
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        seed=args.seed,
        device=args.device,
        tensorboard_log="logs/rl/tensorboard",
        learning_rate=3e-4,
        n_steps=1024,
        batch_size=256,
        gamma=0.98,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
    )

    model.learn(total_timesteps=args.total_timesteps, progress_bar=True)
    model_path = model_dir / "ppo_simple_uav.zip"
    model.save(model_path)

    eval_env = Monitor(GymSimpleUAVEnv(seed=args.seed + 999))
    mean_reward, std_reward = evaluate_policy(
        model,
        eval_env,
        n_eval_episodes=args.eval_episodes,
        deterministic=True,
    )

    export = export_success_rollouts(
        model,
        args.out,
        requested_episodes=args.export_episodes,
        seed=args.seed + 10000,
    )

    report = {
        "status": "PPO_SIMPLE_UAV_FULL_SMOKE_PASS",
        "method": "ppo",
        "environment": "SimpleUAVNavigationEnv",
        "total_timesteps": args.total_timesteps,
        "eval_mean_reward": float(mean_reward),
        "eval_std_reward": float(std_reward),
        "export": export,
        "model_path": str(model_path),
        "out": args.out,
        "openvla_training_started": False,
        "lora_oft_started": False,
        "diffusion_policy_training_started": False,
        "real_traveluav_simulator_started": False,
    }

    Path(args.report_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = "# PPO Simple UAV Full Smoke Report\n\n```json\n" + json.dumps(report, ensure_ascii=False, indent=2) + "\n```\n"
    Path(args.report_md).write_text(md, encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("PPO_SIMPLE_UAV_FULL_SMOKE_PASS")
    print("NOT_REAL_TRAVELUAV_SIMULATOR_TRAINING")


if __name__ == "__main__":
    main()
