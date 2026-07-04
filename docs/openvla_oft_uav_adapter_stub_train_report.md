# OpenVLA-OFT UAV Adapter Stub Report

- OPENVLA_OFT_UAV_ADAPTER_STUB_PASS
- MODEL_NOT_LOADED
- TRAINING_NOT_STARTED

- jsonl: `data/processed/clean_train_timestamp_maps.jsonl`
- total rows: `120`
- checked rows: `120`
- maps: `{'BrushifyCountryRoads': 60, 'BrushifyUrban': 60}`
- action chunk shapes: `{'8x4': 120}`

```json
{
  "dataset_name": "TravelUAV",
  "episode_id": "0008c004-9c02-40d3-928f-b7228c17a39d",
  "step_id": 0,
  "image_path": "data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/frontcamera/000000.png",
  "language_instruction_chars": 407,
  "proprio": [
    -540.9619750976562,
    -453.1080017089844,
    -39.50600051879883,
    0.2372481270116989
  ],
  "state": [
    -540.9619750976562,
    -453.1080017089844,
    -39.50600051879883,
    0.2372481270116989
  ],
  "action": [
    -0.25632749836174373,
    -0.6267476637951509,
    -0.5523580636035098,
    -0.44208744682595014
  ],
  "action_chunk_shape": [
    8,
    4
  ],
  "dt": 4.986106368,
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
```