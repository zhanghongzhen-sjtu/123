# OpenVLA Processor Smoke Report

## Status

- OPENVLA_PROCESSOR_SMOKE_PASS
- MODEL_WEIGHTS_NOT_LOADED
- TRAINING_NOT_STARTED

## Result

```json
{
  "status": "OPENVLA_PROCESSOR_SMOKE_PASS",
  "model_id": "openvla/openvla-7b",
  "model_weights_loaded": false,
  "training_started": false,
  "jsonl": "data/processed/clean_train_timestamp_maps.jsonl",
  "image_path": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/frontcamera/000000.png",
  "instruction_chars": 407,
  "state_shape": [
    4
  ],
  "actions_shape": [
    8,
    4
  ],
  "processor_class": "PrismaticProcessor",
  "has_tokenizer": true,
  "has_image_processor": true,
  "token_shapes": {
    "input_ids": [
      1,
      102
    ],
    "attention_mask": [
      1,
      102
    ]
  },
  "pixel_shapes": {
    "pixel_values": [
      1,
      6,
      224,
      224
    ]
  },
  "combined_shapes": {
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
  }
}
```

## Interpretation

This smoke test loads the OpenVLA processor/tokenizer/image processor only.
It does not load openvla-7b model weights and does not start training.