# Action Head Hidden-State Contract

## Status

- MODEL_STAGE_CONFIRMED_BY_USER
- ACTION_HEAD_SOURCE_INSPECTED
- MODEL_WEIGHTS_NOT_LOADED
- TRAINING_NOT_STARTED

## Context

The UAV target is:

- `NUM_ACTIONS_CHUNK = 8`
- `ACTION_DIM = 4`
- `PROPRIO_DIM = 4`

The action target shape is:

- `actions = [B, 8, 4]`

## L1RegressionActionHead Contract

`L1RegressionActionHead` constructs an MLP whose input dimension is:

- `input_dim * ACTION_DIM`

and output dimension is:

- `ACTION_DIM`

The `predict_action()` path reshapes selected action hidden states into:

- `[B, NUM_ACTIONS_CHUNK, -1]`

then applies the MLP per chunk step.

Therefore, the hidden states selected from OpenVLA text positions must be compatible with:

- last dimension = `input_dim * ACTION_DIM`

after the action-token masking and reshape path.

## Important Risk

The local smoke confirmed that the internal MLP can map:

- `[B * 8, llm_dim * 4] -> [B * 8, 4] -> [B, 8, 4]`

But the full `predict_action()` path depends on how OpenVLA hidden states are selected by:

- `current_action_mask`
- `next_actions_mask`
- action token positions

This still needs a real one-batch OpenVLA hidden-state smoke before training.

## Diffusion Head

The diffusion head also uses:

- `NUM_ACTIONS_CHUNK`
- `ACTION_DIM`

So UAV diffusion action prediction must use `[B, 8, 4]`.

## Current Decision

The UAV constants and action target dimensions are consistent at the local module level.

The full OpenVLA hidden-state contract is not yet validated.

## Next Step

Before training:

1. run tokenizer/image-transform smoke;
2. run one-batch model forward smoke;
3. inspect selected action hidden-state tensor shape;
4. only then run a tiny optimizer-step smoke if separately confirmed.
