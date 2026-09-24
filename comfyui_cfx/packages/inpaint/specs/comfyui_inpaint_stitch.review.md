# Adversarial Review: comfyui_inpaint_stitch

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 往返：直接赋值覆盖目标矩形，矩形外保持整图，有测试。
- §8.2 越界矩形：`x0/y0` 取 `max(0, …)`、`x1/y1` 取 `min(size, …)`，并按偏移裁剪 patch，避免错位写入。
- §8.3 空矩形：clamp 后 `x1<=x0 or y1<=y0` 提前返回克隆整图。
- §8.4 尺寸不符：patch 空间维与 `crop_data` 不一致时 `ValueError`，无隐式 resize。
- §8.5 缺键：逐键检查并抛 `ValueError`。
- §8.6 原始尺寸不符：`original_width/height` 与整图不符时 `ValueError`。
- §8.7 mask：`clamp(0,1)` + 广播为 `[1,h,w,1]`，结果等价 `base*(1-m)+patch*m`，有测试。
- 副作用：`base.clone()` 后写入，输入张量不被修改。
- `ensure_image` 统一 3D/4D/BCHW，返回 shape 与输入整图一致。

## 未决疑点
1. patch 与整图 batch 不同时依赖广播（patch batch 为 1 或相等）；非 1 且不等由 torch 抛错。
2. `mask` 同时接受 patch 尺寸与整图尺寸；两者都匹配时优先整图尺寸。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 原样 stitch | 矩形外相等 | PASS |
| 越界矩形 | clamp 不越界 | PASS |
| 空矩形 | 原样返回 | PASS |
| patch 尺寸不符 | ValueError | PASS |
| 缺键 | ValueError | PASS |
| 原始尺寸不符 | ValueError | PASS |
| mask 混合 | 加权且 clamp | PASS |
