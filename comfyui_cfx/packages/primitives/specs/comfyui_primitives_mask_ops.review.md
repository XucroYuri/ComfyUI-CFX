# Adversarial Review: comfyui_primitives_mask_ops

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §8.4 环形掩码 `fill_holes` 后中心填充为 1，有测试。
- §8.5 二维输入自动升维。
- §2 顺序固定且文档化；`grow`/`shrink` 同时给定时按顺序执行。
- §8.3 `blur` 大半径用 `reflect` padding，不越界。
- 输出 clamp 到 [0,1]。
- 不改动输入张量（`fill_holes` 用副本）。

## 未决疑点
1. `fill_holes` 以 0.5 为阈值判定前景；对软掩码可能不理想，已在文档说明用于二值语义。
2. `grow`/`shrink` 多次交替的质量问题不在范围内（应串多个节点）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 全 0 / 全 1 | 稳定 | PASS |
| grow+shrink 同给 | 顺序执行 | PASS |
| blur 半径 > 图 | 不越界 | PASS |
| 环形 fill | 中心=1 | PASS |
| 2D 输入 | 升维 | PASS |
