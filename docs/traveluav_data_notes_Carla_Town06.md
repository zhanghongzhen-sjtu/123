# TravelUAV Data Notes

## Inspection Scope
- TravelUAV root: `external/TravelUAV`
- Dataset root: `data/raw/TravelUAV/Carla_Town06`
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

- `data/raw/TravelUAV/Carla_Town06/02bd54e2-3802-4472-9d47-08ad6130ce2e/mark.json`
- `data/raw/TravelUAV/Carla_Town06/02bd54e2-3802-4472-9d47-08ad6130ce2e/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/02c3eed4-b5df-4385-b270-7ac1f98fdda2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/02c3eed4-b5df-4385-b270-7ac1f98fdda2/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/03410934-e474-4d74-8ca7-9a9fdf32d0b8/mark.json`
- `data/raw/TravelUAV/Carla_Town06/03410934-e474-4d74-8ca7-9a9fdf32d0b8/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/076f2892-c438-4981-98bc-36792dfd9b7a/mark.json`
- `data/raw/TravelUAV/Carla_Town06/076f2892-c438-4981-98bc-36792dfd9b7a/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/07f90428-01f0-4b93-9013-77e0c02098b6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/07f90428-01f0-4b93-9013-77e0c02098b6/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/087f3acc-7daa-42c9-a862-881eff880bd3/mark.json`
- `data/raw/TravelUAV/Carla_Town06/087f3acc-7daa-42c9-a862-881eff880bd3/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/0cab68a3-a33a-4b33-af5e-0df74bc0fd94/mark.json`
- `data/raw/TravelUAV/Carla_Town06/0cab68a3-a33a-4b33-af5e-0df74bc0fd94/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/0d99900b-0b29-4609-940e-30ae5f91d7b6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/0d99900b-0b29-4609-940e-30ae5f91d7b6/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/0ecb5180-8fdb-485b-abfa-93ae80cb7b21/mark.json`
- `data/raw/TravelUAV/Carla_Town06/0ecb5180-8fdb-485b-abfa-93ae80cb7b21/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/1473eb77-fd76-46e7-aec0-9ae36da821d2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1473eb77-fd76-46e7-aec0-9ae36da821d2/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/149c812f-9f10-4a62-b8c9-f336346242e4/mark.json`
- `data/raw/TravelUAV/Carla_Town06/149c812f-9f10-4a62-b8c9-f336346242e4/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/15891121-23fd-435e-9fba-476bc045db39/mark.json`
- `data/raw/TravelUAV/Carla_Town06/15891121-23fd-435e-9fba-476bc045db39/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/1a6335e8-fcc2-48bf-9dd7-afc9c0a23d12/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1a6335e8-fcc2-48bf-9dd7-afc9c0a23d12/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/1b159c2a-4d40-4ebd-8447-60f191d50070/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1b159c2a-4d40-4ebd-8447-60f191d50070/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/1da57ccc-45d2-4294-b694-c93b809b9063/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1da57ccc-45d2-4294-b694-c93b809b9063/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/234e591c-aa89-418c-b66b-cddd2bdadb30/mark.json`
- `data/raw/TravelUAV/Carla_Town06/234e591c-aa89-418c-b66b-cddd2bdadb30/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/239c6bf2-eb82-44e2-a826-b3f0e6819ef9/mark.json`
- `data/raw/TravelUAV/Carla_Town06/239c6bf2-eb82-44e2-a826-b3f0e6819ef9/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/24fe5db4-c19d-41d5-bd06-943a378335f7/mark.json`
- `data/raw/TravelUAV/Carla_Town06/24fe5db4-c19d-41d5-bd06-943a378335f7/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/2b478eac-ac1e-4a47-ae9a-0b35115a9e1a/mark.json`
- `data/raw/TravelUAV/Carla_Town06/2b478eac-ac1e-4a47-ae9a-0b35115a9e1a/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/2b601934-5b6f-4b3a-a619-981783010322/mark.json`
- `data/raw/TravelUAV/Carla_Town06/2b601934-5b6f-4b3a-a619-981783010322/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/2f71f5b3-4d78-4054-8e27-6dc062035809/mark.json`
- `data/raw/TravelUAV/Carla_Town06/2f71f5b3-4d78-4054-8e27-6dc062035809/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/33fe18e6-04a1-4d76-99d5-a146f775c58f/mark.json`
- `data/raw/TravelUAV/Carla_Town06/33fe18e6-04a1-4d76-99d5-a146f775c58f/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/3455d7d6-f01f-44e4-a6fe-88705e25fc52/mark.json`
- `data/raw/TravelUAV/Carla_Town06/3455d7d6-f01f-44e4-a6fe-88705e25fc52/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/34bb61e6-e6bc-44e4-b734-96cdc2e202ef/mark.json`
- `data/raw/TravelUAV/Carla_Town06/34bb61e6-e6bc-44e4-b734-96cdc2e202ef/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/3ff30709-2eee-4f3c-8d20-4f168757c022/mark.json`
- `data/raw/TravelUAV/Carla_Town06/3ff30709-2eee-4f3c-8d20-4f168757c022/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/40cc61bb-520d-493a-a72e-497781cf6be2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/40cc61bb-520d-493a-a72e-497781cf6be2/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/40ea6d5b-314c-4afb-a250-72a90db69431/mark.json`
- `data/raw/TravelUAV/Carla_Town06/40ea6d5b-314c-4afb-a250-72a90db69431/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/43df6dd5-e1ce-41b9-9396-0c01c29704e4/mark.json`
- `data/raw/TravelUAV/Carla_Town06/43df6dd5-e1ce-41b9-9396-0c01c29704e4/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/45a3bcc8-2635-4eba-937d-2b3b3385f111/mark.json`
- `data/raw/TravelUAV/Carla_Town06/45a3bcc8-2635-4eba-937d-2b3b3385f111/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/45f8f092-7ff7-482c-a173-06424807ebf2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/45f8f092-7ff7-482c-a173-06424807ebf2/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/4b2b893b-f1ff-4144-91d0-c51489d57b50/mark.json`
- `data/raw/TravelUAV/Carla_Town06/4b2b893b-f1ff-4144-91d0-c51489d57b50/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/4b9ce9f5-ec3e-4cac-974d-d8b38e37cbe6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/4b9ce9f5-ec3e-4cac-974d-d8b38e37cbe6/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/4ba54ff6-bac3-435c-956f-0bfb87679614/mark.json`
- `data/raw/TravelUAV/Carla_Town06/4ba54ff6-bac3-435c-956f-0bfb87679614/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/51911d27-10f2-4d3b-be4b-39419c46e717/mark.json`
- `data/raw/TravelUAV/Carla_Town06/51911d27-10f2-4d3b-be4b-39419c46e717/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/51fcd20f-96ec-4ed8-9cf8-12b851f4238f/mark.json`
- `data/raw/TravelUAV/Carla_Town06/51fcd20f-96ec-4ed8-9cf8-12b851f4238f/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/521092b8-6e92-49cc-aa17-c7aca3ce24d4/mark.json`
- `data/raw/TravelUAV/Carla_Town06/521092b8-6e92-49cc-aa17-c7aca3ce24d4/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/5a3914eb-e686-47b4-b76d-a63da05534e6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/5a3914eb-e686-47b4-b76d-a63da05534e6/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/5add9b38-78d1-451c-b4cd-0636a5a972ee/mark.json`
- `data/raw/TravelUAV/Carla_Town06/5add9b38-78d1-451c-b4cd-0636a5a972ee/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/5af52e8d-ee28-4da7-ad39-2b8f7001fbbb/mark.json`
- `data/raw/TravelUAV/Carla_Town06/5af52e8d-ee28-4da7-ad39-2b8f7001fbbb/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/606901b9-ba4a-48dd-8339-d0d84bb1c426/mark.json`
- `data/raw/TravelUAV/Carla_Town06/606901b9-ba4a-48dd-8339-d0d84bb1c426/object_description.json`

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
- `data/raw/TravelUAV/Carla_Town06/0ecb5180-8fdb-485b-abfa-93ae80cb7b21/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/15891121-23fd-435e-9fba-476bc045db39/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/239c6bf2-eb82-44e2-a826-b3f0e6819ef9/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/33fe18e6-04a1-4d76-99d5-a146f775c58f/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/4b2b893b-f1ff-4144-91d0-c51489d57b50/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/5a3914eb-e686-47b4-b76d-a63da05534e6/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/61247534-5681-4617-81ea-27598e1edcde/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/8f6f1789-48cc-4d87-af3e-017e2f29d334/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/91c1fb74-fd78-4b84-8ded-053158e3d693/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/c13aaa0e-a580-46fb-a4e0-03d910f79ae9/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/ff96780a-595b-4c4c-af80-f1216c5071ab/object_description.json`
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
- `data/raw/TravelUAV/Carla_Town06/02bd54e2-3802-4472-9d47-08ad6130ce2e/mark.json`
- `data/raw/TravelUAV/Carla_Town06/02bd54e2-3802-4472-9d47-08ad6130ce2e/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/02c3eed4-b5df-4385-b270-7ac1f98fdda2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/03410934-e474-4d74-8ca7-9a9fdf32d0b8/mark.json`
- `data/raw/TravelUAV/Carla_Town06/03410934-e474-4d74-8ca7-9a9fdf32d0b8/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/076f2892-c438-4981-98bc-36792dfd9b7a/mark.json`
- `data/raw/TravelUAV/Carla_Town06/07f90428-01f0-4b93-9013-77e0c02098b6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/087f3acc-7daa-42c9-a862-881eff880bd3/mark.json`
- `data/raw/TravelUAV/Carla_Town06/087f3acc-7daa-42c9-a862-881eff880bd3/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/0cab68a3-a33a-4b33-af5e-0df74bc0fd94/mark.json`
- `data/raw/TravelUAV/Carla_Town06/0d99900b-0b29-4609-940e-30ae5f91d7b6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/0ecb5180-8fdb-485b-abfa-93ae80cb7b21/mark.json`
- `data/raw/TravelUAV/Carla_Town06/0ecb5180-8fdb-485b-abfa-93ae80cb7b21/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/1473eb77-fd76-46e7-aec0-9ae36da821d2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1473eb77-fd76-46e7-aec0-9ae36da821d2/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/149c812f-9f10-4a62-b8c9-f336346242e4/mark.json`
- `data/raw/TravelUAV/Carla_Town06/149c812f-9f10-4a62-b8c9-f336346242e4/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/15891121-23fd-435e-9fba-476bc045db39/mark.json`
- `data/raw/TravelUAV/Carla_Town06/15891121-23fd-435e-9fba-476bc045db39/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/1a6335e8-fcc2-48bf-9dd7-afc9c0a23d12/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1b159c2a-4d40-4ebd-8447-60f191d50070/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1da57ccc-45d2-4294-b694-c93b809b9063/mark.json`
- `data/raw/TravelUAV/Carla_Town06/234e591c-aa89-418c-b66b-cddd2bdadb30/mark.json`
- `data/raw/TravelUAV/Carla_Town06/239c6bf2-eb82-44e2-a826-b3f0e6819ef9/mark.json`
- `data/raw/TravelUAV/Carla_Town06/24fe5db4-c19d-41d5-bd06-943a378335f7/mark.json`
- `data/raw/TravelUAV/Carla_Town06/2b478eac-ac1e-4a47-ae9a-0b35115a9e1a/mark.json`
- `data/raw/TravelUAV/Carla_Town06/2b601934-5b6f-4b3a-a619-981783010322/mark.json`
- `data/raw/TravelUAV/Carla_Town06/2f71f5b3-4d78-4054-8e27-6dc062035809/mark.json`
- `data/raw/TravelUAV/Carla_Town06/33fe18e6-04a1-4d76-99d5-a146f775c58f/mark.json`
- `data/raw/TravelUAV/Carla_Town06/3455d7d6-f01f-44e4-a6fe-88705e25fc52/mark.json`
- `data/raw/TravelUAV/Carla_Town06/34bb61e6-e6bc-44e4-b734-96cdc2e202ef/mark.json`
- `data/raw/TravelUAV/Carla_Town06/34bb61e6-e6bc-44e4-b734-96cdc2e202ef/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/3ff30709-2eee-4f3c-8d20-4f168757c022/mark.json`
- `data/raw/TravelUAV/Carla_Town06/3ff30709-2eee-4f3c-8d20-4f168757c022/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/40cc61bb-520d-493a-a72e-497781cf6be2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/40cc61bb-520d-493a-a72e-497781cf6be2/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/40ea6d5b-314c-4afb-a250-72a90db69431/mark.json`
- `data/raw/TravelUAV/Carla_Town06/43df6dd5-e1ce-41b9-9396-0c01c29704e4/mark.json`
- `data/raw/TravelUAV/Carla_Town06/43df6dd5-e1ce-41b9-9396-0c01c29704e4/object_description.json`
- `data/raw/TravelUAV/Carla_Town06/45a3bcc8-2635-4eba-937d-2b3b3385f111/mark.json`

