# Adversarial Review: comfyui_primitives_resolution

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §8.1 极小 megapixels 不产生 0px（`_align` clamp）。
- §8.2 单侧覆盖按比例推导，有测试。
- §8.3 portrait 交换长短边，有测试。
- **不输出 LATENT**：避免猜测模型通道数导致错误 latent，符合"宁可少做不做错"。

## 未决疑点
1. 比例集合为内置常量；如需扩展，走版本化新增而非改语义。
2. 与 `ComfyUI-Resolve`（P1）的边界：本节点是纯计算，端到端放大/重采样归 Resolve。
