# TravelUAV Data Notes

## Inspection Scope
- TravelUAV root: `external/TravelUAV`
- Dataset root: `data/raw/TravelUAV/Carla_Town10HD`
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

- `data/raw/TravelUAV/Carla_Town10HD/0011a476-568c-4ae3-9009-1ccb15d68441/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0011a476-568c-4ae3-9009-1ccb15d68441/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/02d3781c-1062-4661-87a4-5759b4a12fb0/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/02d3781c-1062-4661-87a4-5759b4a12fb0/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/0464209b-3cae-4048-b2b1-29f2788e4ace/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0464209b-3cae-4048-b2b1-29f2788e4ace/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/06aee7ca-8edf-4f83-82da-dd5ca6e4f7a5/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/06aee7ca-8edf-4f83-82da-dd5ca6e4f7a5/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/086a1731-7fe2-4bfe-b675-a21a9addcd08/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/086a1731-7fe2-4bfe-b675-a21a9addcd08/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/0a88fa68-eff6-4ccd-88b3-f0ef2b8eb31e/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0a88fa68-eff6-4ccd-88b3-f0ef2b8eb31e/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/0c2fe1f6-ffef-4cda-b202-0ded35d47cd8/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0c2fe1f6-ffef-4cda-b202-0ded35d47cd8/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/0e248484-4a3d-4a55-b521-05df4818b8a0/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0e248484-4a3d-4a55-b521-05df4818b8a0/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/10c91db0-0991-4fe9-8cc1-cef6edb8d779/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/10c91db0-0991-4fe9-8cc1-cef6edb8d779/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/12cbc4dd-d985-40f7-9244-c38960cd83db/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/12cbc4dd-d985-40f7-9244-c38960cd83db/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/143dec49-5140-4d83-8a31-95172475e0f8/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/143dec49-5140-4d83-8a31-95172475e0f8/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/19f20d6c-5504-4236-9152-192345aba576/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/19f20d6c-5504-4236-9152-192345aba576/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/1c222dc6-59f4-45c6-b3a8-564b63327b5d/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/1c222dc6-59f4-45c6-b3a8-564b63327b5d/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/1e75771d-fddd-4af3-8f26-88a339963ab9/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/1e75771d-fddd-4af3-8f26-88a339963ab9/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/21364674-ad00-467e-94c3-bb2bbc32ec2e/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/21364674-ad00-467e-94c3-bb2bbc32ec2e/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/23d225e5-5243-4690-8603-7742efd286b4/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/23d225e5-5243-4690-8603-7742efd286b4/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/265deabf-279c-4e14-a841-fe0d43cfaf0b/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/265deabf-279c-4e14-a841-fe0d43cfaf0b/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/290d0260-8848-4b18-addb-ec1c45e72a14/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/290d0260-8848-4b18-addb-ec1c45e72a14/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/2c08f0e9-c0b7-40ae-a825-d8ed3250fc33/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/2c08f0e9-c0b7-40ae-a825-d8ed3250fc33/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/2fea7ffa-b78a-41e7-8748-b01b61f17046/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/2fea7ffa-b78a-41e7-8748-b01b61f17046/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/31e0de80-92c4-47d5-9bd0-1c59d142b7f6/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/31e0de80-92c4-47d5-9bd0-1c59d142b7f6/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/336d6250-3c6a-4f42-8b97-22b7faf081ff/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/336d6250-3c6a-4f42-8b97-22b7faf081ff/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/35de7218-d26c-488c-9d8b-9c406ec65efc/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/35de7218-d26c-488c-9d8b-9c406ec65efc/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/38ad4ae4-3ac8-47d2-9dcc-d60de5b5a7d6/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/38ad4ae4-3ac8-47d2-9dcc-d60de5b5a7d6/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/3b109e12-07e2-4f4f-8d45-6d85030edc0a/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/3b109e12-07e2-4f4f-8d45-6d85030edc0a/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/3db0680a-bec3-4f2e-a41a-aa51cf4cde0c/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/3db0680a-bec3-4f2e-a41a-aa51cf4cde0c/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/3f6f4cf0-54f1-4402-bdf0-ec6a0acdb05d/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/3f6f4cf0-54f1-4402-bdf0-ec6a0acdb05d/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/41caa078-f16d-4765-a2b5-a313e0dbd1f4/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/41caa078-f16d-4765-a2b5-a313e0dbd1f4/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/44964865-5475-43ea-a239-c1117e19034b/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/44964865-5475-43ea-a239-c1117e19034b/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/46e78489-f917-462b-a640-3f999049b295/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/46e78489-f917-462b-a640-3f999049b295/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/4a08c7c2-5919-4380-b1b6-a3c569e82307/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/4a08c7c2-5919-4380-b1b6-a3c569e82307/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/4c148035-aed1-4d51-9777-9b143c2285fe/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/4c148035-aed1-4d51-9777-9b143c2285fe/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/4e6f6a52-c662-4f4b-b886-e0e93c07cbda/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/4e6f6a52-c662-4f4b-b886-e0e93c07cbda/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/5055e75b-ee07-4493-8544-05bbb61a65c3/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/5055e75b-ee07-4493-8544-05bbb61a65c3/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/5358b507-0401-4275-86c4-008e2a899c39/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/5358b507-0401-4275-86c4-008e2a899c39/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/54da8de9-a67e-4007-a21c-40cba7bc45e1/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/54da8de9-a67e-4007-a21c-40cba7bc45e1/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/56fcf0f1-8626-4172-8960-f1aebc94d16b/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/56fcf0f1-8626-4172-8960-f1aebc94d16b/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/585be061-fac3-4d20-835f-31e6ef26c8f3/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/585be061-fac3-4d20-835f-31e6ef26c8f3/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/5b0cbd61-0ab7-4765-a873-1d12e63f6b2d/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/5b0cbd61-0ab7-4765-a873-1d12e63f6b2d/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/5d40e520-3a10-4428-903c-7625a12c4212/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/5d40e520-3a10-4428-903c-7625a12c4212/object_description.json`

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
- `data/raw/TravelUAV/Carla_Town10HD/0e248484-4a3d-4a55-b521-05df4818b8a0/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/23d225e5-5243-4690-8603-7742efd286b4/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/2c08f0e9-c0b7-40ae-a825-d8ed3250fc33/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/35de7218-d26c-488c-9d8b-9c406ec65efc/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/3f6f4cf0-54f1-4402-bdf0-ec6a0acdb05d/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/41caa078-f16d-4765-a2b5-a313e0dbd1f4/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/46e78489-f917-462b-a640-3f999049b295/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/7710e55a-cad0-4e7e-a09d-125885cddb52/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/b6e135b1-2076-4a19-98a5-3a659fa7bb59/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/bd5ca246-0315-41f5-a463-3a3333500cf0/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/c7b249c9-32cc-4551-9d04-6987160f333f/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/cc56cca8-080b-4232-9218-079a3aa1096c/object_description.json`
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

