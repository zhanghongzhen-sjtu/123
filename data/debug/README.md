# Debug Data

`traveluav_debug.jsonl` 是 toy debug 数据，仅用于测试 JSONL 格式，不可作为论文实验数据。

以下文件来自本地已下载的 TravelUAV 3 个 raw 地图子集，可用于真实数据转换流程验证，但仍不是完整实验训练集：

- `traveluav_BrushifyCountryRoads_debug.jsonl`
- `traveluav_BrushifyUrban_debug.jsonl`
- `traveluav_Carla_Town02_debug.jsonl`
- `traveluav_3maps_debug.jsonl`

这些真实 debug JSONL 使用 `sensors.state.timestamp` 自动计算 image-aligned 相邻帧的 `dt`。
