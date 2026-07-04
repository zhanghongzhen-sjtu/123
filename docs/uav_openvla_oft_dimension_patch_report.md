# UAV OpenVLA-OFT Dimension Patch Report

## Status

- MODEL_STAGE_CONFIRMED_BY_USER
- OPENVLA_OFT_UAV_LOCAL_SHAPE_SMOKE_PASS
- MODEL_WEIGHTS_NOT_LOADED
- TRAINING_NOT_STARTED

## UAV Dimensions

- ROBOT_PLATFORM = UAV
- NUM_ACTIONS_CHUNK = 8
- ACTION_DIM = 4
- PROPRIO_DIM = 4

## Checked Shapes

- proprio input: `[B, 4]`
- proprio projector output: `[B, llm_dim]`
- action head MLP input: `[B * 8, llm_dim * 4]`
- predicted actions: `[B, 8, 4]`

## Note

This is a local shape-only smoke. It does not run the full OpenVLA forward pass.

## Not Done

- No OpenVLA/openvla-7b checkpoint loaded.
- No checkpoint downloaded.
- No LoRA/OFT training.
- No closed-loop simulation.

## Next Step

Inspect the exact `L1RegressionActionHead.predict_action` hidden-state contract before wiring real OpenVLA hidden states.
