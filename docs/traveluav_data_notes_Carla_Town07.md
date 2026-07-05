# TravelUAV Data Notes

## Inspection Scope
- TravelUAV root: `external/TravelUAV`
- Dataset root: `data/raw/TravelUAV/Carla_Town07`
- Dataset root exists: `True`
- Found `merged_data.json`: `0` sample path(s)
- Found raw episode dirs with `log/` and `frontcamera/`: `20` sample path(s)

> 已发现真实 TravelUAV raw episode 目录，但当前子集未预生成 `merged_data.json`。本项目转换脚本可直接从 `log/*.json` 与 `frontcamera/*.png` 生成 debug JSONL；后续若要完全复刻 TravelUAV/AeroVLA 流程，可再运行 TravelUAV 的 `generate_merged_json.py`。

## Repository Structure Summary

### `.`
- .git/
- .git/HEAD
- .git/branches/
- .git/config
- .git/description
- .git/hooks/
- .git/index
- .git/info/
- .git/logs/
- .git/objects/
- .git/packed-refs
- .git/refs/
- .git/shallow
- .gitattributes
- Model/
- Model/LLaMA-UAV/
- README.md
- airsim_plugin/
- airsim_plugin/AirVLNSimulatorClientTool.py
- airsim_plugin/AirVLNSimulatorServerTool.py
- airsim_plugin/__pycache__/
- data/
- data/meta/
- data/traj_train/
- data/uav_dataset/
- header.png
- requirement.txt
- scripts/
- scripts/dagger_NYC.sh
- scripts/eval.sh
- scripts/metric.sh
- src/
- src/common/
- src/model_wrapper/
- src/vlnce_src/
- utils/
- utils/CN.py
- utils/__pycache__/
- utils/env_utils_uav.py
- utils/env_vector_uav.py
- utils/logger.py
- utils/metric.py
- utils/pickle5_multiprocessing.py
- utils/utils.py

### `data`
- meta/
- meta/map_spawnarea_info.json
- meta/object_description.json
- traj_train/
- traj_train/train_balance.json
- traj_train/val_8s_8k.json
- uav_dataset/
- uav_dataset/seen_valset.json
- uav_dataset/trainset.json
- uav_dataset/unseen_valset.json

### `scripts`
- dagger_NYC.sh
- eval.sh
- metric.sh

### `src`
- common/
- common/__pycache__/
- common/param.py
- model_wrapper/
- model_wrapper/__pycache__/
- model_wrapper/base_model.py
- model_wrapper/travel_llm.py
- model_wrapper/utils/
- vlnce_src/
- vlnce_src/__pycache__/
- vlnce_src/assist.py
- vlnce_src/closeloop_util.py
- vlnce_src/dagger.py
- vlnce_src/dino_monitor_online.py
- vlnce_src/env_uav.py
- vlnce_src/eval.py

### `Model/LLaMA-UAV/tools`
- generate_merged_json.py
- preprocess_image2tensor.py

## Candidate Data Entry Files

