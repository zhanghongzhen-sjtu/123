# OpenVLA One-Batch Forward Smoke Report

## Status

- OPENVLA_ONE_BATCH_FORWARD_SMOKE_PASS
- MODEL_WEIGHTS_LOADED_FOR_SMOKE
- TRAINING_NOT_STARTED
- LORA_OFT_NOT_STARTED

## Result

```json
{
  "status": "OPENVLA_ONE_BATCH_FORWARD_SMOKE_PASS",
  "model_id": "openvla/openvla-7b",
  "device": "cuda",
  "image_path": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/frontcamera/000000.png",
  "instruction_chars": 407,
  "training_started": false,
  "lora_oft_started": false,
  "closed_loop_eval_started": false,
  "input_shapes": {
    "input_ids": [
      1,
      102
    ],
    "attention_mask": [
      1,
      102
    ],
    "pixel_values": [
      1,
      6,
      224,
      224
    ]
  },
  "generate_shape": [
    1,
    103
  ],
  "forward_mode": "generate_max_new_tokens_1",
  "cuda_max_memory_gb": 14.348
}
```