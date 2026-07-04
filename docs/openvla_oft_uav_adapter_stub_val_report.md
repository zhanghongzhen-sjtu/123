# OpenVLA-OFT UAV Adapter Stub Report

- OPENVLA_OFT_UAV_ADAPTER_STUB_PASS
- MODEL_NOT_LOADED
- TRAINING_NOT_STARTED

- jsonl: `data/processed/clean_val_timestamp_maps.jsonl`
- total rows: `114`
- checked rows: `114`
- maps: `{'Carla_Town02': 54, 'Carla_Town03': 60}`
- action chunk shapes: `{'8x4': 114}`

```json
{
  "dataset_name": "TravelUAV",
  "episode_id": "01fa26b7-98aa-4284-b75d-d1fad1f81ee2",
  "step_id": 0,
  "image_path": "data/raw/TravelUAV/Carla_Town02/01fa26b7-98aa-4284-b75d-d1fad1f81ee2/frontcamera/000000.png",
  "language_instruction_chars": 369,
  "proprio": [
    69.0469970703125,
    241.37350463867188,
    -2.5260000228881836,
    -3.119737218959457
  ],
  "state": [
    69.0469970703125,
    241.37350463867188,
    -2.5260000228881836,
    -3.119737218959457
  ],
  "action": [
    -0.7692137064705468,
    -0.280254440836122,
    0.010606681434723396,
    0.06538285572998824
  ],
  "action_chunk_shape": [
    8,
    4
  ],
  "dt": 4.998106624,
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
```