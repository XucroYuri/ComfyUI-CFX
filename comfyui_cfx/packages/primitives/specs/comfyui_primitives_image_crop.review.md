# Adversarial Review: comfyui_primitives_image_crop

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §8.1 越界 clamp：`x/y` 超出后停在 `in_w-1/in_h-1`，有测试。
- §8.2 inset 过大：`max(x0+1, …)` / `max(y0+1, …)` 保证至少 1px。
- §8.3 零尺寸：`width/height=0` 取到边缘。
- §8.4 percent：按边长换算。
- 无副作用；输出 contiguous。

## 未决疑点
1. 是否需要在裁剪后联动 mask（当前仅 IMAGE）；mask 由 `mask_ops`/专用节点处理。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| x/y 超界 | clamp | PASS |
| inset 过大 | ≥1px | PASS |
| 0 尺寸 | 到边缘 | PASS |
| percent | 正确换算 | PASS |
