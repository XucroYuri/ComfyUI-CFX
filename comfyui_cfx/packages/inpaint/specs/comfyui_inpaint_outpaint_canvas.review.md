# Adversarial Review: comfyui_inpaint_outpaint_canvas

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 四边全 0：`(left, right, top, bottom) == (0, 0, 0, 0)` 提前返回归一化输入，不重建画布。
- §8.2 单边扩展：画布按 `(H+top+bottom, W+left+right)` 构造，`fill` 覆盖整块，仅新增边框保持 `fill`。
- §8.3 batch：`canvas` 保留 `img` 的 batch 维，`image` 整体贴到 `(left, top)`。
- §8.4 `mask` 为 `[H,W]`：先 `dim()==2` 保持，clamp 后 `unsqueeze(0)` 成 `[1,H,W]`，写入原图区域。
- §8.5 尺寸不符：空间维与 `image` 不一致时报 `ValueError`，不依赖 torch 广播静默处理。
- §8.6 `fill` 边界：`torch.full` 用 `fill` 精确填充，边框像素等于 `0.0`/`1.0`。
- mask 语义：`out_mask` 先置 `1.0`，再把输入掩码写回原图区域，边框为 `1.0`。
- 副作用：新分配 `canvas`/`out_mask`，不修改输入张量。
- 输出 dtype/device/channels 与 `image` 一致（`ensure_image` 为 float32）。

## 未决疑点
1. 掩码只取首个 batch 项，与 `crop_by_mask`/`stitch` 的约定一致；多 batch 掩码的其余项被忽略。
2. 仅当边距非全 0 时才校验掩码空间维；全 0 时原样返回，保持与“unchanged”语义一致。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 四边全 0 | 原样返回 | PASS |
| 单边扩展 | 仅该边为 fill | PASS |
| 多 batch 图像 | batch 保留 | PASS |
| mask `[H,W]` | 归一写入 | PASS |
| mask 尺寸不符 | ValueError | PASS |
| fill 边界 0/1 | 精确填充 | PASS |
