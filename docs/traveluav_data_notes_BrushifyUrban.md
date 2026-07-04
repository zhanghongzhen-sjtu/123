# TravelUAV Data Notes

## Inspection Scope
- TravelUAV root: `external/TravelUAV`
- Dataset root: `data/raw/TravelUAV/BrushifyUrban`
- Dataset root exists: `True`
- Found `merged_data.json`: `0` sample path(s)
- Found raw episode dirs with `log/` and `frontcamera/`: `20` sample path(s)

> 已发现真实 TravelUAV raw episode 目录，但当前子集未预生成 `merged_data.json`。本项目转换脚本可直接从 `log/*.json` 与 `frontcamera/*.png` 生成 debug JSONL；后续若要完全复刻 TravelUAV/AeroVLA 流程，可再运行 TravelUAV 的 `generate_merged_json.py`。

## Repository Structure Summary

### `.`
- .git/
- .git/HEAD
- .git/config
- .git/description
- .git/hooks/
- .git/index
- .git/info/
- .git/lfs/
- .git/logs/
- .git/objects/
- .git/packed-refs
- .git/refs/
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

- `data/raw/TravelUAV/BrushifyUrban/00d1fb8b-d31a-44d0-b0da-aa91b30cc0ae/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/00d1fb8b-d31a-44d0-b0da-aa91b30cc0ae/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/02872f4c-6fe4-4b46-b33f-e6ba10f391c4/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/02872f4c-6fe4-4b46-b33f-e6ba10f391c4/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/02cefa4e-dbdf-495d-a9f3-2bfeae48bf48/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/02cefa4e-dbdf-495d-a9f3-2bfeae48bf48/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/035846ed-36f5-475a-9e58-c2cecb95dfd6/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/035846ed-36f5-475a-9e58-c2cecb95dfd6/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/04d17431-598a-4de9-be6f-e86ab8e71358/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/04d17431-598a-4de9-be6f-e86ab8e71358/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0610d32f-cbb5-4c8f-9114-a3ccb387ef4f/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0610d32f-cbb5-4c8f-9114-a3ccb387ef4f/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0625c658-42e4-41bc-ba75-82a6d041633f/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0625c658-42e4-41bc-ba75-82a6d041633f/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0680771c-8898-4fbc-9b29-b61b53b9f669/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0680771c-8898-4fbc-9b29-b61b53b9f669/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/089eb120-bc01-4ab3-beb1-7166c5d10ffa/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/089eb120-bc01-4ab3-beb1-7166c5d10ffa/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/08b25df1-d3c3-4c16-b780-33b9ff2362a6/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/08b25df1-d3c3-4c16-b780-33b9ff2362a6/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/09e601a9-27ec-4032-8b7e-bad34d449f21/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/09e601a9-27ec-4032-8b7e-bad34d449f21/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0a82a7c3-9fe1-432c-85cb-ecb95e04be07/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0a82a7c3-9fe1-432c-85cb-ecb95e04be07/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0a939c40-3e91-4ab2-a480-da9a55608e95/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0a939c40-3e91-4ab2-a480-da9a55608e95/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0af50b29-e23f-4f24-afda-37000741fe3e/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0af50b29-e23f-4f24-afda-37000741fe3e/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0b0d2d26-d05f-4d01-99e7-b4e6385f52e9/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0b0d2d26-d05f-4d01-99e7-b4e6385f52e9/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0b889b37-b2cc-4a66-a58d-5edea3f5f437/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0b889b37-b2cc-4a66-a58d-5edea3f5f437/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0c17fa2d-c2ff-495f-8547-9918cf69e63f/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0c17fa2d-c2ff-495f-8547-9918cf69e63f/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0ccbea83-86f3-46b3-a1e9-0523aaf04f25/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0ccbea83-86f3-46b3-a1e9-0523aaf04f25/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0cce3ef6-b93e-4d21-b493-169353692086/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0cce3ef6-b93e-4d21-b493-169353692086/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0d1f8e11-0e2c-40e0-b920-21354dfb5b1a/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0d1f8e11-0e2c-40e0-b920-21354dfb5b1a/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0dd49ceb-760b-4cc4-b1b2-014f45504110/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0dd49ceb-760b-4cc4-b1b2-014f45504110/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0e60d10a-683a-4699-bfcf-9e00951d0d65/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0e60d10a-683a-4699-bfcf-9e00951d0d65/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0e62203b-efa1-48ee-adee-4e91a06e7833/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0e62203b-efa1-48ee-adee-4e91a06e7833/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0ee106da-beec-4b7b-8db2-f2405460b9aa/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0ee106da-beec-4b7b-8db2-f2405460b9aa/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0ef32b88-01d2-40b9-8285-9927c930b99d/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0ef32b88-01d2-40b9-8285-9927c930b99d/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0fa06a12-3d9d-4c09-ae1c-4d4ba75c5db5/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0fa06a12-3d9d-4c09-ae1c-4d4ba75c5db5/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/105a7390-28b5-480d-8fe0-e62045584ede/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/105a7390-28b5-480d-8fe0-e62045584ede/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/11187371-948b-4076-9d5a-177118889d64/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/11187371-948b-4076-9d5a-177118889d64/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/115d0ef8-bef3-451a-8a64-55050c1cc6bb/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/115d0ef8-bef3-451a-8a64-55050c1cc6bb/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/116b78e6-e25f-4068-a790-9b0bcc8f2975/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/116b78e6-e25f-4068-a790-9b0bcc8f2975/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/11f58924-b82e-4702-a52a-0901da550a69/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/11f58924-b82e-4702-a52a-0901da550a69/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/1268c1d1-30b9-4fdc-9dee-324a85bd1832/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/1268c1d1-30b9-4fdc-9dee-324a85bd1832/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/131f5923-29d4-4e18-b849-f5e014a85ea9/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/131f5923-29d4-4e18-b849-f5e014a85ea9/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/142ae2b0-b504-4ace-8e36-12d38a6a69dd/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/142ae2b0-b504-4ace-8e36-12d38a6a69dd/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/146571fb-e37d-4944-952c-c7391d382034/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/146571fb-e37d-4944-952c-c7391d382034/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/15753fc6-65c7-4c1e-825a-9cdafe9a5577/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/15753fc6-65c7-4c1e-825a-9cdafe9a5577/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/1609bb02-d5b1-4afd-9115-efd126c46c3b/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/1609bb02-d5b1-4afd-9115-efd126c46c3b/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/169af737-81cd-4b16-b75d-39f04b2b7136/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/169af737-81cd-4b16-b75d-39f04b2b7136/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/173545f7-e6b5-44ff-84d8-05c129aa77a1/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/173545f7-e6b5-44ff-84d8-05c129aa77a1/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/17db292b-73c4-4aa9-b0db-85d5d37a63ff/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/17db292b-73c4-4aa9-b0db-85d5d37a63ff/object_description.json`

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
- `data/raw/TravelUAV/BrushifyUrban/105a7390-28b5-480d-8fe0-e62045584ede/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/11f58924-b82e-4702-a52a-0901da550a69/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/173545f7-e6b5-44ff-84d8-05c129aa77a1/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/1eb8a90f-f79f-4234-a0bd-a22b4de0e1b0/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/1f5c4f9c-7d9d-4990-9c67-83fffcadc55d/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/21aed88b-bf73-4a28-9dd2-b39c780a2d57/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/21f7c792-2b7b-4e17-879c-f1aacd3ae53d/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/2421ddfe-91a9-45a8-8b0b-09835ac9f3c7/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/2a5440d5-0594-4aba-8c8b-8cf764d23a35/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/30b779b1-e2db-440c-a762-ab30e0984b69/object_description.json`
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
- `data/raw/TravelUAV/BrushifyUrban/00d1fb8b-d31a-44d0-b0da-aa91b30cc0ae/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/00d1fb8b-d31a-44d0-b0da-aa91b30cc0ae/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/02872f4c-6fe4-4b46-b33f-e6ba10f391c4/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/02872f4c-6fe4-4b46-b33f-e6ba10f391c4/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/02cefa4e-dbdf-495d-a9f3-2bfeae48bf48/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/02cefa4e-dbdf-495d-a9f3-2bfeae48bf48/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/035846ed-36f5-475a-9e58-c2cecb95dfd6/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/035846ed-36f5-475a-9e58-c2cecb95dfd6/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/04d17431-598a-4de9-be6f-e86ab8e71358/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/04d17431-598a-4de9-be6f-e86ab8e71358/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0610d32f-cbb5-4c8f-9114-a3ccb387ef4f/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0625c658-42e4-41bc-ba75-82a6d041633f/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0625c658-42e4-41bc-ba75-82a6d041633f/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0680771c-8898-4fbc-9b29-b61b53b9f669/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/089eb120-bc01-4ab3-beb1-7166c5d10ffa/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/08b25df1-d3c3-4c16-b780-33b9ff2362a6/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/09e601a9-27ec-4032-8b7e-bad34d449f21/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0a82a7c3-9fe1-432c-85cb-ecb95e04be07/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0a82a7c3-9fe1-432c-85cb-ecb95e04be07/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0a939c40-3e91-4ab2-a480-da9a55608e95/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0af50b29-e23f-4f24-afda-37000741fe3e/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0b0d2d26-d05f-4d01-99e7-b4e6385f52e9/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0b889b37-b2cc-4a66-a58d-5edea3f5f437/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0c17fa2d-c2ff-495f-8547-9918cf69e63f/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0c17fa2d-c2ff-495f-8547-9918cf69e63f/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0ccbea83-86f3-46b3-a1e9-0523aaf04f25/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0ccbea83-86f3-46b3-a1e9-0523aaf04f25/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0cce3ef6-b93e-4d21-b493-169353692086/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0cce3ef6-b93e-4d21-b493-169353692086/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0d1f8e11-0e2c-40e0-b920-21354dfb5b1a/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0d1f8e11-0e2c-40e0-b920-21354dfb5b1a/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0dd49ceb-760b-4cc4-b1b2-014f45504110/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0dd49ceb-760b-4cc4-b1b2-014f45504110/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0e60d10a-683a-4699-bfcf-9e00951d0d65/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0e60d10a-683a-4699-bfcf-9e00951d0d65/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0e62203b-efa1-48ee-adee-4e91a06e7833/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0e62203b-efa1-48ee-adee-4e91a06e7833/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0ee106da-beec-4b7b-8db2-f2405460b9aa/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0ee106da-beec-4b7b-8db2-f2405460b9aa/object_description.json`
- `data/raw/TravelUAV/BrushifyUrban/0ef32b88-01d2-40b9-8285-9927c930b99d/mark.json`

