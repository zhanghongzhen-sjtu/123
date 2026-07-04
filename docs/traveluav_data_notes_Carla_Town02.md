# TravelUAV Data Notes

## Inspection Scope
- TravelUAV root: `external/TravelUAV`
- Dataset root: `data/raw/TravelUAV/Carla_Town02`
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

- `data/raw/TravelUAV/Carla_Town02/01fa26b7-98aa-4284-b75d-d1fad1f81ee2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/01fa26b7-98aa-4284-b75d-d1fad1f81ee2/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/023a87bc-8f55-4c47-b14e-ee4f738466ca/mark.json`
- `data/raw/TravelUAV/Carla_Town02/023a87bc-8f55-4c47-b14e-ee4f738466ca/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/02d774d3-2987-474b-87f6-7da6197b0d2e/mark.json`
- `data/raw/TravelUAV/Carla_Town02/02d774d3-2987-474b-87f6-7da6197b0d2e/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0344a972-a323-4079-bd8f-6337e9e746e2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0344a972-a323-4079-bd8f-6337e9e746e2/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/03bef537-73f4-409c-a5b1-ef880e2a15cd/mark.json`
- `data/raw/TravelUAV/Carla_Town02/03bef537-73f4-409c-a5b1-ef880e2a15cd/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/03c77242-e272-4521-94b9-af48995f6165/mark.json`
- `data/raw/TravelUAV/Carla_Town02/03c77242-e272-4521-94b9-af48995f6165/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/043abbf2-31f8-4631-82ae-d96d13c3af57/mark.json`
- `data/raw/TravelUAV/Carla_Town02/043abbf2-31f8-4631-82ae-d96d13c3af57/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/045e7f58-02b1-4ff5-a9f1-69d7e4dacc4c/mark.json`
- `data/raw/TravelUAV/Carla_Town02/045e7f58-02b1-4ff5-a9f1-69d7e4dacc4c/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/04600454-5345-40fe-90b4-72e6b03aa2a0/mark.json`
- `data/raw/TravelUAV/Carla_Town02/04600454-5345-40fe-90b4-72e6b03aa2a0/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/04c026bb-7b37-4daf-bbd7-e8652a50dcf8/mark.json`
- `data/raw/TravelUAV/Carla_Town02/04c026bb-7b37-4daf-bbd7-e8652a50dcf8/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/05268af3-40b0-4d06-85b2-7a8a29448b9c/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05268af3-40b0-4d06-85b2-7a8a29448b9c/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/052bf106-4d47-4583-8387-6a486ca7bfa8/mark.json`
- `data/raw/TravelUAV/Carla_Town02/052bf106-4d47-4583-8387-6a486ca7bfa8/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0596fe30-486e-48ba-a7ba-c6d967742a50/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0596fe30-486e-48ba-a7ba-c6d967742a50/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/05a09b7c-ff81-4009-9e25-ceb09c334766/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05a09b7c-ff81-4009-9e25-ceb09c334766/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/05abaa9b-6a3e-43ea-b9a6-1eec33e781de/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05abaa9b-6a3e-43ea-b9a6-1eec33e781de/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0619b5ff-328d-43ba-aad7-5095bcfe5c3a/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0619b5ff-328d-43ba-aad7-5095bcfe5c3a/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/062132ab-4c96-4426-920e-2dea5bb773de/mark.json`
- `data/raw/TravelUAV/Carla_Town02/062132ab-4c96-4426-920e-2dea5bb773de/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/064792a2-f001-405c-a2f7-bac638ccdd29/mark.json`
- `data/raw/TravelUAV/Carla_Town02/064792a2-f001-405c-a2f7-bac638ccdd29/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/07851403-91e4-4b2e-92c2-a3250590bfb0/mark.json`
- `data/raw/TravelUAV/Carla_Town02/07851403-91e4-4b2e-92c2-a3250590bfb0/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/07b03001-65a2-4335-a074-257e8ab151e1/mark.json`
- `data/raw/TravelUAV/Carla_Town02/07b03001-65a2-4335-a074-257e8ab151e1/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0855aeb5-5d7d-4800-834a-443daecfb497/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0855aeb5-5d7d-4800-834a-443daecfb497/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/09296113-bf16-4ad5-af9b-638477e569ee/mark.json`
- `data/raw/TravelUAV/Carla_Town02/09296113-bf16-4ad5-af9b-638477e569ee/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/092f790d-aeda-4cdc-b5f6-a6c92e64aa97/mark.json`
- `data/raw/TravelUAV/Carla_Town02/092f790d-aeda-4cdc-b5f6-a6c92e64aa97/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/09ba8c4a-4be2-4b66-b1f8-934e40180e7c/mark.json`
- `data/raw/TravelUAV/Carla_Town02/09ba8c4a-4be2-4b66-b1f8-934e40180e7c/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/09c9048a-15db-43dd-a2c6-cbb1e8b4c0b2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/09c9048a-15db-43dd-a2c6-cbb1e8b4c0b2/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0a0b8257-06ae-4b07-a830-c3e45614f802/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0a0b8257-06ae-4b07-a830-c3e45614f802/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0a41b6ff-9eb7-4823-ae59-985a067ad8ab/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0a41b6ff-9eb7-4823-ae59-985a067ad8ab/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0afd24a4-b6d6-474e-be30-959e495064f2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0afd24a4-b6d6-474e-be30-959e495064f2/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0b36dd69-42b9-40f9-aa22-2c73eaf74e92/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0b36dd69-42b9-40f9-aa22-2c73eaf74e92/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0bb7c8f3-42d3-4a1f-b63a-b2fa257163e9/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0bb7c8f3-42d3-4a1f-b63a-b2fa257163e9/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0bbb2ef4-2368-4173-8d83-859a9a455181/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0bbb2ef4-2368-4173-8d83-859a9a455181/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0c5716c4-2f32-4928-8276-996330637645/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0c5716c4-2f32-4928-8276-996330637645/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0c7229f1-1f90-4008-b3e4-50056f47d8cd/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0c7229f1-1f90-4008-b3e4-50056f47d8cd/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0cc9ca8d-e13d-4195-9786-a7c34af50a38/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0cc9ca8d-e13d-4195-9786-a7c34af50a38/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0ce267b7-cded-4e5c-aa2c-50dac661e5d1/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0ce267b7-cded-4e5c-aa2c-50dac661e5d1/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0d110d23-585b-40d6-9bfe-ed298126b852/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0d110d23-585b-40d6-9bfe-ed298126b852/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0d2865ac-b23e-4879-bdd8-8f403a103464/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0d2865ac-b23e-4879-bdd8-8f403a103464/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0d9b0d02-cd89-4ce4-8004-b4b83a719b04/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0d9b0d02-cd89-4ce4-8004-b4b83a719b04/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0e2fe952-9eb3-44a0-9ec4-fc643ca9995a/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0e2fe952-9eb3-44a0-9ec4-fc643ca9995a/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0e311399-9791-414c-b2ac-61e2724c12c8/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0e311399-9791-414c-b2ac-61e2724c12c8/object_description.json`

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
- `data/raw/TravelUAV/Carla_Town02/09296113-bf16-4ad5-af9b-638477e569ee/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0a0b8257-06ae-4b07-a830-c3e45614f802/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0ce267b7-cded-4e5c-aa2c-50dac661e5d1/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0e311399-9791-414c-b2ac-61e2724c12c8/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/107e40dc-04eb-447e-bbed-7807e695059c/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/14273108-5e83-41e5-a53c-79a84a262ad2/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/17569493-dfec-4df9-824a-306bf4dd7e2a/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/1dd1a52b-1c36-4bb4-ab6d-5c61200f0892/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/2723910e-e77a-4f4a-b3ef-2aa0cbedcaf7/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/2993276f-056a-40e6-8e81-b3bf588fa53b/object_description.json`
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
- `data/raw/TravelUAV/Carla_Town02/01fa26b7-98aa-4284-b75d-d1fad1f81ee2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/023a87bc-8f55-4c47-b14e-ee4f738466ca/mark.json`
- `data/raw/TravelUAV/Carla_Town02/02d774d3-2987-474b-87f6-7da6197b0d2e/mark.json`
- `data/raw/TravelUAV/Carla_Town02/02d774d3-2987-474b-87f6-7da6197b0d2e/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0344a972-a323-4079-bd8f-6337e9e746e2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/03bef537-73f4-409c-a5b1-ef880e2a15cd/mark.json`
- `data/raw/TravelUAV/Carla_Town02/03c77242-e272-4521-94b9-af48995f6165/mark.json`
- `data/raw/TravelUAV/Carla_Town02/043abbf2-31f8-4631-82ae-d96d13c3af57/mark.json`
- `data/raw/TravelUAV/Carla_Town02/045e7f58-02b1-4ff5-a9f1-69d7e4dacc4c/mark.json`
- `data/raw/TravelUAV/Carla_Town02/04600454-5345-40fe-90b4-72e6b03aa2a0/mark.json`
- `data/raw/TravelUAV/Carla_Town02/04c026bb-7b37-4daf-bbd7-e8652a50dcf8/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05268af3-40b0-4d06-85b2-7a8a29448b9c/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05268af3-40b0-4d06-85b2-7a8a29448b9c/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/052bf106-4d47-4583-8387-6a486ca7bfa8/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0596fe30-486e-48ba-a7ba-c6d967742a50/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05a09b7c-ff81-4009-9e25-ceb09c334766/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05abaa9b-6a3e-43ea-b9a6-1eec33e781de/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0619b5ff-328d-43ba-aad7-5095bcfe5c3a/mark.json`
- `data/raw/TravelUAV/Carla_Town02/062132ab-4c96-4426-920e-2dea5bb773de/mark.json`
- `data/raw/TravelUAV/Carla_Town02/064792a2-f001-405c-a2f7-bac638ccdd29/mark.json`
- `data/raw/TravelUAV/Carla_Town02/07851403-91e4-4b2e-92c2-a3250590bfb0/mark.json`
- `data/raw/TravelUAV/Carla_Town02/07b03001-65a2-4335-a074-257e8ab151e1/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0855aeb5-5d7d-4800-834a-443daecfb497/mark.json`
- `data/raw/TravelUAV/Carla_Town02/09296113-bf16-4ad5-af9b-638477e569ee/mark.json`
- `data/raw/TravelUAV/Carla_Town02/092f790d-aeda-4cdc-b5f6-a6c92e64aa97/mark.json`
- `data/raw/TravelUAV/Carla_Town02/09ba8c4a-4be2-4b66-b1f8-934e40180e7c/mark.json`
- `data/raw/TravelUAV/Carla_Town02/09c9048a-15db-43dd-a2c6-cbb1e8b4c0b2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0a0b8257-06ae-4b07-a830-c3e45614f802/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0a0b8257-06ae-4b07-a830-c3e45614f802/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0a41b6ff-9eb7-4823-ae59-985a067ad8ab/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0a41b6ff-9eb7-4823-ae59-985a067ad8ab/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0afd24a4-b6d6-474e-be30-959e495064f2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0b36dd69-42b9-40f9-aa22-2c73eaf74e92/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0bb7c8f3-42d3-4a1f-b63a-b2fa257163e9/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0bbb2ef4-2368-4173-8d83-859a9a455181/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0c5716c4-2f32-4928-8276-996330637645/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0c5716c4-2f32-4928-8276-996330637645/object_description.json`
- `data/raw/TravelUAV/Carla_Town02/0c7229f1-1f90-4008-b3e4-50056f47d8cd/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0cc9ca8d-e13d-4195-9786-a7c34af50a38/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0ce267b7-cded-4e5c-aa2c-50dac661e5d1/mark.json`

