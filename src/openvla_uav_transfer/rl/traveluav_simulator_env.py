from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


def wrap_angle(angle: float) -> float:
    return float((angle + math.pi) % (2.0 * math.pi) - math.pi)


@dataclass
class TravelUAVSimulatorConfig:
    max_steps: int = 300
    goal_tolerance: float = 1.0
    collision_penalty: float = 5.0
    success_reward: float = 10.0
    step_penalty: float = 0.01
    distance_weight: float = 0.02
    progress_weight: float = 1.0
    action_smooth_weight: float = 0.01


def compute_navigation_reward(
    prev_state,
    next_state,
    goal,
    *,
    action=None,
    prev_action=None,
    collision: bool = False,
    success: bool = False,
    timeout: bool = False,
    config: TravelUAVSimulatorConfig | None = None,
) -> float:
    cfg = config or TravelUAVSimulatorConfig()
    prev_state = np.asarray(prev_state, dtype=np.float32)
    next_state = np.asarray(next_state, dtype=np.float32)
    goal = np.asarray(goal, dtype=np.float32)

    prev_dist = float(np.linalg.norm(goal[:3] - prev_state[:3]))
    next_dist = float(np.linalg.norm(goal[:3] - next_state[:3]))
    progress = prev_dist - next_dist

    reward = cfg.progress_weight * progress
    reward -= cfg.step_penalty
    reward -= cfg.distance_weight * next_dist

    if action is not None and prev_action is not None:
        action = np.asarray(action, dtype=np.float32)
        prev_action = np.asarray(prev_action, dtype=np.float32)
        reward -= cfg.action_smooth_weight * float(np.linalg.norm(action - prev_action))

    if collision:
        reward -= cfg.collision_penalty
    if success:
        reward += cfg.success_reward
    if timeout:
        reward -= 1.0

    return float(reward)


class TravelUAVSimulatorEnv:
    """Real simulator wrapper contract.

    This class defines the interface required for PPO/SAC:
      reset() -> observation
      step(action=[vx,vy,vz,yaw_rate]) -> observation, reward, done, info

    A real backend is still required. Without backend, this class intentionally
    refuses to run real simulator training.
    """

    def __init__(self, backend=None, config: TravelUAVSimulatorConfig | None = None):
        self.backend = backend
        self.config = config or TravelUAVSimulatorConfig()
        self.prev_action = None

    def reset(self, *args, **kwargs) -> dict[str, Any]:
        if self.backend is None:
            raise RuntimeError("REAL_TRAVELUAV_SIMULATOR_BACKEND_NOT_CONFIGURED")
        self.prev_action = None
        return self.backend.reset(*args, **kwargs)

    def step(self, action) -> tuple[dict[str, Any], float, bool, dict[str, Any]]:
        if self.backend is None:
            raise RuntimeError("REAL_TRAVELUAV_SIMULATOR_BACKEND_NOT_CONFIGURED")

        obs, backend_reward, done, info = self.backend.step(action)
        if backend_reward is not None:
            reward = float(backend_reward)
        else:
            reward = compute_navigation_reward(
                info["prev_state"],
                obs["state"],
                info["goal"],
                action=action,
                prev_action=self.prev_action,
                collision=bool(info.get("collision", False)),
                success=bool(info.get("success", False)),
                timeout=bool(info.get("timeout", False)),
                config=self.config,
            )
        self.prev_action = np.asarray(action, dtype=np.float32)
        return obs, reward, bool(done), info


class ReplayTravelUAVJsonlEnv:
    """Offline replay environment for interface validation only.

    It replays converted TravelUAV JSONL rows and derives goal from the final
    state of each episode. It is not an interactive simulator, so PPO should not
    be trained on this class.
    """

    def __init__(self, jsonl: str | Path, max_rows: int = 1000, config: TravelUAVSimulatorConfig | None = None):
        self.jsonl = Path(jsonl)
        self.max_rows = max_rows
        self.config = config or TravelUAVSimulatorConfig()
        self.episodes = self._load_episodes()
        self.ep_ids = sorted(self.episodes)
        self.ep_idx = -1
        self.step_idx = 0
        self.prev_action = None

    def _load_episodes(self):
        episodes = {}
        with self.jsonl.open("r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if self.max_rows and i >= self.max_rows:
                    break
                if not line.strip():
                    continue
                row = json.loads(line)
                episodes.setdefault(str(row["episode_id"]), []).append(row)
        for rows in episodes.values():
            rows.sort(key=lambda r: int(r.get("step_id", 0)))
        return {k: v for k, v in episodes.items() if len(v) >= 2}

    def reset(self):
        if not self.ep_ids:
            raise RuntimeError(f"No valid episodes in {self.jsonl}")
        self.ep_idx = (self.ep_idx + 1) % len(self.ep_ids)
        self.step_idx = 0
        self.prev_action = None
        return self._observation()

    def _current_rows(self):
        return self.episodes[self.ep_ids[self.ep_idx]]

    def _goal(self):
        rows = self._current_rows()
        return np.asarray(rows[-1]["state"][:3], dtype=np.float32)

    def _observation(self):
        rows = self._current_rows()
        row = rows[self.step_idx]
        state = np.asarray(row["state"], dtype=np.float32)
        goal = self._goal()
        return {
            "state": state.astype(float).tolist(),
            "goal": goal.astype(float).tolist(),
            "relative_goal": (goal - state[:3]).astype(float).tolist(),
            "image": row.get("image", ""),
            "instruction": row.get("instruction", ""),
            "episode_id": row.get("episode_id", ""),
            "step_id": row.get("step_id", self.step_idx),
        }

    def step(self, action=None):
        rows = self._current_rows()
        prev_row = rows[self.step_idx]
        prev_state = np.asarray(prev_row["state"], dtype=np.float32)

        self.step_idx += 1
        done = self.step_idx >= len(rows) - 1
        obs = self._observation()
        next_state = np.asarray(obs["state"], dtype=np.float32)
        goal = self._goal()

        expert_action = np.asarray(prev_row.get("action", [0, 0, 0, 0]), dtype=np.float32)
        used_action = expert_action if action is None else np.asarray(action, dtype=np.float32)

        distance = float(np.linalg.norm(goal - next_state[:3]))
        success = distance <= self.config.goal_tolerance

        reward = compute_navigation_reward(
            prev_state,
            next_state,
            goal,
            action=used_action,
            prev_action=self.prev_action,
            success=success,
            timeout=done and not success,
            config=self.config,
        )
        self.prev_action = used_action

        info = {
            "expert_action": expert_action.astype(float).tolist(),
            "distance": distance,
            "success": bool(success),
            "replay_only": True,
        }
        return obs, reward, bool(done), info