### yaw
- `data/raw/TravelUAV/BrushifyUrban/00d1fb8b-d31a-44d0-b0da-aa91b30cc0ae/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/02872f4c-6fe4-4b46-b33f-e6ba10f391c4/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/02cefa4e-dbdf-495d-a9f3-2bfeae48bf48/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/035846ed-36f5-475a-9e58-c2cecb95dfd6/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/04d17431-598a-4de9-be6f-e86ab8e71358/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0610d32f-cbb5-4c8f-9114-a3ccb387ef4f/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0625c658-42e4-41bc-ba75-82a6d041633f/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0680771c-8898-4fbc-9b29-b61b53b9f669/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/089eb120-bc01-4ab3-beb1-7166c5d10ffa/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/08b25df1-d3c3-4c16-b780-33b9ff2362a6/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/09e601a9-27ec-4032-8b7e-bad34d449f21/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0a82a7c3-9fe1-432c-85cb-ecb95e04be07/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0a939c40-3e91-4ab2-a480-da9a55608e95/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0af50b29-e23f-4f24-afda-37000741fe3e/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0b0d2d26-d05f-4d01-99e7-b4e6385f52e9/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0b889b37-b2cc-4a66-a58d-5edea3f5f437/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0c17fa2d-c2ff-495f-8547-9918cf69e63f/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0ccbea83-86f3-46b3-a1e9-0523aaf04f25/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0cce3ef6-b93e-4d21-b493-169353692086/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0d1f8e11-0e2c-40e0-b920-21354dfb5b1a/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0dd49ceb-760b-4cc4-b1b2-014f45504110/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0e60d10a-683a-4699-bfcf-9e00951d0d65/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0e62203b-efa1-48ee-adee-4e91a06e7833/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0ee106da-beec-4b7b-8db2-f2405460b9aa/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0ef32b88-01d2-40b9-8285-9927c930b99d/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/0fa06a12-3d9d-4c09-ae1c-4d4ba75c5db5/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/105a7390-28b5-480d-8fe0-e62045584ede/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/11187371-948b-4076-9d5a-177118889d64/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/115d0ef8-bef3-451a-8a64-55050c1cc6bb/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/116b78e6-e25f-4068-a790-9b0bcc8f2975/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/11f58924-b82e-4702-a52a-0901da550a69/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/1268c1d1-30b9-4fdc-9dee-324a85bd1832/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/131f5923-29d4-4e18-b849-f5e014a85ea9/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/142ae2b0-b504-4ace-8e36-12d38a6a69dd/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/146571fb-e37d-4944-952c-c7391d382034/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/15753fc6-65c7-4c1e-825a-9cdafe9a5577/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/1609bb02-d5b1-4afd-9115-efd126c46c3b/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/169af737-81cd-4b16-b75d-39f04b2b7136/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/173545f7-e6b5-44ff-84d8-05c129aa77a1/mark.json`
- `data/raw/TravelUAV/BrushifyUrban/17db292b-73c4-4aa9-b0db-85d5d37a63ff/mark.json`

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
