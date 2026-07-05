from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any

import numpy as np

def wrap_angle(angle: float) -> float:
    return float((angle + math.pi) % (2.0 * math.pi) - math.pi)

ACTION_NAMES = (
    "x_pos", "x_neg", "y_pos", "y_neg", "z_pos", "z_neg", "hover",
)

MOVE_VECTORS = np.asarray(
    [
        [1.0, 0.0, 0.0],
        [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, -1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 0.0, -1.0],
        [0.0, 0.0, 0.0],
    ],
    dtype=np.float32,
)

@dataclass
class SimpleUAVEnvConfig:
    grid_size: int = 11
    z_levels: int = 4
    dt: float = 1.0
    max_steps: int = 45
    speed: float = 1.0
    yaw_rate_limit: float = math.pi / 4.0
    goal_tolerance: float = 0.75
    seed: int = 0

class SimpleUAVNavigationEnv:
    def __init__(self, config: SimpleUAVEnvConfig | None = None) -> None:
        self.config = config or SimpleUAVEnvConfig()
        self.rng = np.random.default_rng(self.config.seed)
        self.state = np.zeros(4, dtype=np.float32)
        self.goal = np.zeros(3, dtype=np.float32)
        self.steps = 0

    @property
    def n_actions(self) -> int:
        return len(ACTION_NAMES)

    def reset(self, seed: int | None = None) -> dict[str, Any]:
        if seed is not None:
            self.rng = np.random.default_rng(seed)

        start = np.asarray([
            self.rng.integers(0, self.config.grid_size),
            self.rng.integers(0, self.config.grid_size),
            self.rng.integers(0, self.config.z_levels),
        ], dtype=np.float32)

        goal = np.asarray([
            self.rng.integers(0, self.config.grid_size),
            self.rng.integers(0, self.config.grid_size),
            self.rng.integers(0, self.config.z_levels),
        ], dtype=np.float32)

        while np.linalg.norm(goal - start) < 3.0:
            goal = np.asarray([
                self.rng.integers(0, self.config.grid_size),
                self.rng.integers(0, self.config.grid_size),
                self.rng.integers(0, self.config.z_levels),
            ], dtype=np.float32)

        self.state = np.asarray(
            [start[0], start[1], start[2], self.rng.uniform(-math.pi, math.pi)],
            dtype=np.float32,
        )
        self.goal = goal.astype(np.float32)
        self.steps = 0
        return self.observation()

    def observation(self) -> dict[str, Any]:
        rel = self.goal - self.state[:3]
        return {
            "state": self.state.astype(float).tolist(),
            "goal": self.goal.astype(float).tolist(),
            "relative_goal": rel.astype(float).tolist(),
            "step": int(self.steps),
        }

    def action_vector(self, action_index: int) -> list[float]:
        move = MOVE_VECTORS[int(action_index)] * self.config.speed
        yaw = float(self.state[3])

        if abs(float(move[0])) + abs(float(move[1])) > 1e-6:
            desired_yaw = math.atan2(float(move[1]), float(move[0]))
        else:
            desired_yaw = math.atan2(float(self.goal[1] - self.state[1]), float(self.goal[0] - self.state[0]))

        yaw_rate = wrap_angle(desired_yaw - yaw) / self.config.dt
        yaw_rate = float(np.clip(yaw_rate, -self.config.yaw_rate_limit, self.config.yaw_rate_limit))
        return [float(move[0]), float(move[1]), float(move[2]), yaw_rate]

    def step(self, action_index: int):
        prev_distance = float(np.linalg.norm(self.goal - self.state[:3]))
        action = np.asarray(self.action_vector(action_index), dtype=np.float32)

        next_state = self.state.copy()
        next_state[:3] = next_state[:3] + action[:3] * self.config.dt
        next_state[3] = wrap_angle(float(next_state[3] + action[3] * self.config.dt))

        penalty = 0.0
        max_xy = self.config.grid_size - 1
        max_z = self.config.z_levels - 1

        clipped = next_state.copy()
        clipped[0] = np.clip(clipped[0], 0.0, float(max_xy))
        clipped[1] = np.clip(clipped[1], 0.0, float(max_xy))
        clipped[2] = np.clip(clipped[2], 0.0, float(max_z))

        if not np.allclose(clipped[:3], next_state[:3]):
            penalty -= 1.0

        self.state = clipped.astype(np.float32)
        self.steps += 1

        distance = float(np.linalg.norm(self.goal - self.state[:3]))
        progress = prev_distance - distance
        reward = 0.5 * progress - 0.03 - 0.03 * distance + penalty

        success = distance <= self.config.goal_tolerance
        if success:
            reward += 10.0

        timeout = self.steps >= self.config.max_steps
        done = bool(success or timeout)

        info = {
            "action_name": ACTION_NAMES[int(action_index)],
            "action": action.astype(float).tolist(),
            "distance": distance,
            "success": bool(success),
            "timeout": bool(timeout),
        }
        return self.observation(), float(reward), done, info