### yaw
- `data/raw/TravelUAV/Carla_Town06/02bd54e2-3802-4472-9d47-08ad6130ce2e/mark.json`
- `data/raw/TravelUAV/Carla_Town06/02c3eed4-b5df-4385-b270-7ac1f98fdda2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/03410934-e474-4d74-8ca7-9a9fdf32d0b8/mark.json`
- `data/raw/TravelUAV/Carla_Town06/076f2892-c438-4981-98bc-36792dfd9b7a/mark.json`
- `data/raw/TravelUAV/Carla_Town06/07f90428-01f0-4b93-9013-77e0c02098b6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/087f3acc-7daa-42c9-a862-881eff880bd3/mark.json`
- `data/raw/TravelUAV/Carla_Town06/0cab68a3-a33a-4b33-af5e-0df74bc0fd94/mark.json`
- `data/raw/TravelUAV/Carla_Town06/0d99900b-0b29-4609-940e-30ae5f91d7b6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/0ecb5180-8fdb-485b-abfa-93ae80cb7b21/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1473eb77-fd76-46e7-aec0-9ae36da821d2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/149c812f-9f10-4a62-b8c9-f336346242e4/mark.json`
- `data/raw/TravelUAV/Carla_Town06/15891121-23fd-435e-9fba-476bc045db39/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1a6335e8-fcc2-48bf-9dd7-afc9c0a23d12/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1b159c2a-4d40-4ebd-8447-60f191d50070/mark.json`
- `data/raw/TravelUAV/Carla_Town06/1da57ccc-45d2-4294-b694-c93b809b9063/mark.json`
- `data/raw/TravelUAV/Carla_Town06/234e591c-aa89-418c-b66b-cddd2bdadb30/mark.json`
- `data/raw/TravelUAV/Carla_Town06/239c6bf2-eb82-44e2-a826-b3f0e6819ef9/mark.json`
- `data/raw/TravelUAV/Carla_Town06/24fe5db4-c19d-41d5-bd06-943a378335f7/mark.json`
- `data/raw/TravelUAV/Carla_Town06/2b478eac-ac1e-4a47-ae9a-0b35115a9e1a/mark.json`
- `data/raw/TravelUAV/Carla_Town06/2b601934-5b6f-4b3a-a619-981783010322/mark.json`
- `data/raw/TravelUAV/Carla_Town06/2f71f5b3-4d78-4054-8e27-6dc062035809/mark.json`
- `data/raw/TravelUAV/Carla_Town06/33fe18e6-04a1-4d76-99d5-a146f775c58f/mark.json`
- `data/raw/TravelUAV/Carla_Town06/3455d7d6-f01f-44e4-a6fe-88705e25fc52/mark.json`
- `data/raw/TravelUAV/Carla_Town06/34bb61e6-e6bc-44e4-b734-96cdc2e202ef/mark.json`
- `data/raw/TravelUAV/Carla_Town06/3ff30709-2eee-4f3c-8d20-4f168757c022/mark.json`
- `data/raw/TravelUAV/Carla_Town06/40cc61bb-520d-493a-a72e-497781cf6be2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/40ea6d5b-314c-4afb-a250-72a90db69431/mark.json`
- `data/raw/TravelUAV/Carla_Town06/43df6dd5-e1ce-41b9-9396-0c01c29704e4/mark.json`
- `data/raw/TravelUAV/Carla_Town06/45a3bcc8-2635-4eba-937d-2b3b3385f111/mark.json`
- `data/raw/TravelUAV/Carla_Town06/45f8f092-7ff7-482c-a173-06424807ebf2/mark.json`
- `data/raw/TravelUAV/Carla_Town06/4b2b893b-f1ff-4144-91d0-c51489d57b50/mark.json`
- `data/raw/TravelUAV/Carla_Town06/4b9ce9f5-ec3e-4cac-974d-d8b38e37cbe6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/4ba54ff6-bac3-435c-956f-0bfb87679614/mark.json`
- `data/raw/TravelUAV/Carla_Town06/51911d27-10f2-4d3b-be4b-39419c46e717/mark.json`
- `data/raw/TravelUAV/Carla_Town06/51fcd20f-96ec-4ed8-9cf8-12b851f4238f/mark.json`
- `data/raw/TravelUAV/Carla_Town06/521092b8-6e92-49cc-aa17-c7aca3ce24d4/mark.json`
- `data/raw/TravelUAV/Carla_Town06/5a3914eb-e686-47b4-b76d-a63da05534e6/mark.json`
- `data/raw/TravelUAV/Carla_Town06/5add9b38-78d1-451c-b4cd-0636a5a972ee/mark.json`
- `data/raw/TravelUAV/Carla_Town06/5af52e8d-ee28-4da7-ad39-2b8f7001fbbb/mark.json`
- `data/raw/TravelUAV/Carla_Town06/606901b9-ba4a-48dd-8339-d0d84bb1c426/mark.json`

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
