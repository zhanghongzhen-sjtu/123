# OpenVLA Real Processor Collator Smoke Report

## Status

- OPENVLA_REAL_PROCESSOR_COLLATOR_SMOKE_PASS
- MODEL_WEIGHTS_NOT_LOADED
- TRAINING_NOT_STARTED

## Result

```json
{
  "status": "OPENVLA_REAL_PROCESSOR_COLLATOR_SMOKE_PASS",
  "model_id": "openvla/openvla-7b",
  "processor_class": "PrismaticProcessor",
  "model_weights_loaded": false,
  "training_started": false,
  "train": {
    "split": "train",
    "jsonl": "data/processed/clean_train_timestamp_maps.jsonl",
    "rows_loaded": 16,
    "maps": {
      "BrushifyCountryRoads": 16
    },
    "batch_shapes": {
      "pixel_values": [
        4,
        6,
        224,
        224
      ],
      "input_ids": [
        4,
        102
      ],
      "attention_mask": [
        4,
        102
      ],
      "labels": [
        4,
        102
      ],
      "actions": [
        4,
        8,
        4
      ],
      "proprio": [
        4,
        4
      ]
    },
    "dataset_names": [
      "TravelUAV"
    ],
    "pad_token_id": 32000,
    "model_max_length_used": 2048
  },
  "val": {
    "split": "val",
    "jsonl": "data/processed/clean_val_timestamp_maps.jsonl",
    "rows_loaded": 16,
    "maps": {
      "Carla_Town02": 16
    },
    "batch_shapes": {
      "pixel_values": [
        4,
        6,
        224,
        224
      ],
      "input_ids": [
        4,
        99
      ],
      "attention_mask": [
        4,
        99
      ],
      "labels": [
        4,
        99
      ],
      "actions": [
        4,
        8,
        4
      ],
      "proprio": [
        4,
        4
      ]
    },
    "dataset_names": [
      "TravelUAV"
    ],
    "pad_token_id": 32000,
    "model_max_length_used": 2048
  }
}
```

## Interpretation

This smoke test uses the real OpenVLA processor/tokenizer/image processor to create collator-ready tensors from TravelUAV JSONL.

It does not load OpenVLA/openvla-7b model weights and does not start training.