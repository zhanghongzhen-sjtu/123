# TravelUAV Data Notes

## Inspection Scope
- TravelUAV root: `external/TravelUAV`
- Dataset root: `data/raw/TravelUAV/Carla_Town15`
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

- `data/raw/TravelUAV/Carla_Town15/02cce8d9-2f66-423b-8b51-df576f526efb/mark.json`
- `data/raw/TravelUAV/Carla_Town15/02cce8d9-2f66-423b-8b51-df576f526efb/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/02df8d4e-c3a2-4d62-84dc-302e83ebb7b2/mark.json`
- `data/raw/TravelUAV/Carla_Town15/02df8d4e-c3a2-4d62-84dc-302e83ebb7b2/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/0643bcdd-0680-4af3-8e82-2426fdd7c27d/mark.json`
- `data/raw/TravelUAV/Carla_Town15/0643bcdd-0680-4af3-8e82-2426fdd7c27d/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/065a0114-94c2-4d72-b636-f2b55a792657/mark.json`
- `data/raw/TravelUAV/Carla_Town15/065a0114-94c2-4d72-b636-f2b55a792657/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/085f4a8d-23a4-4043-a449-c4b6b0d7b9c1/mark.json`
- `data/raw/TravelUAV/Carla_Town15/085f4a8d-23a4-4043-a449-c4b6b0d7b9c1/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/087521f0-520f-47e5-9728-e8b6704c8844/mark.json`
- `data/raw/TravelUAV/Carla_Town15/087521f0-520f-47e5-9728-e8b6704c8844/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/0d100cca-59a6-49bd-8319-4abe5c525aba/mark.json`
- `data/raw/TravelUAV/Carla_Town15/0d100cca-59a6-49bd-8319-4abe5c525aba/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/0d25c0da-2097-47bf-bc48-18a85283d48c/mark.json`
- `data/raw/TravelUAV/Carla_Town15/0d25c0da-2097-47bf-bc48-18a85283d48c/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/106f9915-4848-49e2-b40b-c66147f6148c/mark.json`
- `data/raw/TravelUAV/Carla_Town15/106f9915-4848-49e2-b40b-c66147f6148c/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/10abee26-2f28-4b30-bb83-39870ec2790e/mark.json`
- `data/raw/TravelUAV/Carla_Town15/10abee26-2f28-4b30-bb83-39870ec2790e/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/12731094-4d5b-403b-904e-652210d82145/mark.json`
- `data/raw/TravelUAV/Carla_Town15/12731094-4d5b-403b-904e-652210d82145/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/12f57f71-f4b4-4c11-b537-475b65c5a587/mark.json`
- `data/raw/TravelUAV/Carla_Town15/12f57f71-f4b4-4c11-b537-475b65c5a587/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/15c5dc77-6003-4419-8b7d-2ad2c0f3af65/mark.json`
- `data/raw/TravelUAV/Carla_Town15/15c5dc77-6003-4419-8b7d-2ad2c0f3af65/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/161e008d-2ba6-4534-8bb6-2df39251b6a1/mark.json`
- `data/raw/TravelUAV/Carla_Town15/161e008d-2ba6-4534-8bb6-2df39251b6a1/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/18905cc5-046a-471d-af79-7585f06ffeef/mark.json`
- `data/raw/TravelUAV/Carla_Town15/18905cc5-046a-471d-af79-7585f06ffeef/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/192079ac-6971-4718-ae50-a1ac7491a801/mark.json`
- `data/raw/TravelUAV/Carla_Town15/192079ac-6971-4718-ae50-a1ac7491a801/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/1ab27e5b-05d5-4070-ac93-dae9c41b0857/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1ab27e5b-05d5-4070-ac93-dae9c41b0857/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/1ae08848-9aa3-4097-9094-0d83c0a5b21a/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1ae08848-9aa3-4097-9094-0d83c0a5b21a/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/1d207916-f5e0-4358-a0eb-a604765d234f/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1d207916-f5e0-4358-a0eb-a604765d234f/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/1d325b8d-b5ae-46f1-b8fe-1005ed59b3bf/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1d325b8d-b5ae-46f1-b8fe-1005ed59b3bf/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/21568703-f138-4702-b470-35bf80ee5c17/mark.json`
- `data/raw/TravelUAV/Carla_Town15/21568703-f138-4702-b470-35bf80ee5c17/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/216c1d27-b709-48e6-9d3c-63fcd6bc3cc8/mark.json`
- `data/raw/TravelUAV/Carla_Town15/216c1d27-b709-48e6-9d3c-63fcd6bc3cc8/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/22b48e11-f1c2-4fbe-8387-d808cc86f787/mark.json`
- `data/raw/TravelUAV/Carla_Town15/22b48e11-f1c2-4fbe-8387-d808cc86f787/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/2376b75d-ed34-4a5e-9e11-2dd2f10e3817/mark.json`
- `data/raw/TravelUAV/Carla_Town15/2376b75d-ed34-4a5e-9e11-2dd2f10e3817/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/26b4648a-7439-439a-a6b7-b209b16e636b/mark.json`
- `data/raw/TravelUAV/Carla_Town15/26b4648a-7439-439a-a6b7-b209b16e636b/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/29a52216-7a99-4afe-8969-c94892920004/mark.json`
- `data/raw/TravelUAV/Carla_Town15/29a52216-7a99-4afe-8969-c94892920004/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/2a3c6950-0160-4832-bb9b-c6fa52f71684/mark.json`
- `data/raw/TravelUAV/Carla_Town15/2a3c6950-0160-4832-bb9b-c6fa52f71684/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/2dad008b-a508-4b91-b660-ec4ad7abfbe1/mark.json`
- `data/raw/TravelUAV/Carla_Town15/2dad008b-a508-4b91-b660-ec4ad7abfbe1/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/32908e28-fc6e-4298-b4c7-3c86e7044fbd/mark.json`
- `data/raw/TravelUAV/Carla_Town15/32908e28-fc6e-4298-b4c7-3c86e7044fbd/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/32c7e3c8-0511-47e2-9904-5b8dd5be2302/mark.json`
- `data/raw/TravelUAV/Carla_Town15/32c7e3c8-0511-47e2-9904-5b8dd5be2302/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/3593928d-97d4-4a4f-bf0b-3447f68f9f47/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3593928d-97d4-4a4f-bf0b-3447f68f9f47/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/35d5efeb-1459-4e7e-946f-9c89e7223712/mark.json`
- `data/raw/TravelUAV/Carla_Town15/35d5efeb-1459-4e7e-946f-9c89e7223712/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/3872d501-d115-451c-ae1c-b75f41cf5031/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3872d501-d115-451c-ae1c-b75f41cf5031/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/38b17fe1-598c-47d2-8de5-8b9df5c76ef6/mark.json`
- `data/raw/TravelUAV/Carla_Town15/38b17fe1-598c-47d2-8de5-8b9df5c76ef6/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/3b6a2169-a8e4-40db-acb2-69a4d6f855cd/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3b6a2169-a8e4-40db-acb2-69a4d6f855cd/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/3b739ae9-08aa-4db6-9084-9d2761a44796/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3b739ae9-08aa-4db6-9084-9d2761a44796/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/3ce1b883-7f87-402a-97ed-2cd355d6a50f/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3ce1b883-7f87-402a-97ed-2cd355d6a50f/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/3d2fa034-828e-4ae9-9cac-43180127581d/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3d2fa034-828e-4ae9-9cac-43180127581d/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/40eb2255-4781-44b0-9d3b-4c77882d3a2c/mark.json`
- `data/raw/TravelUAV/Carla_Town15/40eb2255-4781-44b0-9d3b-4c77882d3a2c/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/40fe156f-22d9-4eb9-8ef0-030a51735442/mark.json`
- `data/raw/TravelUAV/Carla_Town15/40fe156f-22d9-4eb9-8ef0-030a51735442/object_description.json`

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
- `data/raw/TravelUAV/Carla_Town15/02df8d4e-c3a2-4d62-84dc-302e83ebb7b2/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/18905cc5-046a-471d-af79-7585f06ffeef/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/1ab27e5b-05d5-4070-ac93-dae9c41b0857/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/4723ce4b-ee75-4225-94e2-a212a563959c/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/4a34c9d5-05ff-4ae1-b18d-4fddb191c567/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/577a4135-afb6-4e99-80b3-97cef5bb2c76/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/6706cd07-d7e2-48eb-a2d4-a15e67a184a6/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/889e45bb-bbd5-421e-8ad6-5570c12c982e/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/cdad888a-ec84-4808-9bf0-00582a3b7806/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/f5032684-a28e-4dbc-ad7b-ec146679833e/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/f80e0b95-f4f4-431d-ad1d-5bd54e23354e/object_description.json`
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

