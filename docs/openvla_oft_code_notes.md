# OpenVLA-OFT Code Notes

## Main Structure

- `README.md`: 项目概览、推理示例和显存要求。
- `SETUP.md`: conda、PyTorch、Flash Attention 和 editable install 说明。
- `LIBERO.md`: LIBERO 评估和 fine-tuning 命令。
- `vla-scripts/finetune.py`: LoRA/OFT fine-tuning 主入口。
- `experiments/robot/libero/run_libero_eval.py`: LIBERO 闭环评估入口。
- `experiments/robot/openvla_utils.py`: 加载 VLA、processor、action head、proprio projector、noisy action projector 的工具。
- `prismatic/models/action_heads.py`: L1 regression action head 和 diffusion action head。
- `prismatic/models/projectors.py`: proprio projector 和 noisy action projector。
- `prismatic/vla/constants.py`: action chunk、action dim、proprio dim 等常量。
- `prismatic/vla/datasets/`: RLDS / OXE 数据加载、action/proprio 标准化和 batch transform。

## Training Entry

训练入口主要是 `vla-scripts/finetune.py`。该脚本会加载 `openvla/openvla-7b` 或本地 checkpoint，构建 LoRA、action head、proprio projector、RLDS dataset 和 DDP 训练流程。该入口不能在本地 3060 上运行。

## Inference Entry

推理和评估入口主要是 `experiments/robot/libero/run_libero_eval.py`，并通过 `experiments/robot/openvla_utils.py` 加载模型和组件。README 的 quick start 也会调用 `get_vla()`、`get_processor()`、`get_action_head()` 和 `get_proprio_projector()`，这些都会触发模型或 checkpoint 加载。

## Action Head

`prismatic/models/action_heads.py` 包含：

- `L1RegressionActionHead`: 从 action token hidden states 回归连续动作。
- `DiffusionActionHead`: 使用 DDIM scheduler，对动作序列做条件扩散建模。

两者当前默认依赖 `ACTION_DIM` 和 `NUM_ACTIONS_CHUNK`。LIBERO 默认是 `ACTION_DIM=7`，`NUM_ACTIONS_CHUNK=8`。

## Action Chunk Constants

`prismatic/vla/constants.py` 中定义平台常量：

- LIBERO: `NUM_ACTIONS_CHUNK=8`, `ACTION_DIM=7`, `PROPRIO_DIM=8`
- ALOHA: `NUM_ACTIONS_CHUNK=25`, `ACTION_DIM=14`, `PROPRIO_DIM=14`
- BRIDGE: `NUM_ACTIONS_CHUNK=5`, `ACTION_DIM=7`, `PROPRIO_DIM=7`

后续 UAV 应新增或改造为 `ACTION_DIM=4`，`PROPRIO_DIM=4`，`NUM_ACTIONS_CHUNK` 可先保持 8。

## Proprio/State Projector

`prismatic/models/projectors.py` 中的 `ProprioProjector` 把 proprio state 映射到 LLM embedding 空间。`modeling_prismatic.py` 中 `_process_proprio_features()` 会把 proprio token append 到视觉 patch embedding 后面。

UAV state 接入时，可能需要：

- 修改 `prismatic/vla/constants.py` 中平台检测和 `PROPRIO_DIM`。
- 在训练数据 transform 中把 UAV `state=[x,y,z,yaw]` 写入 observation/proprio。
- 初始化 `ProprioProjector(llm_dim, proprio_dim=4)`。

## LIBERO Data and Action Format

OpenVLA-OFT 的 LIBERO 管线使用 RLDS 数据集。batch 中包含 `pixel_values`、`input_ids`、`attention_mask`、`labels`、`actions` 和可选 `proprio`。collator 会 stack `actions`，并在 `use_proprio=True` 时 stack `proprio`。

LIBERO action 默认是 7 维机器人动作，UAV 不能直接沿用，需要改为 4 维 `[vx,vy,vz,yaw_rate]`。

## UAV Adaptation Points

- `prismatic/vla/constants.py`: 增加 UAV 平台常量，设置 action/proprio 维度。
- `prismatic/models/action_heads.py`: 确认 action head 使用 `ACTION_DIM=4` 后 shape 正确。
- `prismatic/models/projectors.py`: 使用 4 维 state projector。
- `prismatic/vla/datasets/`: 后续需要把 JSONL 或真实 TravelUAV 数据转为 OpenVLA-OFT 可训练数据格式，可能需要新增 dataset adapter。
- `vla-scripts/finetune.py`: 后续训练 UAV action head / LoRA / OFT 时修改 dataset_name、data_root、num_images、use_proprio 等参数。

## Must Use 5090

以下操作必须放到 AutoDL RTX 5090 或更合适的远端 GPU：

- 加载 `openvla-7b` 或 OpenVLA-OFT checkpoint。
- 运行 `experiments/robot/libero/run_libero_eval.py` 或类似闭环评估。
- 运行 `vla-scripts/finetune.py`。
- 训练 UAV continuous action head。
- LoRA / OFT 微调。
- 使用 Diffusion action head 训练。
- 大规模 TravelUAV 数据转换和训练集统计。