- `data/raw/TravelUAV/Carla_Town07/004d6e1f-248f-4804-881d-635f5a05e8bb/mark.json`
- `data/raw/TravelUAV/Carla_Town07/004d6e1f-248f-4804-881d-635f5a05e8bb/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/07dc3754-4b63-4d67-a28e-d007e71f45c4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/07dc3754-4b63-4d67-a28e-d007e71f45c4/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/07df84e1-6da7-427a-88ba-603fa1aa24b2/mark.json`
- `data/raw/TravelUAV/Carla_Town07/07df84e1-6da7-427a-88ba-603fa1aa24b2/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/086846df-ca48-4690-80f2-ceae362c0b0d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/086846df-ca48-4690-80f2-ceae362c0b0d/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/0c625b2c-fa65-40d8-a727-547dc7dcd440/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0c625b2c-fa65-40d8-a727-547dc7dcd440/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/0cc61a3a-f9d0-43f1-ace7-74fc96e040ac/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0cc61a3a-f9d0-43f1-ace7-74fc96e040ac/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/0cf8413d-e441-459f-841a-a33cb12563fe/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0cf8413d-e441-459f-841a-a33cb12563fe/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/14854721-e5a0-407a-b511-19467ee300dd/mark.json`
- `data/raw/TravelUAV/Carla_Town07/14854721-e5a0-407a-b511-19467ee300dd/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/14cac25a-9462-4214-bdd9-30537c476d74/mark.json`
- `data/raw/TravelUAV/Carla_Town07/14cac25a-9462-4214-bdd9-30537c476d74/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/15515bbb-96e2-4fa5-b172-8697bd81c30d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/15515bbb-96e2-4fa5-b172-8697bd81c30d/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/193d0c46-d133-4e23-a158-2802e206094d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/193d0c46-d133-4e23-a158-2802e206094d/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/196017ac-5458-4a44-9652-adb2ddd01013/mark.json`
- `data/raw/TravelUAV/Carla_Town07/196017ac-5458-4a44-9652-adb2ddd01013/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/19ec1266-c1c6-4257-ac0c-eab41102a6a4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/19ec1266-c1c6-4257-ac0c-eab41102a6a4/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/1db41498-6189-425f-b0dd-cc2c388df9b5/mark.json`
- `data/raw/TravelUAV/Carla_Town07/1db41498-6189-425f-b0dd-cc2c388df9b5/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/1df027d2-699a-4c3d-a84c-3e05c565b5e4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/1df027d2-699a-4c3d-a84c-3e05c565b5e4/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/1e6dc9de-c86b-4895-9c58-2ba338a88ae4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/1e6dc9de-c86b-4895-9c58-2ba338a88ae4/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/21773f09-3210-4581-971e-639e15ad3afb/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21773f09-3210-4581-971e-639e15ad3afb/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/21aaec2b-cde9-4ed3-9975-2a45dc2c3217/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21aaec2b-cde9-4ed3-9975-2a45dc2c3217/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/21ca74bf-69ed-4f9e-a66b-aeb6aa9ee8b1/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21ca74bf-69ed-4f9e-a66b-aeb6aa9ee8b1/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/27c2f769-8913-47a4-b780-a1507b30e934/mark.json`
- `data/raw/TravelUAV/Carla_Town07/27c2f769-8913-47a4-b780-a1507b30e934/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/295fe8e7-1167-4724-8c95-e21b80c998c3/mark.json`
- `data/raw/TravelUAV/Carla_Town07/295fe8e7-1167-4724-8c95-e21b80c998c3/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/2977001c-4194-4927-986e-731b0ff80925/mark.json`
- `data/raw/TravelUAV/Carla_Town07/2977001c-4194-4927-986e-731b0ff80925/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/2dcf6969-7fd3-4553-8dde-39bf77b6424f/mark.json`
- `data/raw/TravelUAV/Carla_Town07/2dcf6969-7fd3-4553-8dde-39bf77b6424f/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/2f3b431e-5136-4d3d-8f2c-0c0702b4386d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/2f3b431e-5136-4d3d-8f2c-0c0702b4386d/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/30626553-5aa5-418d-92bf-70cf68a6633c/mark.json`
- `data/raw/TravelUAV/Carla_Town07/30626553-5aa5-418d-92bf-70cf68a6633c/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/34dc49cc-9570-44a4-a36c-b9259c7977e2/mark.json`
- `data/raw/TravelUAV/Carla_Town07/34dc49cc-9570-44a4-a36c-b9259c7977e2/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/354aad0f-c06a-479d-8c49-257c34cd19b1/mark.json`
- `data/raw/TravelUAV/Carla_Town07/354aad0f-c06a-479d-8c49-257c34cd19b1/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/3bf37b50-355e-4c64-a8da-7ab77fc27324/mark.json`
- `data/raw/TravelUAV/Carla_Town07/3bf37b50-355e-4c64-a8da-7ab77fc27324/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/3c1e25f6-cde2-4d3b-9612-54a6fa53844b/mark.json`
- `data/raw/TravelUAV/Carla_Town07/3c1e25f6-cde2-4d3b-9612-54a6fa53844b/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/4297394b-bd20-48f6-9006-6ecb184ad467/mark.json`
- `data/raw/TravelUAV/Carla_Town07/4297394b-bd20-48f6-9006-6ecb184ad467/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/43ec1c75-b445-465f-bd0d-f2484710d68d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/43ec1c75-b445-465f-bd0d-f2484710d68d/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/48ab318b-1591-4009-b0f1-30100dc7e6f1/mark.json`
- `data/raw/TravelUAV/Carla_Town07/48ab318b-1591-4009-b0f1-30100dc7e6f1/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/48e21e14-d6aa-443e-96f3-72361e006fe9/mark.json`
- `data/raw/TravelUAV/Carla_Town07/48e21e14-d6aa-443e-96f3-72361e006fe9/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/4dde8a17-35b0-44d9-8d03-97cfc46e6e82/mark.json`
- `data/raw/TravelUAV/Carla_Town07/4dde8a17-35b0-44d9-8d03-97cfc46e6e82/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/4e0c4f7e-6c03-43db-87ee-d416e2f46540/mark.json`
- `data/raw/TravelUAV/Carla_Town07/4e0c4f7e-6c03-43db-87ee-d416e2f46540/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/5388513c-a78f-4d66-80b2-b9eab0ea582d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/5388513c-a78f-4d66-80b2-b9eab0ea582d/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/5412543d-cd59-4df6-b3c9-1d262c2b6f91/mark.json`
- `data/raw/TravelUAV/Carla_Town07/5412543d-cd59-4df6-b3c9-1d262c2b6f91/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/594c4b93-bf90-49d5-b13f-f86670970fce/mark.json`
- `data/raw/TravelUAV/Carla_Town07/594c4b93-bf90-49d5-b13f-f86670970fce/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/597db4bf-3d4d-43a7-b0ea-a2be4f983e35/mark.json`
- `data/raw/TravelUAV/Carla_Town07/597db4bf-3d4d-43a7-b0ea-a2be4f983e35/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/5cf434d4-d865-4281-b45c-8595b517e7a6/mark.json`
- `data/raw/TravelUAV/Carla_Town07/5cf434d4-d865-4281-b45c-8595b517e7a6/object_description.json`