### trajectory
- `data/raw/TravelUAV/Carla_Town15/02cce8d9-2f66-423b-8b51-df576f526efb/mark.json`
- `data/raw/TravelUAV/Carla_Town15/02cce8d9-2f66-423b-8b51-df576f526efb/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/02df8d4e-c3a2-4d62-84dc-302e83ebb7b2/mark.json`
- `data/raw/TravelUAV/Carla_Town15/0643bcdd-0680-4af3-8e82-2426fdd7c27d/mark.json`
- `data/raw/TravelUAV/Carla_Town15/065a0114-94c2-4d72-b636-f2b55a792657/mark.json`
- `data/raw/TravelUAV/Carla_Town15/065a0114-94c2-4d72-b636-f2b55a792657/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/085f4a8d-23a4-4043-a449-c4b6b0d7b9c1/mark.json`
- `data/raw/TravelUAV/Carla_Town15/087521f0-520f-47e5-9728-e8b6704c8844/mark.json`
- `data/raw/TravelUAV/Carla_Town15/087521f0-520f-47e5-9728-e8b6704c8844/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/0d100cca-59a6-49bd-8319-4abe5c525aba/mark.json`
- `data/raw/TravelUAV/Carla_Town15/0d25c0da-2097-47bf-bc48-18a85283d48c/mark.json`
- `data/raw/TravelUAV/Carla_Town15/106f9915-4848-49e2-b40b-c66147f6148c/mark.json`
- `data/raw/TravelUAV/Carla_Town15/10abee26-2f28-4b30-bb83-39870ec2790e/mark.json`
- `data/raw/TravelUAV/Carla_Town15/12731094-4d5b-403b-904e-652210d82145/mark.json`
- `data/raw/TravelUAV/Carla_Town15/12731094-4d5b-403b-904e-652210d82145/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/12f57f71-f4b4-4c11-b537-475b65c5a587/mark.json`
- `data/raw/TravelUAV/Carla_Town15/12f57f71-f4b4-4c11-b537-475b65c5a587/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/15c5dc77-6003-4419-8b7d-2ad2c0f3af65/mark.json`
- `data/raw/TravelUAV/Carla_Town15/161e008d-2ba6-4534-8bb6-2df39251b6a1/mark.json`
- `data/raw/TravelUAV/Carla_Town15/18905cc5-046a-471d-af79-7585f06ffeef/mark.json`
- `data/raw/TravelUAV/Carla_Town15/18905cc5-046a-471d-af79-7585f06ffeef/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/192079ac-6971-4718-ae50-a1ac7491a801/mark.json`
- `data/raw/TravelUAV/Carla_Town15/192079ac-6971-4718-ae50-a1ac7491a801/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/1ab27e5b-05d5-4070-ac93-dae9c41b0857/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1ab27e5b-05d5-4070-ac93-dae9c41b0857/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/1ae08848-9aa3-4097-9094-0d83c0a5b21a/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1d207916-f5e0-4358-a0eb-a604765d234f/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1d325b8d-b5ae-46f1-b8fe-1005ed59b3bf/mark.json`
- `data/raw/TravelUAV/Carla_Town15/21568703-f138-4702-b470-35bf80ee5c17/mark.json`
- `data/raw/TravelUAV/Carla_Town15/216c1d27-b709-48e6-9d3c-63fcd6bc3cc8/mark.json`
- `data/raw/TravelUAV/Carla_Town15/22b48e11-f1c2-4fbe-8387-d808cc86f787/mark.json`
- `data/raw/TravelUAV/Carla_Town15/22b48e11-f1c2-4fbe-8387-d808cc86f787/object_description.json`
- `data/raw/TravelUAV/Carla_Town15/2376b75d-ed34-4a5e-9e11-2dd2f10e3817/mark.json`
- `data/raw/TravelUAV/Carla_Town15/26b4648a-7439-439a-a6b7-b209b16e636b/mark.json`
- `data/raw/TravelUAV/Carla_Town15/29a52216-7a99-4afe-8969-c94892920004/mark.json`
- `data/raw/TravelUAV/Carla_Town15/2a3c6950-0160-4832-bb9b-c6fa52f71684/mark.json`
- `data/raw/TravelUAV/Carla_Town15/2dad008b-a508-4b91-b660-ec4ad7abfbe1/mark.json`
- `data/raw/TravelUAV/Carla_Town15/32908e28-fc6e-4298-b4c7-3c86e7044fbd/mark.json`
- `data/raw/TravelUAV/Carla_Town15/32c7e3c8-0511-47e2-9904-5b8dd5be2302/mark.json`
- `data/raw/TravelUAV/Carla_Town15/32c7e3c8-0511-47e2-9904-5b8dd5be2302/object_description.json`