### yaw
- `data/raw/TravelUAV/Carla_Town02/01fa26b7-98aa-4284-b75d-d1fad1f81ee2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/023a87bc-8f55-4c47-b14e-ee4f738466ca/mark.json`
- `data/raw/TravelUAV/Carla_Town02/02d774d3-2987-474b-87f6-7da6197b0d2e/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0344a972-a323-4079-bd8f-6337e9e746e2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/03bef537-73f4-409c-a5b1-ef880e2a15cd/mark.json`
- `data/raw/TravelUAV/Carla_Town02/03c77242-e272-4521-94b9-af48995f6165/mark.json`
- `data/raw/TravelUAV/Carla_Town02/043abbf2-31f8-4631-82ae-d96d13c3af57/mark.json`
- `data/raw/TravelUAV/Carla_Town02/045e7f58-02b1-4ff5-a9f1-69d7e4dacc4c/mark.json`
- `data/raw/TravelUAV/Carla_Town02/04600454-5345-40fe-90b4-72e6b03aa2a0/mark.json`
- `data/raw/TravelUAV/Carla_Town02/04c026bb-7b37-4daf-bbd7-e8652a50dcf8/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05268af3-40b0-4d06-85b2-7a8a29448b9c/mark.json`
- `data/raw/TravelUAV/Carla_Town02/052bf106-4d47-4583-8387-6a486ca7bfa8/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0596fe30-486e-48ba-a7ba-c6d967742a50/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05a09b7c-ff81-4009-9e25-ceb09c334766/mark.json`
- `data/raw/TravelUAV/Carla_Town02/05abaa9b-6a3e-43ea-b9a6-1eec33e781de/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0619b5ff-328d-43ba-aad7-5095bcfe5c3a/mark.json`
- `data/raw/TravelUAV/Carla_Town02/062132ab-4c96-4426-920e-2dea5bb773de/mark.json`
- `data/raw/TravelUAV/Carla_Town02/064792a2-f001-405c-a2f7-bac638ccdd29/mark.json`
- `data/raw/TravelUAV/Carla_Town02/07851403-91e4-4b2e-92c2-a3250590bfb0/mark.json`
- `data/raw/TravelUAV/Carla_Town02/07b03001-65a2-4335-a074-257e8ab151e1/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0855aeb5-5d7d-4800-834a-443daecfb497/mark.json`
- `data/raw/TravelUAV/Carla_Town02/09296113-bf16-4ad5-af9b-638477e569ee/mark.json`
- `data/raw/TravelUAV/Carla_Town02/092f790d-aeda-4cdc-b5f6-a6c92e64aa97/mark.json`
- `data/raw/TravelUAV/Carla_Town02/09ba8c4a-4be2-4b66-b1f8-934e40180e7c/mark.json`
- `data/raw/TravelUAV/Carla_Town02/09c9048a-15db-43dd-a2c6-cbb1e8b4c0b2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0a0b8257-06ae-4b07-a830-c3e45614f802/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0a41b6ff-9eb7-4823-ae59-985a067ad8ab/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0afd24a4-b6d6-474e-be30-959e495064f2/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0b36dd69-42b9-40f9-aa22-2c73eaf74e92/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0bb7c8f3-42d3-4a1f-b63a-b2fa257163e9/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0bbb2ef4-2368-4173-8d83-859a9a455181/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0c5716c4-2f32-4928-8276-996330637645/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0c7229f1-1f90-4008-b3e4-50056f47d8cd/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0cc9ca8d-e13d-4195-9786-a7c34af50a38/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0ce267b7-cded-4e5c-aa2c-50dac661e5d1/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0d110d23-585b-40d6-9bfe-ed298126b852/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0d2865ac-b23e-4879-bdd8-8f403a103464/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0d9b0d02-cd89-4ce4-8004-b4b83a719b04/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0e2fe952-9eb3-44a0-9ec4-fc643ca9995a/mark.json`
- `data/raw/TravelUAV/Carla_Town02/0e311399-9791-414c-b2ac-61e2724c12c8/mark.json`

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
