# UAV JSONL Dataset Collator-Ready Stub Report

## Status

- UAV_JSONL_COLLATOR_READY_STUB_PASS
- MODEL_NOT_LOADED
- TRAINING_NOT_STARTED
- OPENVLA_TOKENIZER_NOT_USED
- OPENVLA_IMAGE_TRANSFORM_NOT_USED

## Result

```json
{
  "status": "UAV_JSONL_COLLATOR_READY_STUB_PASS",
  "model_loaded": false,
  "training_started": false,
  "tokenizer": "fake_tokenizer_stub",
  "image_transform": "PIL_resize_224_stub",
  "train": {
    "jsonl": "data/processed/clean_train_timestamp_maps.jsonl",
    "rows_loaded": 32,
    "maps": {
      "BrushifyCountryRoads": 32
    },
    "batch_shapes": {
      "pixel_values": [
        8,
        3,
        224,
        224
      ],
      "input_ids": [
        8,
        128
      ],
      "attention_mask": [
        8,
        128
      ],
      "labels": [
        8,
        128
      ],
      "actions": [
        8,
        8,
        4
      ],
      "proprio": [
        8,
        4
      ]
    },
    "dataset_names": [
      "TravelUAV"
    ]
  },
  "val": {
    "jsonl": "data/processed/clean_val_timestamp_maps.jsonl",
    "rows_loaded": 32,
    "maps": {
      "Carla_Town02": 32
    },
    "batch_shapes": {
      "pixel_values": [
        8,
        3,
        224,
        224
      ],
      "input_ids": [
        8,
        128
      ],
      "attention_mask": [
        8,
        128
      ],
      "labels": [
        8,
        128
      ],
      "actions": [
        8,
        8,
        4
      ],
      "proprio": [
        8,
        4
      ]
    },
    "dataset_names": [
      "TravelUAV"
    ]
  }
}
```

## Interpretation

This confirms that TravelUAV JSONL can be mapped into OpenVLA-OFT collator-ready field names and tensor shapes using lightweight stubs.

This does not confirm compatibility with the real OpenVLA tokenizer, image transform, or model forward pass.