## Observed JSON Field Hints

- `object_name`: 100
- `start`: 100
- `end`: 100
- `target`: 100
- `target.position`: 100
- `target.rotation`: 100
- `[].object_name`: 5
- `[].object_desc`: 5
- `Carla_Town01`: 1
- `Carla_Town02`: 1
- `Carla_Town03`: 1
- `Carla_Town04`: 1
- `Carla_Town05`: 1
- `Carla_Town06`: 1
- `Carla_Town07`: 1
- `Carla_Town10HD`: 1
- `Carla_Town15`: 1
- `ModernCityMap`: 1
- `NewYorkCity`: 1
- `ModularPark`: 1
- `NYCEnvironmentMegapa`: 1
- `TropicalIsland`: 1

## Keyword-Based Field Candidates

### instruction
- `Model/LLaMA-UAV/tools/generate_merged_json.py`
- `Model/LLaMA-UAV/tools/preprocess_image2tensor.py`
- `README.md`
- `scripts/dagger_NYC.sh`
- `scripts/eval.sh`
- `src/common/param.py`
- `src/model_wrapper/travel_llm.py`
- `src/model_wrapper/utils/GroundingDINO/environment.yaml`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/fuse_modules.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/transformer_vanilla.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/util/slconfig.py`
- `src/model_wrapper/utils/GroundingDINO/setup.py`
- `src/model_wrapper/utils/travel_util.py`
- `src/vlnce_src/closeloop_util.py`
- `src/vlnce_src/dino_monitor_online.py`
- `src/vlnce_src/env_uav.py`

### image
- `data/raw/TravelUAV/Carla_Town07/086846df-ca48-4690-80f2-ceae362c0b0d/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/14854721-e5a0-407a-b511-19467ee300dd/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/3bf37b50-355e-4c64-a8da-7ab77fc27324/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/3c1e25f6-cde2-4d3b-9612-54a6fa53844b/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/43ec1c75-b445-465f-bd0d-f2484710d68d/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/7d0c5808-0154-4d18-9531-602a4719b5bf/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/88141905-cbba-4eb9-a4d2-9d0d39077e43/object_description.json`
- `Model/LLaMA-UAV/tools/generate_merged_json.py`
- `Model/LLaMA-UAV/tools/preprocess_image2tensor.py`
- `README.md`
- `data/traj_train/val_8s_8k.json`
- `scripts/dagger_NYC.sh`
- `scripts/eval.sh`
- `src/common/param.py`
- `src/model_wrapper/travel_llm.py`
- `src/model_wrapper/utils/GroundingDINO/README.md`
- `src/model_wrapper/utils/GroundingDINO/environment.yaml`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/config/GroundingDINO_SwinB_cfg.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/datasets/cocogrounding_eval.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/datasets/transforms.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/backbone/backbone.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/backbone/position_encoding.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/backbone/swin_transformer.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/fuse_modules.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/groundingdino.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/ms_deform_attn.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/transformer.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/util/inference.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/util/logger.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/util/utils.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/util/visualizer.py`
- `src/model_wrapper/utils/travel_util.py`
- `src/vlnce_src/assist.py`
- `src/vlnce_src/closeloop_util.py`
- `src/vlnce_src/dino_monitor_online.py`
- `src/vlnce_src/env_uav.py`

