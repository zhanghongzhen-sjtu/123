# Baseline Notes

## UAV-VLA

UAV-VLA 可作为前期复现 baseline，用于说明 VLM/LLM + 航迹规划可以生成任务理解、目标描述和路径规划结果。它的价值在于帮助建立 UAV 视觉语言导航问题背景，但不直接等价于本项目的 OpenVLA-OFT 跨形态迁移路线。

## UAV-VLPA*

UAV-VLPA* 可作为路径规划类 baseline，用于理解 TSP、A*、路径规划和可视化流程。它更偏向规划算法和可解释路径生成，不是端到端 VLA 连续动作学习方法。

## TravelUAV

TravelUAV 是主 UAV 仿真数据来源，包含 UAV VLN 任务、AirSim/Unreal 环境、地图划分、轨迹和语言指令相关数据。相比普通 UAV 检测或分类数据集，TravelUAV 更贴近本论文的输入输出形式：图像、自然语言指令、状态/轨迹和导航目标。

## OpenVLA-OFT

OpenVLA-OFT 是机器人 VLA 底座模型与 fine-tuning 框架参考。它包含连续 action head、action chunk、proprio/state projector 和 LIBERO/ALOHA 等机器人任务的数据处理方式。本项目重点不是直接复现 LIBERO，而是把这种机器人 VLA 结构迁移到 UAV 仿真导航。

## AeroVLA

AeroVLA 是重要参考项目，展示了 TravelUAV 上端到端 UAV VLA 的数据组织和闭环评估方式。但本项目不是简单复现 AeroVLA，而是围绕 OpenVLA-OFT 的机器人 VLA 到 UAV 连续动作空间迁移，重点建设 TravelUAV -> OpenVLA-OFT 数据通路和 UAV action adapter。
