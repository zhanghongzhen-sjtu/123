# Thesis Method Draft

## Research Problem

本文研究面向无人机仿真导航的视觉语言动作模型迁移方法。给定 UAV 视觉观测、自然语言指令和当前状态，模型需要输出连续 UAV 控制动作，使无人机在三维仿真环境中根据语言目标完成导航。

## Input and Output

输入包括：

- UAV 图像观测，可先使用前视图，后续扩展到前视图和下视图。
- 自然语言指令，例如目标描述、方向提示和任务要求。
- UAV 当前状态：

```text
state = [x, y, z, yaw]
```

输出为连续 UAV 控制动作：

```text
action = [vx, vy, vz, yaw_rate]
```

其中 `vx, vy, vz` 表示速度控制量，`yaw_rate` 表示偏航角速度。

## Trajectory to Action

若 TravelUAV 原始数据未直接提供连续动作，则由相邻轨迹点计算动作。设时间间隔为 `dt`：

```text
vx = (x_next - x) / dt
vy = (y_next - y) / dt
vz = (z_next - z) / dt
yaw_rate = wrap_angle(yaw_next - yaw) / dt
```

其中 `wrap_angle` 将角度差限制到 `[-pi, pi]`，避免跨越 `pi/-pi` 时出现错误的大角速度。

在 TravelUAV raw episode 中，图像帧通常按 `000000.png`、`000005.png`、`000010.png` 对齐保存，因此 `dt` 不应简单固定为 1 秒。当前工程实现优先使用 `sensors.state.timestamp` 计算相邻 image-aligned 帧的真实时间差，并将该值写入 JSONL 的 `dt` 字段。

## OpenVLA-OFT Cross-Embodiment Transfer

OpenVLA-OFT 面向机器人操作任务，已经包含视觉语言编码、proprio/state 输入、action chunk 和 continuous action head 等结构。UAV 与机械臂的传感状态和动作语义不同，因此不能直接使用原始 LIBERO action 格式。

本文的迁移思路是：

- 保留 OpenVLA-OFT 的视觉语言表示和 action chunk 训练思想。
- 将 UAV 状态 `[x,y,z,yaw]` 接入 proprio/state projector。
- 将机器人连续动作头改造为 UAV 连续动作 `[vx,vy,vz,yaw_rate]`。
- 先构建 TravelUAV -> OpenVLA-OFT-style JSONL 数据通路，再进入大规模训练。

## Diffusion Policy Module

Diffusion Policy 用作后续底层控制序列生成模块。它可以在 VLA 高层语义条件、当前状态和历史观测条件下生成一段连续控制序列，使 UAV 动作更加平滑，并适合开放环 action chunk 执行。

当前阶段只预留 `diffusion/` 模块，不训练 Diffusion Policy。

## RL Expert Trajectory Generation

强化学习用于后续专家轨迹生成。RL agent 可在 TravelUAV/AirSim 仿真环境中学习到达目标、避障和稳定控制策略，生成可供 VLA 或 Diffusion Policy 学习的 expert trajectories。

当前阶段只预留 `rl/` 模块，不训练 RL。

## Current Experimental Goal

当前第一阶段实验目标不是最终模型效果，而是验证：

- TravelUAV 数据结构是否可解析。
- `state=[x,y,z,yaw]` 是否能稳定得到。
- `action=[vx,vy,vz,yaw_rate]` 是否能由相邻轨迹点计算。
- `action_chunk` 是否能按 OpenVLA-OFT 思路生成。
- `traveluav_debug.jsonl` 是否能通过格式检查。

本阶段不训练模型、不加载大模型、不运行 LoRA/OFT、不跑闭环仿真。
