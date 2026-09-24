# Adversarial Review: comfyui_video_frame_range

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 中间切片 `[2:6]` 有测试，返回帧数与内容正确。
- §8.4 `stop > B` 夹取到 B，无越界；`stop=-1` 到结尾，有测试。
- §8.5 `start >= stop` 显式抛 `ValueError`，不静默返回空批次。
- 输出经 `ensure_image` 归一，shape 恒为 `[B', H, W, C]`。

## 未决疑点
1. `step` 由 widget 约束在 1..1000；直接调用传入 `step<=0` 属未定义（Python 切片语义），不额外校验。
