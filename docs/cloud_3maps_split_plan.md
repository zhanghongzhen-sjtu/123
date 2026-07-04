# Cloud 3-Map Split Plan

当前阶段只用于 3-map pilot / sanity experiment，不作为正式论文最终训练集。

## Maps

- BrushifyCountryRoads
- BrushifyUrban
- Carla_Town02

## Proposed Pilot Split

建议：

- train: BrushifyCountryRoads + BrushifyUrban
- val: Carla_Town02

原因：

- train 使用两个风格不同地图；
- val 留出 Carla_Town02 作为未见地图验证；
- 该 split 只用于小规模 sanity training / overfit test / adapter debugging；
- 不能作为最终 OpenVLA-OFT 迁移实验结论。

## Not Training-Ready Notes

三地图 pilot 可以验证：

- JSONL 转换
- image/instruction/state/action/action_chunk 格式
- action head 维度
- dataloader/collator
- loss 是否能正常下降

不能证明：

- 泛化能力
- 完整 TravelUAV 性能
- OpenVLA-OFT 迁移最终效果
- Diffusion Policy/RL 最终闭环能力

## Next

1. 统计每个地图 episode 数量。
2. 生成 pilot train/val JSONL。
3. 计算 pilot train stats。
4. 跑 train/val validation。
5. 跑 dataset loader/collator smoke。
6. 只在全部通过后，再考虑极小规模 smoke training。
