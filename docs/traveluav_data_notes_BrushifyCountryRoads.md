# TravelUAV Data Notes

## Inspection Scope
- TravelUAV root: `external/TravelUAV`
- Dataset root: `data/raw/TravelUAV/BrushifyCountryRoads`
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

- `data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/00cae84c-2e1b-4b7b-95e7-7d9505670795/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/00cae84c-2e1b-4b7b-95e7-7d9505670795/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/00dcf5f0-43cb-4cd6-8c84-655c44ceae67/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/00dcf5f0-43cb-4cd6-8c84-655c44ceae67/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0139e7ca-1fd9-44f3-bed6-dc9a85291228/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0139e7ca-1fd9-44f3-bed6-dc9a85291228/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/01706a3c-66a8-477f-947a-d62e0e4c963f/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/01706a3c-66a8-477f-947a-d62e0e4c963f/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0182f2e3-5e31-4f92-b1a0-768005dd9e58/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0182f2e3-5e31-4f92-b1a0-768005dd9e58/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/022c92db-7327-4814-b9e7-01eb76b84d19/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/022c92db-7327-4814-b9e7-01eb76b84d19/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/02406dbc-8497-48a8-b00b-040b4c8c277a/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/02406dbc-8497-48a8-b00b-040b4c8c277a/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/02f80d28-cff4-4111-9e6c-175ade4eebec/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/02f80d28-cff4-4111-9e6c-175ade4eebec/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03157986-8439-4b57-8f80-caafef157067/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03157986-8439-4b57-8f80-caafef157067/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0357636d-9a0f-454a-8292-2c87a8cc9724/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0357636d-9a0f-454a-8292-2c87a8cc9724/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/035d0e6a-a876-462f-909d-911af8fd1425/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/035d0e6a-a876-462f-909d-911af8fd1425/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03d39699-4b00-4c04-8253-de31e99e3763/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03d39699-4b00-4c04-8253-de31e99e3763/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03e2d3d4-5460-4562-98dc-50091d41063b/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03e2d3d4-5460-4562-98dc-50091d41063b/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0487110b-3e78-4a96-ba43-c5c75919603c/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0487110b-3e78-4a96-ba43-c5c75919603c/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/04b11c1d-33a7-4a17-a1a3-57c7722f70a9/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/04b11c1d-33a7-4a17-a1a3-57c7722f70a9/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05252346-7b46-4353-80c8-f9f53d17d95b/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05252346-7b46-4353-80c8-f9f53d17d95b/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05c65b80-360b-4935-9401-adcfe2acf9c5/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05c65b80-360b-4935-9401-adcfe2acf9c5/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05d48d5c-8a2f-4457-b6a3-691edc4ddedc/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05d48d5c-8a2f-4457-b6a3-691edc4ddedc/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05f064f0-f960-4b9a-9f62-698e21de0c56/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05f064f0-f960-4b9a-9f62-698e21de0c56/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/065d7d28-5c33-4afc-88d2-6b9af37c8123/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/065d7d28-5c33-4afc-88d2-6b9af37c8123/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06af1b22-6371-4b79-9503-fd8470a17537/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06af1b22-6371-4b79-9503-fd8470a17537/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06c746f9-fde1-4d08-b3d1-1494a1e57c6e/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06c746f9-fde1-4d08-b3d1-1494a1e57c6e/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06da7acb-ce01-426c-a016-9b68cfb26c8b/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06da7acb-ce01-426c-a016-9b68cfb26c8b/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/07047924-ab14-4fd7-87d4-df9aaaac8f78/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/07047924-ab14-4fd7-87d4-df9aaaac8f78/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/074af58c-4e8f-4e7a-a2df-5938077ee0a9/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/074af58c-4e8f-4e7a-a2df-5938077ee0a9/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/081d005a-2551-4aa1-9960-f41dc187a3b6/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/081d005a-2551-4aa1-9960-f41dc187a3b6/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/082e6b3b-7775-45a8-97fa-9aff060b9483/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/082e6b3b-7775-45a8-97fa-9aff060b9483/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/085a5a9f-5c40-4d24-a626-d6a6d0c548a1/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/085a5a9f-5c40-4d24-a626-d6a6d0c548a1/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/08d6b78d-5078-43d7-a549-6c4d022ffac3/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/08d6b78d-5078-43d7-a549-6c4d022ffac3/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0902a4b0-090f-43f2-aa8c-922cfc4c7606/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0902a4b0-090f-43f2-aa8c-922cfc4c7606/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/09871935-c4b9-48ff-a7fc-3dff4868f8d2/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/09871935-c4b9-48ff-a7fc-3dff4868f8d2/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/09f771e6-c8a3-4f42-b82d-f697f157fc03/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/09f771e6-c8a3-4f42-b82d-f697f157fc03/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0ba569e3-4d17-443d-8f68-af89dcb50393/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0ba569e3-4d17-443d-8f68-af89dcb50393/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0bd68d31-6b77-48f5-bf44-259487dbd9f7/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0bd68d31-6b77-48f5-bf44-259487dbd9f7/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0cfa0a24-6f1d-4390-9c3c-4ce4d7574749/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0cfa0a24-6f1d-4390-9c3c-4ce4d7574749/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0e8a735f-1aa1-4055-b8c1-a503ba8862f3/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0e8a735f-1aa1-4055-b8c1-a503ba8862f3/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0ec894b7-2c14-41e0-ba45-5331ba7bebe1/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0ec894b7-2c14-41e0-ba45-5331ba7bebe1/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0f573f5c-e41a-4c4c-9412-e84c543b4c2e/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0f573f5c-e41a-4c4c-9412-e84c543b4c2e/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0f97e354-e014-47ac-800b-6b908d33a611/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0f97e354-e014-47ac-800b-6b908d33a611/object_description.json`

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
- `data/raw/TravelUAV/BrushifyCountryRoads/02406dbc-8497-48a8-b00b-040b4c8c277a/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/035d0e6a-a876-462f-909d-911af8fd1425/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05252346-7b46-4353-80c8-f9f53d17d95b/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/065d7d28-5c33-4afc-88d2-6b9af37c8123/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/074af58c-4e8f-4e7a-a2df-5938077ee0a9/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0f97e354-e014-47ac-800b-6b908d33a611/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/10ac88bc-414a-4570-aefa-1540ae59d443/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/14aaca6c-e100-429a-a7ec-8629d587bbf0/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/15bd6aca-71a6-4e54-82cb-2c78a4f645b2/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/16644759-3550-4ecb-9e2d-88b9412e722b/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/168c620d-8bbb-47ce-9a72-d14446a9db9d/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/17541d2f-6775-4fff-a004-ed5558a0110c/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/17f598a7-34ab-4fae-84e4-a83be14494e3/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/1c94a930-8269-4c58-9922-43998f1490f2/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/1d8e281f-7a32-47f5-a949-d0efabd78765/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/20bb7f67-55d4-4b5a-b7e4-9057a47bb58f/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/228ec508-719f-4b5a-a127-ed0b7dece891/object_description.json`
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