### trajectory
- `data/raw/TravelUAV/Carla_Town10HD/0011a476-568c-4ae3-9009-1ccb15d68441/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/02d3781c-1062-4661-87a4-5759b4a12fb0/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0464209b-3cae-4048-b2b1-29f2788e4ace/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/06aee7ca-8edf-4f83-82da-dd5ca6e4f7a5/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/086a1731-7fe2-4bfe-b675-a21a9addcd08/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/086a1731-7fe2-4bfe-b675-a21a9addcd08/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/0a88fa68-eff6-4ccd-88b3-f0ef2b8eb31e/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0c2fe1f6-ffef-4cda-b202-0ded35d47cd8/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0e248484-4a3d-4a55-b521-05df4818b8a0/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/10c91db0-0991-4fe9-8cc1-cef6edb8d779/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/12cbc4dd-d985-40f7-9244-c38960cd83db/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/143dec49-5140-4d83-8a31-95172475e0f8/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/19f20d6c-5504-4236-9152-192345aba576/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/1c222dc6-59f4-45c6-b3a8-564b63327b5d/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/1e75771d-fddd-4af3-8f26-88a339963ab9/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/1e75771d-fddd-4af3-8f26-88a339963ab9/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/21364674-ad00-467e-94c3-bb2bbc32ec2e/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/23d225e5-5243-4690-8603-7742efd286b4/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/265deabf-279c-4e14-a841-fe0d43cfaf0b/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/290d0260-8848-4b18-addb-ec1c45e72a14/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/290d0260-8848-4b18-addb-ec1c45e72a14/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/2c08f0e9-c0b7-40ae-a825-d8ed3250fc33/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/2fea7ffa-b78a-41e7-8748-b01b61f17046/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/31e0de80-92c4-47d5-9bd0-1c59d142b7f6/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/336d6250-3c6a-4f42-8b97-22b7faf081ff/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/35de7218-d26c-488c-9d8b-9c406ec65efc/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/35de7218-d26c-488c-9d8b-9c406ec65efc/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/38ad4ae4-3ac8-47d2-9dcc-d60de5b5a7d6/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/3b109e12-07e2-4f4f-8d45-6d85030edc0a/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/3db0680a-bec3-4f2e-a41a-aa51cf4cde0c/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/3f6f4cf0-54f1-4402-bdf0-ec6a0acdb05d/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/41caa078-f16d-4765-a2b5-a313e0dbd1f4/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/44964865-5475-43ea-a239-c1117e19034b/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/44964865-5475-43ea-a239-c1117e19034b/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/46e78489-f917-462b-a640-3f999049b295/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/4a08c7c2-5919-4380-b1b6-a3c569e82307/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/4c148035-aed1-4d51-9777-9b143c2285fe/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/4e6f6a52-c662-4f4b-b886-e0e93c07cbda/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/5055e75b-ee07-4493-8544-05bbb61a65c3/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/5055e75b-ee07-4493-8544-05bbb61a65c3/object_description.json`