### trajectory
- `data/raw/TravelUAV/Carla_Town07/004d6e1f-248f-4804-881d-635f5a05e8bb/mark.json`
- `data/raw/TravelUAV/Carla_Town07/07dc3754-4b63-4d67-a28e-d007e71f45c4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/07dc3754-4b63-4d67-a28e-d007e71f45c4/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/07df84e1-6da7-427a-88ba-603fa1aa24b2/mark.json`
- `data/raw/TravelUAV/Carla_Town07/086846df-ca48-4690-80f2-ceae362c0b0d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0c625b2c-fa65-40d8-a727-547dc7dcd440/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0c625b2c-fa65-40d8-a727-547dc7dcd440/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/0cc61a3a-f9d0-43f1-ace7-74fc96e040ac/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0cc61a3a-f9d0-43f1-ace7-74fc96e040ac/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/0cf8413d-e441-459f-841a-a33cb12563fe/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0cf8413d-e441-459f-841a-a33cb12563fe/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/14854721-e5a0-407a-b511-19467ee300dd/mark.json`
- `data/raw/TravelUAV/Carla_Town07/14854721-e5a0-407a-b511-19467ee300dd/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/14cac25a-9462-4214-bdd9-30537c476d74/mark.json`
- `data/raw/TravelUAV/Carla_Town07/14cac25a-9462-4214-bdd9-30537c476d74/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/15515bbb-96e2-4fa5-b172-8697bd81c30d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/15515bbb-96e2-4fa5-b172-8697bd81c30d/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/193d0c46-d133-4e23-a158-2802e206094d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/196017ac-5458-4a44-9652-adb2ddd01013/mark.json`
- `data/raw/TravelUAV/Carla_Town07/19ec1266-c1c6-4257-ac0c-eab41102a6a4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/19ec1266-c1c6-4257-ac0c-eab41102a6a4/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/1db41498-6189-425f-b0dd-cc2c388df9b5/mark.json`
- `data/raw/TravelUAV/Carla_Town07/1df027d2-699a-4c3d-a84c-3e05c565b5e4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/1e6dc9de-c86b-4895-9c58-2ba338a88ae4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21773f09-3210-4581-971e-639e15ad3afb/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21aaec2b-cde9-4ed3-9975-2a45dc2c3217/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21ca74bf-69ed-4f9e-a66b-aeb6aa9ee8b1/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21ca74bf-69ed-4f9e-a66b-aeb6aa9ee8b1/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/27c2f769-8913-47a4-b780-a1507b30e934/mark.json`
- `data/raw/TravelUAV/Carla_Town07/295fe8e7-1167-4724-8c95-e21b80c998c3/mark.json`
- `data/raw/TravelUAV/Carla_Town07/295fe8e7-1167-4724-8c95-e21b80c998c3/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/2977001c-4194-4927-986e-731b0ff80925/mark.json`
- `data/raw/TravelUAV/Carla_Town07/2977001c-4194-4927-986e-731b0ff80925/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/2dcf6969-7fd3-4553-8dde-39bf77b6424f/mark.json`
- `data/raw/TravelUAV/Carla_Town07/2dcf6969-7fd3-4553-8dde-39bf77b6424f/object_description.json`
- `data/raw/TravelUAV/Carla_Town07/2f3b431e-5136-4d3d-8f2c-0c0702b4386d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/30626553-5aa5-418d-92bf-70cf68a6633c/mark.json`
- `data/raw/TravelUAV/Carla_Town07/34dc49cc-9570-44a4-a36c-b9259c7977e2/mark.json`
- `data/raw/TravelUAV/Carla_Town07/354aad0f-c06a-479d-8c49-257c34cd19b1/mark.json`
- `data/raw/TravelUAV/Carla_Town07/3bf37b50-355e-4c64-a8da-7ab77fc27324/mark.json`

