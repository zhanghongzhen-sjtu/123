# System Design

## Overall Route

```text
TravelUAV 数据
-> observation / image / instruction / trajectory
-> UAV state/action adapter
-> OpenVLA-OFT-style JSONL
-> UAV continuous action head
-> Diffusion Policy 控制序列
-> RL 专家轨迹生成
-> 仿真评估
```

## Why Build the Data Path First

VLA 迁移的核心风险不是先能不能训练，而是数据字段、状态定义、动作定义和模型输入输出契约是否一致。当前先打通 TravelUAV 轨迹到 `[image, instruction, state, action, action_chunk]` 的轻量 JSONL，可以在不加载模型的情况下验证工程接口。

## Why Not Train Now

OpenVLA-OFT / openvla-7b 加载、LoRA / OFT 微调、Diffusion Policy 训练和闭环仿真评估都属于显存和时间开销较高的任务。本地 RTX 3060 不适合作为第一阶段训练平台。当前只验证数据通路和格式正确性。

## Why TravelUAV

普通 UAV 检测数据集通常只提供图像和目标标签，缺少自然语言导航指令、连续轨迹和仿真评估接口。TravelUAV 提供 UAV VLN 场景、地图、轨迹、目标和语言指令，更适合作为 VLA + UAV + RL + Diffusion Policy 的研究数据基础。

## Why OpenVLA-OFT to UAV Is Cross-Embodiment Transfer

OpenVLA-OFT 原始任务主要面向机器人操作，action/proprio 维度和物理语义与 UAV 不同。UAV 的状态为 `state=[x,y,z,yaw]`，动作为 `action=[vx,vy,vz,yaw_rate]`。把机器人 VLA 的视觉语言表示、action chunk 和 continuous action head 迁移到 UAV 3D 导航控制，是跨形态迁移问题。

## Why AeroVLA Is Reference Only

AeroVLA 已经展示了 TravelUAV 上的端到端 UAV VLA 思路，并使用双视角、方向 prompt 和连续控制输出。我的项目参考其数据组织和评估接口，但研究重点不同：不是复现 AeroVLA，而是构建 OpenVLA-OFT 风格的数据通路、UAV action adapter，并为后续 Diffusion Policy 和 RL 专家轨迹生成预留接口。

## 3-Map Data Path Validation

本地已完成 `BrushifyCountryRoads`、`BrushifyUrban`、`Carla_Town02` 三个 TravelUAV raw 地图子集的数据通路验证。三个子集没有预生成 `merged_data.json`，因此当前转换链路直接读取 raw episode：

```text
log/*.json + frontcamera/*.png + object_description.json + mark.json
-> state=[x,y,z,yaw]
-> timestamp-based dt
-> action=[vx,vy,vz,yaw_rate]
-> action_chunk
-> OpenVLA-OFT-style JSONL
```

验证结果说明：在不训练、不加载大模型、不跑闭环仿真的前提下，真实 TravelUAV raw 数据可以被转换成包含 `image`、`instruction`、`state`、`action`、`action_chunk` 的训练前格式样例。

后续训练前数据应继续保留每行真实 `dt`，并避免把 image-aligned 的 5 帧位移误当作 1 秒位移。当前三地图审计中 `dt` 均来自 `sensors.state.timestamp`，平均约 4.97 秒。

## Frozen Debug Schema

当前第一阶段数据接口固定为 `uav_openvla_jsonl_v0.1`：

```text
image + instruction + state=[x,y,z,yaw] + action=[vx,vy,vz,yaw_rate] + action_chunk + dt + source
```

详细字段约束见 `docs/uav_jsonl_schema.md`。该 schema 不是最终训练配置，而是用于保证 TravelUAV raw 数据、UAV action adapter 和未来 OpenVLA-OFT dataset loader 之间的接口一致。

## 3-Map Statistics

已生成小样本统计：

- `data/debug/traveluav_3maps_stats.json`
- `docs/traveluav_3maps_stats.md`

统计覆盖 174 行真实 debug 样本，`action_chunk` 长度均为 8，`dt_source` 均为 `timestamp`。这些统计可用于后续代码接口规划和归一化字段设计，但完整训练前必须使用实际训练 split 重新计算统计。

## Next Integration Step

后续 OpenVLA-OFT 接入不应直接开始训练。推荐先做 CPU-only dataset-loader smoke test：读取 JSONL，解析 image path、instruction、4D state、4D action、action chunk 和 normalization config，但不加载 OpenVLA-OFT / openvla-7b 权重。完整改造计划见 `docs/openvla_oft_uav_modification_plan.md`。

该 smoke test 已完成：

```text
UAV JSONL -> UavJsonlDataset -> image_path/instruction/state/action/action_chunk/dt/source
```

测试覆盖：

- `data/debug/traveluav_3maps_debug.jsonl` 的 60 行合并小文件。
- 三个单地图 debug JSONL 的 174 行完整 debug 文件。
- `--image-root .` 图片路径存在检查。
- `data/debug/traveluav_3maps_stats.json` 归一化向量读取。
- `state_normalized`、`action_normalized`、`action_chunk_normalized` 字段生成。

成功标记：

```text
SMOKE_PASS: UAV JSONL dataset loader works without model loading.
```

## OpenVLA-OFT Adapter Smoke Test

在 dataset loader 之后，已新增 CPU-only OpenVLA-OFT-style collator，用于验证未来训练 dataloader 的 batch 形状：

```text
UavJsonlDataset samples
-> OpenVLAOFTUavCollator
-> image_paths / instructions / states / actions / action_chunks / dts / sources
```

当前空跑结果：

- batch size: 8
- states: `[8, 4]`
- actions: `[8, 4]`
- action_chunks: `[8, 8, 4]`
- normalized states/actions/action_chunks: shape 正确
- image path check: enabled
- model loading: none

报告文件：

- `docs/openvla_oft_adapter_smoke_report.md`
- `docs/openvla_oft_dataset_adapter_design.md`

这一步说明数据接口已经能形成 OpenVLA-OFT 迁移训练所需的 batch 形状，但仍不代表可以直接训练。全量 train/val split、完整统计、OpenVLA-OFT 真实 dataset adapter、proprio projector 和 4D action head 仍需后续完成。

## Pseudo Config

已新增本地 pseudo config：

- `configs/openvla_oft_uav_debug.yaml`
- `docs/openvla_oft_uav_pseudo_config.md`
- `docs/openvla_oft_uav_pseudo_config_check_report.md`

该配置固定了当前 debug 数据、UAV 4D state/action、action chunk size 8、stats 文件、OpenVLA-OFT 字段映射和 future 5090 阶段计划。配置检查通过：

```text
PSEUDO_CONFIG_PASS: local OpenVLA-OFT UAV pseudo config is valid and training remains disabled.
```

配置中的训练、模型加载、LoRA/OFT、仿真、Diffusion Policy 和 RL 开关均为 false，因此它只作为接口契约，不是训练配置。