### yaw
- `data/raw/TravelUAV/Carla_Town10HD/0011a476-568c-4ae3-9009-1ccb15d68441/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/02d3781c-1062-4661-87a4-5759b4a12fb0/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0464209b-3cae-4048-b2b1-29f2788e4ace/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0464209b-3cae-4048-b2b1-29f2788e4ace/object_description.json`
- `data/raw/TravelUAV/Carla_Town10HD/06aee7ca-8edf-4f83-82da-dd5ca6e4f7a5/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/086a1731-7fe2-4bfe-b675-a21a9addcd08/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0a88fa68-eff6-4ccd-88b3-f0ef2b8eb31e/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0c2fe1f6-ffef-4cda-b202-0ded35d47cd8/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/0e248484-4a3d-4a55-b521-05df4818b8a0/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/10c91db0-0991-4fe9-8cc1-cef6edb8d779/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/12cbc4dd-d985-40f7-9244-c38960cd83db/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/143dec49-5140-4d83-8a31-95172475e0f8/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/19f20d6c-5504-4236-9152-192345aba576/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/1c222dc6-59f4-45c6-b3a8-564b63327b5d/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/1e75771d-fddd-4af3-8f26-88a339963ab9/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/21364674-ad00-467e-94c3-bb2bbc32ec2e/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/23d225e5-5243-4690-8603-7742efd286b4/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/265deabf-279c-4e14-a841-fe0d43cfaf0b/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/290d0260-8848-4b18-addb-ec1c45e72a14/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/2c08f0e9-c0b7-40ae-a825-d8ed3250fc33/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/2fea7ffa-b78a-41e7-8748-b01b61f17046/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/31e0de80-92c4-47d5-9bd0-1c59d142b7f6/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/336d6250-3c6a-4f42-8b97-22b7faf081ff/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/35de7218-d26c-488c-9d8b-9c406ec65efc/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/38ad4ae4-3ac8-47d2-9dcc-d60de5b5a7d6/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/3b109e12-07e2-4f4f-8d45-6d85030edc0a/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/3db0680a-bec3-4f2e-a41a-aa51cf4cde0c/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/3f6f4cf0-54f1-4402-bdf0-ec6a0acdb05d/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/41caa078-f16d-4765-a2b5-a313e0dbd1f4/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/44964865-5475-43ea-a239-c1117e19034b/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/46e78489-f917-462b-a640-3f999049b295/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/4a08c7c2-5919-4380-b1b6-a3c569e82307/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/4c148035-aed1-4d51-9777-9b143c2285fe/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/4e6f6a52-c662-4f4b-b886-e0e93c07cbda/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/5055e75b-ee07-4493-8544-05bbb61a65c3/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/5358b507-0401-4275-86c4-008e2a899c39/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/54da8de9-a67e-4007-a21c-40cba7bc45e1/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/56fcf0f1-8626-4172-8960-f1aebc94d16b/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/585be061-fac3-4d20-835f-31e6ef26c8f3/mark.json`
- `data/raw/TravelUAV/Carla_Town10HD/5b0cbd61-0ab7-4765-a873-1d12e63f6b2d/mark.json`

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
