# Adversarial Review: comfyui_video_pad_frames

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 `repeat_last` 补帧实现为 `torch.cat([img[-1:]] * missing)`，有测试断言补出帧逐元素等于 `img[-1]`。
- §8.2 `loop` 用 `img[:take]` 切片循环，`take = min(B, missing - taken)`；测试断言帧序 `[0,1,2,0,1,2,0,1]`。
- §8.3/§8.4 `B >= count` 提前返回 `img`，既不补也不截断，测试覆盖 `count == B` 与 `count < B`。
- §8.5 测试逐元素比对输出前 `B` 帧与输入相等，原帧未被改写；输入张量本身未被原地修改。
- §8.6 `while` 循环保证 `loop` 在 `count` 远大于 `B` 时仍恰好补满，不产生缺帧。
- 输出经 `contiguous()`，测试断言 `is_contiguous()`，shape 恒为 `[count, H, W, C]`。
- 空批次显式 `ValueError`，未知 `mode` 显式 `ValueError`，不静默降级。

## 未决疑点
1. `count <= 0` 由 widget 约束在 1..100000；直接调用传入 `count <= 0` 时 `B >= count` 恒真，原样返回，不做额外校验。
