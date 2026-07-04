# When To Use 5090

## Local RTX 3060 Only

本地 3060 只做：

- 克隆项目。
- 阅读代码。
- 分析数据结构。
- 写数据转换脚本。
- 写 UAV action adapter。
- 生成少量 debug JSONL。
- 检查数据格式。
- 写论文方法文档。
- 只下载少量 TravelUAV 地图子集并做真实数据 debug 转换验证。
- 固定 UAV JSONL debug schema。
- 计算少量 debug JSONL 的 state/action 统计。
- 编写 OpenVLA-OFT UAV 接入计划。
- 做不加载权重的 dataset-loader smoke test。
- 读取 debug JSONL 并检查 image path、state/action、action chunk 和 normalization config。
- 做 CPU-only OpenVLA-OFT-style collator/batch shape 空跑。
- 检查 OpenVLA-OFT UAV pseudo config，确认训练和模型加载开关关闭。
- 生成 5090 交接计划和轻量 manifest 预览。

## AutoDL RTX 5090

AutoDL RTX 5090 用于：

- 加载 OpenVLA-OFT / openvla-7b。
- 训练 UAV action head。
- LoRA / OFT 微调。
- 大规模 TravelUAV 数据处理。
- 完整 train/val split 的转换、重统计和训练前数据整理。
- 闭环仿真评估。
- Diffusion Policy 训练。
- 强化学习训练。

## Current 3-Map Run

本次只下载并解压 3 个地图：`BrushifyCountryRoads`、`BrushifyUrban`、`Carla_Town02`，并生成少量 debug JSONL。这一步不需要 5090，也没有加载任何 OpenVLA / OpenVLA-OFT / openvla-7b 权重。

已完成的 schema 固定、三地图统计和 OpenVLA-OFT UAV 改造计划也都属于本地轻量工程范围，不需要 5090。

已完成 CPU-only dataset loader smoke test：

- `scripts/run_smoke_dataset_loader.sh`
- `SMOKE_PASS: UAV JSONL dataset loader works without model loading.`

已完成 CPU-only OpenVLA-OFT UAV adapter smoke test：

- `scripts/run_smoke_openvla_oft_adapter.sh`
- `ADAPTER_SMOKE_PASS: OpenVLA-OFT UAV adapter batch contract is valid without model loading.`

已完成 pseudo config 检查：

- `configs/openvla_oft_uav_debug.yaml`
- `scripts/run_check_pseudo_config.sh`
- `PSEUDO_CONFIG_PASS: local OpenVLA-OFT UAV pseudo config is valid and training remains disabled.`

已完成 5090 handoff 预览：

- `configs/autodl_5090_paths.yaml`
- `docs/autodl_5090_handoff_plan.md`
- `docs/autodl_5090_handoff_manifest.md`
- `scripts/package_handoff_preview.sh`
- `HANDOFF_PREVIEW_PASS`

## When Full Data Starts

全量数据不是一开始就上 5090，也不是现在直接训练。推荐边界如下：

- 本地可以继续做少量样本调试、schema 检查、可视化、adapter 空跑。
- 如果只是下载/解压少数地图，且磁盘足够，可以本地做。
- 一旦准备完整 train/val split、全量转换、全量 normalization stats，建议切到 5090 服务器或至少在 5090 训练环境同一存储下处理。
- 一旦需要加载 OpenVLA-OFT / openvla-7b、训练 action head、LoRA/OFT、闭环仿真、Diffusion Policy 或 RL，必须使用 5090。

原因：全量转换和统计本身可能不一定吃 GPU，但它们必须和训练 split、训练路径、归一化配置完全一致；放到 5090 阶段能减少本地 3060 的 IO/磁盘压力，也避免本地生成一套和训练环境不一致的数据。

当前 handoff manifest 只列轻量工程文件、小 debug JSONL、小统计和文档，不包含 `data/raw/`、`external/`、`.venv/`、`logs/`、`work/` 或任何模型权重。

当前统计产物：

- `data/debug/traveluav_3maps_stats.json`
- `docs/traveluav_3maps_stats.md`

注意：这些统计只来自 3-map debug subset，不能作为最终训练归一化统计。完整训练 split 的统计和模型训练应放到 5090 阶段。

## Stop Marker

如果本地阶段遇到上述任务，应停止执行并明确写：

```text
NEED_5090: 当前任务需要 AutoDL RTX 5090，不应在本地 3060 执行。
```
