# Adversarial Review: comfyui_primitives_image_stitch

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §8.2 单路透传，无多余拷贝语义变化。
- §7 尺寸不匹配（高/宽/batch/通道）逐项 `ValueError`，有测试。
- §8.4 `spacing` 后总尺寸 = 各部分之和 + 间距。
- 未连接槽按 `is not None` 跳过。

## 未决疑点
1. 不同尺寸是否自动 resize/pad？刻意不做，避免隐式质量变化；由 `image_resize`/`pad` 显式处理。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 未连接槽 | 跳过 | PASS |
| 单路 | 透传 | PASS |
| 高度不匹配（横向） | 报错 | PASS |
| spacing | 尺寸正确 | PASS |