### yaw
- `data/raw/TravelUAV/Carla_Town07/004d6e1f-248f-4804-881d-635f5a05e8bb/mark.json`
- `data/raw/TravelUAV/Carla_Town07/07dc3754-4b63-4d67-a28e-d007e71f45c4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/07df84e1-6da7-427a-88ba-603fa1aa24b2/mark.json`
- `data/raw/TravelUAV/Carla_Town07/086846df-ca48-4690-80f2-ceae362c0b0d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0c625b2c-fa65-40d8-a727-547dc7dcd440/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0cc61a3a-f9d0-43f1-ace7-74fc96e040ac/mark.json`
- `data/raw/TravelUAV/Carla_Town07/0cf8413d-e441-459f-841a-a33cb12563fe/mark.json`
- `data/raw/TravelUAV/Carla_Town07/14854721-e5a0-407a-b511-19467ee300dd/mark.json`
- `data/raw/TravelUAV/Carla_Town07/14cac25a-9462-4214-bdd9-30537c476d74/mark.json`
- `data/raw/TravelUAV/Carla_Town07/15515bbb-96e2-4fa5-b172-8697bd81c30d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/193d0c46-d133-4e23-a158-2802e206094d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/196017ac-5458-4a44-9652-adb2ddd01013/mark.json`
- `data/raw/TravelUAV/Carla_Town07/19ec1266-c1c6-4257-ac0c-eab41102a6a4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/1db41498-6189-425f-b0dd-cc2c388df9b5/mark.json`
- `data/raw/TravelUAV/Carla_Town07/1df027d2-699a-4c3d-a84c-3e05c565b5e4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/1e6dc9de-c86b-4895-9c58-2ba338a88ae4/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21773f09-3210-4581-971e-639e15ad3afb/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21aaec2b-cde9-4ed3-9975-2a45dc2c3217/mark.json`
- `data/raw/TravelUAV/Carla_Town07/21ca74bf-69ed-4f9e-a66b-aeb6aa9ee8b1/mark.json`
- `data/raw/TravelUAV/Carla_Town07/27c2f769-8913-47a4-b780-a1507b30e934/mark.json`
- `data/raw/TravelUAV/Carla_Town07/295fe8e7-1167-4724-8c95-e21b80c998c3/mark.json`
- `data/raw/TravelUAV/Carla_Town07/2977001c-4194-4927-986e-731b0ff80925/mark.json`
- `data/raw/TravelUAV/Carla_Town07/2dcf6969-7fd3-4553-8dde-39bf77b6424f/mark.json`
- `data/raw/TravelUAV/Carla_Town07/2f3b431e-5136-4d3d-8f2c-0c0702b4386d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/30626553-5aa5-418d-92bf-70cf68a6633c/mark.json`
- `data/raw/TravelUAV/Carla_Town07/34dc49cc-9570-44a4-a36c-b9259c7977e2/mark.json`
- `data/raw/TravelUAV/Carla_Town07/354aad0f-c06a-479d-8c49-257c34cd19b1/mark.json`
- `data/raw/TravelUAV/Carla_Town07/3bf37b50-355e-4c64-a8da-7ab77fc27324/mark.json`
- `data/raw/TravelUAV/Carla_Town07/3c1e25f6-cde2-4d3b-9612-54a6fa53844b/mark.json`
- `data/raw/TravelUAV/Carla_Town07/4297394b-bd20-48f6-9006-6ecb184ad467/mark.json`
- `data/raw/TravelUAV/Carla_Town07/43ec1c75-b445-465f-bd0d-f2484710d68d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/48ab318b-1591-4009-b0f1-30100dc7e6f1/mark.json`
- `data/raw/TravelUAV/Carla_Town07/48e21e14-d6aa-443e-96f3-72361e006fe9/mark.json`
- `data/raw/TravelUAV/Carla_Town07/4dde8a17-35b0-44d9-8d03-97cfc46e6e82/mark.json`
- `data/raw/TravelUAV/Carla_Town07/4e0c4f7e-6c03-43db-87ee-d416e2f46540/mark.json`
- `data/raw/TravelUAV/Carla_Town07/5388513c-a78f-4d66-80b2-b9eab0ea582d/mark.json`
- `data/raw/TravelUAV/Carla_Town07/5412543d-cd59-4df6-b3c9-1d262c2b6f91/mark.json`
- `data/raw/TravelUAV/Carla_Town07/594c4b93-bf90-49d5-b13f-f86670970fce/mark.json`
- `data/raw/TravelUAV/Carla_Town07/597db4bf-3d4d-43a7-b0ea-a2be4f983e35/mark.json`
- `data/raw/TravelUAV/Carla_Town07/5cf434d4-d865-4281-b45c-8595b517e7a6/mark.json`