### yaw
- `data/raw/TravelUAV/Carla_Town15/02cce8d9-2f66-423b-8b51-df576f526efb/mark.json`
- `data/raw/TravelUAV/Carla_Town15/02df8d4e-c3a2-4d62-84dc-302e83ebb7b2/mark.json`
- `data/raw/TravelUAV/Carla_Town15/0643bcdd-0680-4af3-8e82-2426fdd7c27d/mark.json`
- `data/raw/TravelUAV/Carla_Town15/065a0114-94c2-4d72-b636-f2b55a792657/mark.json`
- `data/raw/TravelUAV/Carla_Town15/085f4a8d-23a4-4043-a449-c4b6b0d7b9c1/mark.json`
- `data/raw/TravelUAV/Carla_Town15/087521f0-520f-47e5-9728-e8b6704c8844/mark.json`
- `data/raw/TravelUAV/Carla_Town15/0d100cca-59a6-49bd-8319-4abe5c525aba/mark.json`
- `data/raw/TravelUAV/Carla_Town15/0d25c0da-2097-47bf-bc48-18a85283d48c/mark.json`
- `data/raw/TravelUAV/Carla_Town15/106f9915-4848-49e2-b40b-c66147f6148c/mark.json`
- `data/raw/TravelUAV/Carla_Town15/10abee26-2f28-4b30-bb83-39870ec2790e/mark.json`
- `data/raw/TravelUAV/Carla_Town15/12731094-4d5b-403b-904e-652210d82145/mark.json`
- `data/raw/TravelUAV/Carla_Town15/12f57f71-f4b4-4c11-b537-475b65c5a587/mark.json`
- `data/raw/TravelUAV/Carla_Town15/15c5dc77-6003-4419-8b7d-2ad2c0f3af65/mark.json`
- `data/raw/TravelUAV/Carla_Town15/161e008d-2ba6-4534-8bb6-2df39251b6a1/mark.json`
- `data/raw/TravelUAV/Carla_Town15/18905cc5-046a-471d-af79-7585f06ffeef/mark.json`
- `data/raw/TravelUAV/Carla_Town15/192079ac-6971-4718-ae50-a1ac7491a801/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1ab27e5b-05d5-4070-ac93-dae9c41b0857/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1ae08848-9aa3-4097-9094-0d83c0a5b21a/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1d207916-f5e0-4358-a0eb-a604765d234f/mark.json`
- `data/raw/TravelUAV/Carla_Town15/1d325b8d-b5ae-46f1-b8fe-1005ed59b3bf/mark.json`
- `data/raw/TravelUAV/Carla_Town15/21568703-f138-4702-b470-35bf80ee5c17/mark.json`
- `data/raw/TravelUAV/Carla_Town15/216c1d27-b709-48e6-9d3c-63fcd6bc3cc8/mark.json`
- `data/raw/TravelUAV/Carla_Town15/22b48e11-f1c2-4fbe-8387-d808cc86f787/mark.json`
- `data/raw/TravelUAV/Carla_Town15/2376b75d-ed34-4a5e-9e11-2dd2f10e3817/mark.json`
- `data/raw/TravelUAV/Carla_Town15/26b4648a-7439-439a-a6b7-b209b16e636b/mark.json`
- `data/raw/TravelUAV/Carla_Town15/29a52216-7a99-4afe-8969-c94892920004/mark.json`
- `data/raw/TravelUAV/Carla_Town15/2a3c6950-0160-4832-bb9b-c6fa52f71684/mark.json`
- `data/raw/TravelUAV/Carla_Town15/2dad008b-a508-4b91-b660-ec4ad7abfbe1/mark.json`
- `data/raw/TravelUAV/Carla_Town15/32908e28-fc6e-4298-b4c7-3c86e7044fbd/mark.json`
- `data/raw/TravelUAV/Carla_Town15/32c7e3c8-0511-47e2-9904-5b8dd5be2302/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3593928d-97d4-4a4f-bf0b-3447f68f9f47/mark.json`
- `data/raw/TravelUAV/Carla_Town15/35d5efeb-1459-4e7e-946f-9c89e7223712/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3872d501-d115-451c-ae1c-b75f41cf5031/mark.json`
- `data/raw/TravelUAV/Carla_Town15/38b17fe1-598c-47d2-8de5-8b9df5c76ef6/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3b6a2169-a8e4-40db-acb2-69a4d6f855cd/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3b739ae9-08aa-4db6-9084-9d2761a44796/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3ce1b883-7f87-402a-97ed-2cd355d6a50f/mark.json`
- `data/raw/TravelUAV/Carla_Town15/3d2fa034-828e-4ae9-9cac-43180127581d/mark.json`
- `data/raw/TravelUAV/Carla_Town15/40eb2255-4781-44b0-9d3b-4c77882d3a2c/mark.json`
- `data/raw/TravelUAV/Carla_Town15/40fe156f-22d9-4eb9-8ef0-030a51735442/mark.json`

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
