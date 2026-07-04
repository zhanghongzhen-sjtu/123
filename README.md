# vla-uav-diffusion

论文方向暂定为：**基于 OpenVLA-OFT 迁移的无人机仿真视觉语言动作导航方法研究**，或 **面向无人机仿真导航的机器人 VLA 跨形态迁移方法研究**。

当前阶段只做轻量工程搭建，不训练模型，不加载 OpenVLA / OpenVLA-OFT / openvla-7b 权重，不运行 LoRA / OFT 微调，不跑闭环仿真。

## Current Stage

- 搭建项目结构。
- 分析 TravelUAV、AeroVLA、OpenVLA-OFT 的代码和数据入口。
- 定义 UAV state/action adapter。
- 生成 TravelUAV -> OpenVLA-OFT-style JSONL 的 debug 转换脚本。
- 生成 `check_uav_jsonl.py` 数据格式检查脚本。
- 写论文方法相关工程文档。

## 3-Map Real Data Validation

已在本地只下载并解压 3 个 TravelUAV 地图子集：`BrushifyCountryRoads`、`BrushifyUrban`、`Carla_Town02`。

下载位置：`data/raw/TravelUAV/_downloads/`

解压位置：`data/raw/TravelUAV/`

本次子集为 raw episode 结构，包含 `log/*.json`、`frontcamera/*.png`、`object_description.json`、`mark.json`，未预生成 `merged_data.json`。转换脚本已支持直接从 raw episode 生成真实 debug JSONL。

已生成：

- `data/debug/traveluav_BrushifyCountryRoads_debug.jsonl`，60 行
- `data/debug/traveluav_BrushifyUrban_debug.jsonl`，60 行
- `data/debug/traveluav_Carla_Town02_debug.jsonl`，54 行
- `data/debug/traveluav_3maps_debug.jsonl`，60 行，每个地图最多 20 行

四个 JSONL 均通过 `check_uav_jsonl.py`，并额外用 `--image-root .` 验证了 image 路径存在。

已完成 dt 校准：raw episode 转换现在优先使用 `sensors.state.timestamp` 计算相邻 image-aligned 帧的真实时间间隔。三地图审计报告显示 `dt` 均来自 timestamp，均值约 4.97 秒，frame delta 为 5。审计报告：

- `docs/traveluav_3maps_audit.md`
- `docs/traveluav_3maps_debug_audit.md`

当前 JSONL schema 已固定为 `uav_openvla_jsonl_v0.1`，见：

- `docs/uav_jsonl_schema.md`

已生成三地图小样本统计，用于后续归一化接口规划，但不可作为完整训练集统计：

- `data/debug/traveluav_3maps_stats.json`
- `docs/traveluav_3maps_stats.md`

后续 OpenVLA-OFT UAV 接入计划见：

- `docs/openvla_oft_uav_modification_plan.md`

已完成 CPU-only dataset loader smoke test，用于验证未来 OpenVLA-OFT dataset reader 的输入接口，不加载模型权重：

- `src/openvla_uav_transfer/datasets/uav_jsonl_dataset.py`
- `src/openvla_uav_transfer/checks/smoke_uav_dataset_loader.py`
- `docs/uav_dataset_loader_notes.md`

已完成 CPU-only OpenVLA-OFT UAV adapter/collator 空跑：

- `src/openvla_uav_transfer/datasets/uav_collator.py`
- `src/openvla_uav_transfer/checks/smoke_openvla_oft_adapter.py`
- `docs/openvla_oft_dataset_adapter_design.md`
- `docs/openvla_oft_adapter_smoke_report.md`

已固定 OpenVLA-OFT UAV pseudo config，用于记录未来 5090 阶段训练前需要的路径、维度、chunk size、normalization 和安全边界：

- `configs/openvla_oft_uav_debug.yaml`
- `src/openvla_uav_transfer/checks/check_pseudo_config.py`
- `docs/openvla_oft_uav_pseudo_config.md`
- `docs/openvla_oft_uav_pseudo_config_check_report.md`

已生成 AutoDL RTX 5090 交接计划和轻量交接 manifest 预览：

- `configs/autodl_5090_paths.yaml`
- `docs/autodl_5090_handoff_plan.md`
- `docs/autodl_5090_handoff_manifest.md`
- `scripts/package_handoff_preview.sh`

## Local RTX 3060 Scope

本地 3060 只用于轻量任务：克隆项目、阅读代码、分析数据结构、写转换脚本、生成少量 debug JSONL、检查数据格式和写文档。

## AutoDL RTX 5090 Scope

以下任务应放到 AutoDL RTX 5090：加载 OpenVLA-OFT / openvla-7b，训练 UAV action head，LoRA / OFT 微调，大规模 TravelUAV 数据处理，闭环仿真评估，Diffusion Policy 训练，强化学习训练。

如果下一步需要这些任务，应停止本地执行并标记：

```text
NEED_5090: 当前任务需要 AutoDL RTX 5090，不应在本地 3060 执行。
```

## Quick Run

WSL 推荐路径：

```bash
cd /mnt/d/中期/vla-uav-diffusion
bash scripts/run_inspect_traveluav.sh
bash scripts/run_convert_debug.sh
bash scripts/run_check_debug.sh
bash scripts/run_compute_3maps_stats.sh
bash scripts/run_smoke_dataset_loader.sh
bash scripts/run_smoke_openvla_oft_adapter.sh
bash scripts/run_check_pseudo_config.sh
bash scripts/package_handoff_preview.sh
```

Windows PowerShell 路径：

```powershell
cd D:\中期\vla-uav-diffusion
wsl -e bash scripts/run_inspect_traveluav.sh
wsl -e bash scripts/run_convert_debug.sh
wsl -e bash scripts/run_check_debug.sh
wsl -e bash scripts/run_compute_3maps_stats.sh
wsl -e bash scripts/run_smoke_dataset_loader.sh
wsl -e bash scripts/run_smoke_openvla_oft_adapter.sh
wsl -e bash scripts/run_check_pseudo_config.sh
wsl -e bash scripts/package_handoff_preview.sh
```

如果当前没有真实 TravelUAV `dataset_raw`，转换脚本会生成 toy debug 文件 `data/debug/traveluav_debug.jsonl`，仅用于格式测试，不可作为论文实验数据。

真实数据放置位置：

- 推荐：`data/raw/TravelUAV`
- 或：`external/TravelUAV/dataset_raw`

## Lightweight Dependencies

`requirements.txt` 只包含轻量依赖：

```text
numpy
pandas
tqdm
pyyaml
pillow
jsonlines
```

当前阶段不要安装 torch、transformers、CUDA 训练依赖或大模型依赖。