### action
- `data/traj_train/val_8s_8k.json`
- `scripts/dagger_NYC.sh`
- `scripts/eval.sh`
- `src/common/param.py`
- `src/model_wrapper/travel_llm.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/util/slconfig.py`
- `src/model_wrapper/utils/travel_util.py`
- `src/vlnce_src/closeloop_util.py`
- `src/vlnce_src/dagger.py`
- `src/vlnce_src/eval.py`

## Current Understanding
- TravelUAV 仓库 README 指向 Hugging Face 数据集和环境；本地 clone 里部分训练 JSON 是 Git LFS pointer，未下载大数据。
- `data/uav_dataset/*valset*.json` 的样例条目包含 `json` 和 `frame`，其中 `json` 指向 `MapName/EpisodeId/merged_data.json`。
- `Model/LLaMA-UAV/tools/generate_merged_json.py` 会从 `dataset_raw/<map>/<episode>/log/*.json`、相机目录和 `object_description.json` 生成 `merged_data.json`。
- 生成的 `merged_data.json` 关键字段包括 `trajectory`、`trajectory_raw`、`trajectory_raw_detailed`、`image_feature_path`、`index`、`length`、`conversations`。
- 本次下载的地图子集为 raw episode 结构：`<map>/<episode>/log/*.json`、`frontcamera/*.png`、`object_description.json`、`mark.json`；未发现预生成 `merged_data.json`。
- `trajectory_raw*` 中的 pose 预计使用 `position` 和四元数 `orientation`；可转换为本项目 `state=[x,y,z,yaw]`。
- 当前未确认原始文件中存在直接的连续动作字段；默认由相邻轨迹点计算 `action=[vx,vy,vz,yaw_rate]`。

## TravelUAV -> OpenVLA-OFT JSONL Mapping Suggestion
- `dataset`: 固定为 `TravelUAV`。
- `episode_id`: 从 `merged_data.json` 父目录名或原始 JSON 中 episode 字段获得。
- `step_id`: 使用帧序号或转换后的连续 step index。
- `image`: 优先记录 `frontcamera/<frame>.png`；如后续需要双视角，可扩展为 front/down 两路。
- `instruction`: 使用 `conversations[0].value`，去掉可选 `<image>` 前缀后作为自然语言指令。
- `state`: 从 `trajectory_raw_detailed` 或 `trajectory_raw` 的 `position` + `orientation` 得到 `[x,y,z,yaw]`。
- `action`: 若没有直接 action，则由相邻 state 和 `dt` 计算。
- `action_chunk`: 从当前 step 起取未来 `chunk_size` 个 action，不足时用最后一个 action 填充。