### trajectory
- `data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/00cae84c-2e1b-4b7b-95e7-7d9505670795/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/00cae84c-2e1b-4b7b-95e7-7d9505670795/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/00dcf5f0-43cb-4cd6-8c84-655c44ceae67/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0139e7ca-1fd9-44f3-bed6-dc9a85291228/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0139e7ca-1fd9-44f3-bed6-dc9a85291228/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/01706a3c-66a8-477f-947a-d62e0e4c963f/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0182f2e3-5e31-4f92-b1a0-768005dd9e58/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0182f2e3-5e31-4f92-b1a0-768005dd9e58/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/022c92db-7327-4814-b9e7-01eb76b84d19/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/02406dbc-8497-48a8-b00b-040b4c8c277a/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/02f80d28-cff4-4111-9e6c-175ade4eebec/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/02f80d28-cff4-4111-9e6c-175ade4eebec/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03157986-8439-4b57-8f80-caafef157067/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0357636d-9a0f-454a-8292-2c87a8cc9724/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0357636d-9a0f-454a-8292-2c87a8cc9724/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/035d0e6a-a876-462f-909d-911af8fd1425/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03d39699-4b00-4c04-8253-de31e99e3763/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03e2d3d4-5460-4562-98dc-50091d41063b/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0487110b-3e78-4a96-ba43-c5c75919603c/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/04b11c1d-33a7-4a17-a1a3-57c7722f70a9/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05252346-7b46-4353-80c8-f9f53d17d95b/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05c65b80-360b-4935-9401-adcfe2acf9c5/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05c65b80-360b-4935-9401-adcfe2acf9c5/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05d48d5c-8a2f-4457-b6a3-691edc4ddedc/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05d48d5c-8a2f-4457-b6a3-691edc4ddedc/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05f064f0-f960-4b9a-9f62-698e21de0c56/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/065d7d28-5c33-4afc-88d2-6b9af37c8123/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06af1b22-6371-4b79-9503-fd8470a17537/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06af1b22-6371-4b79-9503-fd8470a17537/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06c746f9-fde1-4d08-b3d1-1494a1e57c6e/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06c746f9-fde1-4d08-b3d1-1494a1e57c6e/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06da7acb-ce01-426c-a016-9b68cfb26c8b/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/07047924-ab14-4fd7-87d4-df9aaaac8f78/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/07047924-ab14-4fd7-87d4-df9aaaac8f78/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/074af58c-4e8f-4e7a-a2df-5938077ee0a9/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/081d005a-2551-4aa1-9960-f41dc187a3b6/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/081d005a-2551-4aa1-9960-f41dc187a3b6/object_description.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/082e6b3b-7775-45a8-97fa-9aff060b9483/mark.json`

