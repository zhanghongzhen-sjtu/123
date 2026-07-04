import sys
import types
import importlib.util
from pathlib import Path

import torch


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    sys.modules["prismatic"] = types.ModuleType("prismatic")
    sys.modules["prismatic.vla"] = types.ModuleType("prismatic.vla")
    sys.modules["prismatic.models"] = types.ModuleType("prismatic.models")

    const_mod = load_module(
        "prismatic.vla.constants",
        "external/openvla-oft/prismatic/vla/constants.py",
    )

    print("ROBOT_PLATFORM", const_mod.ROBOT_PLATFORM)
    print("NUM_ACTIONS_CHUNK", const_mod.NUM_ACTIONS_CHUNK)
    print("ACTION_DIM", const_mod.ACTION_DIM)
    print("PROPRIO_DIM", const_mod.PROPRIO_DIM)

    assert const_mod.ROBOT_PLATFORM == "UAV"
    assert const_mod.NUM_ACTIONS_CHUNK == 8
    assert const_mod.ACTION_DIM == 4
    assert const_mod.PROPRIO_DIM == 4

    proj_mod = load_module(
        "prismatic.models.projectors",
        "external/openvla-oft/prismatic/models/projectors.py",
    )

    ah_mod = load_module(
        "prismatic.models.action_heads",
        "external/openvla-oft/prismatic/models/action_heads.py",
    )

    bsz = 2
    llm_dim = 64
    hidden_dim = 16

    proprio_projector = proj_mod.ProprioProjector(
        llm_dim=llm_dim,
        proprio_dim=const_mod.PROPRIO_DIM,
    )
    proprio = torch.randn(bsz, const_mod.PROPRIO_DIM)
    proprio_out = proprio_projector(proprio)

    action_head = ah_mod.L1RegressionActionHead(
        input_dim=llm_dim,
        hidden_dim=hidden_dim,
        action_dim=const_mod.ACTION_DIM,
    )

    # Shape-only smoke for the L1 regression head's internal MLP.
    # The head MLP expects input_dim * ACTION_DIM as its last dimension.
    mlp_in = torch.randn(bsz * const_mod.NUM_ACTIONS_CHUNK, llm_dim * const_mod.ACTION_DIM)
    pred_flat = action_head.model(mlp_in)
    pred = pred_flat.reshape(bsz, const_mod.NUM_ACTIONS_CHUNK, const_mod.ACTION_DIM)

    print("proprio_out", tuple(proprio_out.shape))
    print("pred_actions", tuple(pred.shape))

    assert proprio_out.shape == (bsz, llm_dim)
    assert pred.shape == (bsz, const_mod.NUM_ACTIONS_CHUNK, const_mod.ACTION_DIM)

    print("OPENVLA_OFT_UAV_LOCAL_SHAPE_SMOKE_PASS")
    print("MODEL_WEIGHTS_NOT_LOADED")
    print("TRAINING_NOT_STARTED")


if __name__ == "__main__":
    main()
