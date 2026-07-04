# AeroVLA Reference Notes

## How AeroVLA Uses TravelUAV

AeroVLA README 明确要求下载 TravelUAV 的 `dataset_raw` 和仿真环境。其评估脚本使用 `data/uav_dataset/*_splits/*.json` 中的条目，每条包含 `json` 字段，指向 `dataset_raw/<Map>/<Episode>/merged_data.json`。

`src/vlnce_src/env_uav.py` 会读取这些 split JSON，再加载对应的 `merged_data.json`，从中使用：

- `trajectory_raw_detailed`
- `conversations[0].value`
- episode 所在 map 和 sequence
- `mark.json` 中的目标对象信息

## Use of merged_data.json

AeroVLA README 写明 `merged_data.json` 不包含在 raw download 中，需要用 TravelUAV 工具生成。TravelUAV 的 `Model/LLaMA-UAV/tools/generate_merged_json.py` 会从日志、相机帧和目标描述生成 `merged_data.json`。

因此，`merged_data.json` 是 TravelUAV 到 AeroVLA 评估管线的关键入口。

## Observation / Instruction / Action

AeroVLA 的 observation 来自 AirSim 当前帧。`aerialvla_wrapper_ui.py` 使用前视图和下视图拼成 224x448 mosaic，再送入 OpenVLA tokenizer/processor。

Instruction 来自 TravelUAV 的 `conversations[0].value`，并通过当前状态和目标位置生成额外方向提示，例如 `Fly forward-right and find the target...`。

Action 输出不是 waypoint 列表，而是文本中解析出的三个连续控制量：

- `fwd`
- `down`
- `yaw`

另有 `LAND` 或近零动作作为停止信号。

## Continuous Action Space

AeroVLA 使用 3-DoF 风格动作：

- forward displacement/range
- vertical down displacement
- yaw adjustment

`AirVLNSimulatorClientTool_AerialVLA.py` 将 `fwd/down/yaw` 转换为 AirSim 中的 yaw 旋转、目标位移和 `moveByVelocityAsync` / `moveToZAsync` 控制。

## Useful References

- TravelUAV split JSON 到 `merged_data.json` 的组织方式。
- `trajectory_raw_detailed` 作为状态轨迹来源。
- 前视图 + 下视图的 UAV observation 设计。
- 方向 prompt 的设计思路。
- 连续 UAV 控制量进入 AirSim 的方式。

## What Not to Copy Directly

- 不直接复现 AeroVLA 的文本离散 bin action 输出。
- 不在本地加载 `openvla-7b` 和 LoRA adapter。
- 不运行 AeroVLA 的闭环评估脚本。
- 不把 AeroVLA 的 3 维 `fwd/down/yaw` 直接作为本项目最终动作空间。

## Difference from This Project

- AeroVLA 是参考项目，不是本项目简单复现目标。
- 本项目核心是从通用机器人 VLA 模型 OpenVLA-OFT 迁移到 UAV 仿真 VLN。
- 本项目重点做 TravelUAV -> OpenVLA-OFT 数据通路，以及机器人动作空间到 UAV 连续动作空间的迁移。
- 本项目当前定义 `state=[x,y,z,yaw]`，`action=[vx,vy,vz,yaw_rate]`。
- 后续底层控制使用 Diffusion Policy 生成控制序列。
- 专家轨迹生成使用强化学习算法。