### yaw
- `data/raw/TravelUAV/BrushifyCountryRoads/0008c004-9c02-40d3-928f-b7228c17a39d/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/00cae84c-2e1b-4b7b-95e7-7d9505670795/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/00dcf5f0-43cb-4cd6-8c84-655c44ceae67/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0139e7ca-1fd9-44f3-bed6-dc9a85291228/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/01706a3c-66a8-477f-947a-d62e0e4c963f/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0182f2e3-5e31-4f92-b1a0-768005dd9e58/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/022c92db-7327-4814-b9e7-01eb76b84d19/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/02406dbc-8497-48a8-b00b-040b4c8c277a/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/02f80d28-cff4-4111-9e6c-175ade4eebec/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03157986-8439-4b57-8f80-caafef157067/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0357636d-9a0f-454a-8292-2c87a8cc9724/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/035d0e6a-a876-462f-909d-911af8fd1425/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03d39699-4b00-4c04-8253-de31e99e3763/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/03e2d3d4-5460-4562-98dc-50091d41063b/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0487110b-3e78-4a96-ba43-c5c75919603c/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/04b11c1d-33a7-4a17-a1a3-57c7722f70a9/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05252346-7b46-4353-80c8-f9f53d17d95b/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05c65b80-360b-4935-9401-adcfe2acf9c5/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05d48d5c-8a2f-4457-b6a3-691edc4ddedc/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/05f064f0-f960-4b9a-9f62-698e21de0c56/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/065d7d28-5c33-4afc-88d2-6b9af37c8123/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06af1b22-6371-4b79-9503-fd8470a17537/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06c746f9-fde1-4d08-b3d1-1494a1e57c6e/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/06da7acb-ce01-426c-a016-9b68cfb26c8b/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/07047924-ab14-4fd7-87d4-df9aaaac8f78/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/074af58c-4e8f-4e7a-a2df-5938077ee0a9/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/081d005a-2551-4aa1-9960-f41dc187a3b6/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/082e6b3b-7775-45a8-97fa-9aff060b9483/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/085a5a9f-5c40-4d24-a626-d6a6d0c548a1/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/08d6b78d-5078-43d7-a549-6c4d022ffac3/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0902a4b0-090f-43f2-aa8c-922cfc4c7606/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/09871935-c4b9-48ff-a7fc-3dff4868f8d2/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/09f771e6-c8a3-4f42-b82d-f697f157fc03/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0ba569e3-4d17-443d-8f68-af89dcb50393/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0bd68d31-6b77-48f5-bf44-259487dbd9f7/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0cfa0a24-6f1d-4390-9c3c-4ce4d7574749/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0e8a735f-1aa1-4055-b8c1-a503ba8862f3/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0ec894b7-2c14-41e0-ba45-5331ba7bebe1/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0f573f5c-e41a-4c4c-9412-e84c543b4c2e/mark.json`
- `data/raw/TravelUAV/BrushifyCountryRoads/0f97e354-e014-47ac-800b-6b908d33a611/mark.json`

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
