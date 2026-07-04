# TravelUAV Data Notes

## 2026-07-04 3-Map Real Raw Data Validation

本地已只下载 3 个 TravelUAV 地图子集：

- `BrushifyCountryRoads`
- `BrushifyUrban`
- `Carla_Town02`

下载分卷均完整：

- `BrushifyCountryRoads.z01`
- `BrushifyCountryRoads.z02`
- `BrushifyCountryRoads.zip`
- `BrushifyUrban.z01`
- `BrushifyUrban.z02`
- `BrushifyUrban.zip`
- `Carla_Town02.z01`
- `Carla_Town02.z02`
- `Carla_Town02.zip`

解压后发现这 3 个子集是 raw episode 结构，而不是预生成 `merged_data.json` 结构。典型 episode 目录包括：

- `log/*.json`
- `frontcamera/*.png`
- `downcamera/*.png`
- `leftcamera/*.png`
- `rightcamera/*.png`
- `rearcamera/*.png`
- `object_description.json`
- `mark.json`

raw log 中已确认存在：

- `sensors.state.position`
- `sensors.state.orientation`
- `sensors.state.linear_velocity`
- `sensors.state.angular_velocity`
- `sensors.imu.orientation`

当前转换脚本已经支持直接从 raw episode 生成 OpenVLA-OFT-style JSONL：

- image: 使用 `frontcamera/<frame>.png`
- instruction: 使用 `object_description.json` 和 `mark.json.object_name` 构造 debug 指令
- state: 由 `log/*.json` 的 `position + orientation` 得到 `[x, y, z, yaw]`
- action: 由相邻 image-aligned state 计算 `[vx, vy, vz, yaw_rate]`
- action_chunk: 从未来 action 序列构造，chunk size 为 8

真实数据 debug 输出：

- `data/debug/traveluav_BrushifyCountryRoads_debug.jsonl`: 60 行
- `data/debug/traveluav_BrushifyUrban_debug.jsonl`: 60 行
- `data/debug/traveluav_Carla_Town02_debug.jsonl`: 54 行
- `data/debug/traveluav_3maps_debug.jsonl`: 60 行，每个地图最多取 20 行

四个 JSONL 均通过 `check_uav_jsonl.py`。额外使用 `--image-root .` 检查后，image 路径均可解析到本地文件。

## Timestamp-Based dt Calibration

初版真实数据转换使用命令行参数 `--dt 1.0` 作为固定时间间隔，但 raw episode 的图像帧是 `000000.png`、`000005.png`、`000010.png` 这样的 image-aligned 间隔。直接使用 `dt=1.0` 会把 5 帧位移当作 1 秒位移，导致 action 速度量级偏大。

当前转换脚本已改为：

- 优先读取 `log/*.json` 中的 `sensors.state.timestamp`。
- 对相邻 image-aligned log 计算真实 `dt`。
- 将每行 JSONL 的 `dt` 写为真实秒数。
- 在 `source.dt_source` 中记录 `timestamp` 或 fallback 来源。
- 在 `source` 中保留 `frame`、`next_frame`、`timestamp`、`next_timestamp`、`raw_linear_velocity`、`raw_angular_velocity`，方便后续审计。

三地图完整 debug JSONL 审计结果：

- rows: 174
- maps: 3
- episodes: 9
- `dt`: min=4.164089, max=5.004107, mean=4.966554, median=4.989106
- frame delta: 5
- dt sources: `timestamp`
- issues: none

与 raw log 速度量级对比后，非零 raw velocity 行的平均绝对误差约为：

- vx: 0.015947
- vy: 0.017164
- vz: 0.012027
- yaw_rate vs raw angular z: 0.010528

报告文件：

- `docs/traveluav_3maps_audit.md`
- `docs/traveluav_3maps_debug_audit.md`

## Frozen JSONL Schema And Statistics

当前真实 debug 数据接口已固定为 `uav_openvla_jsonl_v0.1`，字段包括：

```text
image + instruction + state=[x,y,z,yaw] + action=[vx,vy,vz,yaw_rate] + action_chunk + dt + source
```

Schema 文档：

- `docs/uav_jsonl_schema.md`

三地图统计已生成：

- `data/debug/traveluav_3maps_stats.json`
- `docs/traveluav_3maps_stats.md`

统计摘要：

- rows: 174
- maps: 3
- episodes: 9
- action chunk length: 8
- dt sources: `timestamp`
- action mean: `[-0.13566715958563544, -0.18310460726690508, -0.11972598082955935, -0.006232022407943826]`
- action std: `[0.6995363412683623, 0.5618171093169642, 0.30603431141399057, 0.08831146900677601]`

这些统计只用于第一阶段接口验证和后续归一化字段设计，不可作为完整训练集统计。

注意：这一步只验证真实数据转换流程，不训练模型，不加载 OpenVLA / OpenVLA-OFT / openvla-7b，不运行仿真。

## Inspection Scope
- TravelUAV root: `external/TravelUAV`
- Dataset root: `data/raw/TravelUAV`
- Dataset root exists: `True`
- Found `merged_data.json`: `0` sample path(s)

> 当前未发现完整 `dataset_raw` 或预生成 `merged_data.json`。本地已下载 3-map raw subset，并已通过 raw episode 结构完成转换验证；后续如果要做全量训练，需要用户再按实验计划放置完整 TravelUAV 数据。

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

- `data/meta/map_spawnarea_info.json`
- `data/meta/object_description.json`
- `data/traj_train/train_balance.json` (Git LFS pointer)
- `data/traj_train/val_8s_8k.json`
- `data/uav_dataset/seen_valset.json`
- `data/uav_dataset/trainset.json` (Git LFS pointer)
- `data/uav_dataset/unseen_valset.json`
- `src/model_wrapper/utils/GroundingDINO/requirements.txt`

## Observed JSON Field Hints

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
- `Model/LLaMA-UAV/tools/generate_merged_json.py`
- `Model/LLaMA-UAV/tools/preprocess_image2tensor.py`
- `data/traj_train/val_8s_8k.json`
- `scripts/dagger_NYC.sh`
- `scripts/eval.sh`
- `src/common/param.py`
- `src/model_wrapper/travel_llm.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/config/GroundingDINO_SwinB_cfg.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/backbone/backbone.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/backbone/position_encoding.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/backbone/swin_transformer.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/bertwarper.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/fuse_modules.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/ms_deform_attn.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/transformer.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/transformer_vanilla.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/models/GroundingDINO/utils.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/util/inference.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/util/utils.py`
- `src/model_wrapper/utils/travel_util.py`
- `src/vlnce_src/assist.py`
- `src/vlnce_src/closeloop_util.py`
- `src/vlnce_src/dagger.py`
- `src/vlnce_src/dino_monitor_online.py`
- `src/vlnce_src/env_uav.py`
- `src/vlnce_src/eval.py`

### yaw
- `Model/LLaMA-UAV/tools/generate_merged_json.py`
- `src/model_wrapper/travel_llm.py`
- `src/model_wrapper/utils/GroundingDINO/groundingdino/util/visualizer.py`
- `src/model_wrapper/utils/travel_util.py`
- `src/vlnce_src/env_uav.py`

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
