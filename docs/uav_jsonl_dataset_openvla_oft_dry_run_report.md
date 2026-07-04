# UAVJsonlDataset For OpenVLA-OFT Dry Run Report

## Status

- UAV_JSONL_DATASET_OPENVLA_OFT_DRY_RUN_PASS
- MODEL_WEIGHTS_NOT_LOADED
- TRAINING_NOT_STARTED

## Result

```json
{
  "status": "UAV_JSONL_DATASET_OPENVLA_OFT_DRY_RUN_PASS",
  "model_id": "openvla/openvla-7b",
  "processor_class": "PrismaticProcessor",
  "model_weights_loaded": false,
  "training_started": false,
  "train": {
    "split": "train",
    "jsonl": "data/processed/clean_train_timestamp_maps.jsonl",
    "dataset_len": 16,
    "batch_size": 4,
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
    "first_metadata": {
      "episode_id": "0008c004-9c02-40d3-928f-b7228c17a39d",
      "step_id": 0,
      "image": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/frontcamera/000000.png",
      "source": {
        "raw_file": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/log/000000.json",
        "next_raw_file": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/log/000005.json",
        "raw_episode_dir": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d",
        "map": "BrushifyCountryRoads",
        "frame": 0,
        "next_frame": 5,
        "timestamp": 1.7335701666972155e+18,
        "next_timestamp": 1.7335701716833219e+18,
        "dt_source": "timestamp",
        "raw_linear_velocity": [
          0.0,
          0.0,
          0.0
        ],
        "raw_angular_velocity": [
          0.0,
          0.0,
          0.0
        ],
        "target": {
          "object_name": "AASM_VolkswagenBeetle",
          "target": {
            "position": [
              -724.191162109375,
              -805.800537109375,
              -24.149229049682617
            ],
            "rotation": [
              0,
              0
            ]
          },
          "end": [
            -721.5805,
            -801.8415,
            -29.756
          ]
        }
      }
    }
  },
  "val": {
    "split": "val",
    "jsonl": "data/processed/clean_val_timestamp_maps.jsonl",
    "dataset_len": 16,
    "batch_size": 4,
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
    "first_metadata": {
      "episode_id": "01fa26b7-98aa-4284-b75d-d1fad1f81ee2",
      "step_id": 0,
      "image": "data/raw/TravelUAV/Carla_Town02/01fa26b7-98aa-4284-b75d-d1fad1f81ee2/frontcamera/000000.png",
      "source": {
        "raw_file": "data/raw/TravelUAV/Carla_Town02/01fa26b7-98aa-4284-b75d-d1fad1f81ee2/log/000000.json",
        "next_raw_file": "data/raw/TravelUAV/Carla_Town02/01fa26b7-98aa-4284-b75d-d1fad1f81ee2/log/000005.json",
        "raw_episode_dir": "data/raw/TravelUAV/Carla_Town02/01fa26b7-98aa-4284-b75d-d1fad1f81ee2",
        "map": "Carla_Town02",
        "frame": 0,
        "next_frame": 5,
        "timestamp": 1.741023761394426e+18,
        "next_timestamp": 1.7410237663925327e+18,
        "dt_source": "timestamp",
        "raw_linear_velocity": [
          0.0,
          0.0,
          0.0
        ],
        "raw_angular_velocity": [
          0.0,
          0.0,
          0.0
        ],
        "target": {
          "object_name": "SM_Woman44",
          "target": {
            "position": [
              42.18640899658203,
              183.91595458984375,
              -0.6575456857681274
            ],
            "rotation": [
              0,
              0
            ]
          },
          "end": [
            41.4005,
            187.4095,
            -2.526
          ]
        }
      }
    }
  }
}
```