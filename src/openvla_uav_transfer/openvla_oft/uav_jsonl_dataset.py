from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

IGNORE_INDEX = -100


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def _vec(values: Any, dim: int, name: str) -> np.ndarray:
    if not isinstance(values, list) or len(values) != dim:
        raise ValueError(f"{name} must be length {dim}")
    if not all(_is_number(v) for v in values):
        raise ValueError(f"{name} has invalid numeric values")
    return np.asarray(values, dtype=np.float32)


def _resolve_image(path: str, image_root: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else Path(image_root) / p


def build_openvla_prompt(instruction: str) -> str:
    return f"What action should the robot take to {instruction}?"


class UAVJsonlDatasetForOpenVLAOFT(Dataset):
    def __init__(
        self,
        jsonl_path: str | Path,
        processor: Any,
        image_root: str | Path = ".",
        max_rows: Optional[int] = None,
        action_chunk_size: int = 8,
        action_dim: int = 4,
        proprio_dim: int = 4,
        mask_policy: str = "last_token",
    ) -> None:
        self.jsonl_path = Path(jsonl_path)
        self.processor = processor
        self.image_root = Path(image_root)
        self.action_chunk_size = action_chunk_size
        self.action_dim = action_dim
        self.proprio_dim = proprio_dim
        self.mask_policy = mask_policy
        self.rows = self._load_rows(max_rows)

    def _load_rows(self, max_rows: Optional[int]) -> List[Dict[str, Any]]:
        rows = []
        with self.jsonl_path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                row["_line_no"] = line_no
                rows.append(row)
                if max_rows is not None and len(rows) >= max_rows:
                    break
        if not rows:
            raise ValueError(f"empty dataset: {self.jsonl_path}")
        return rows

    def __len__(self) -> int:
        return len(self.rows)

    def _make_labels(self, input_ids: torch.Tensor) -> torch.Tensor:
        labels = input_ids.clone()
        if self.mask_policy == "none":
            return labels
        if self.mask_policy == "last_token":
            labels[:-1] = IGNORE_INDEX
            return labels
        raise ValueError(f"unsupported mask_policy: {self.mask_policy}")

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        row = self.rows[idx]
        line_no = row.get("_line_no", idx)

        if row.get("dataset") != "TravelUAV":
            raise ValueError(f"{self.jsonl_path}:{line_no}: dataset must be TravelUAV")

        instruction = row.get("instruction")
        if not isinstance(instruction, str) or not instruction.strip():
            raise ValueError(f"{self.jsonl_path}:{line_no}: empty instruction")

        img_path = _resolve_image(row["image"], self.image_root)
        if not img_path.exists():
            raise FileNotFoundError(f"{self.jsonl_path}:{line_no}: image not found: {img_path}")

        image = Image.open(img_path).convert("RGB")
        prompt = build_openvla_prompt(instruction)

        tokenized = self.processor.tokenizer(prompt, add_special_tokens=True, return_tensors=None)
        input_ids = torch.tensor(tokenized["input_ids"], dtype=torch.long)
        labels = self._make_labels(input_ids)

        pixels = self.processor.image_processor(images=image, return_tensors="pt")
        pixel_values = pixels["pixel_values"][0]

        proprio = _vec(row["state"], self.proprio_dim, "state/proprio")

        chunk = row.get("action_chunk")
        if not isinstance(chunk, list) or len(chunk) != self.action_chunk_size:
            raise ValueError(f"{self.jsonl_path}:{line_no}: action_chunk must be [{self.action_chunk_size},{self.action_dim}]")
        actions = np.stack([_vec(a, self.action_dim, "action_chunk step") for a in chunk], axis=0)

        return {
            "pixel_values": pixel_values,
            "input_ids": input_ids,
            "labels": labels,
            "actions": actions,
            "proprio": proprio,
            "dataset_name": "TravelUAV",
            "metadata": {
                "episode_id": str(row.get("episode_id")),
                "step_id": int(row.get("step_id")),
                "image": str(img_path),
                "source": row.get("source", {}),
            },
        }
