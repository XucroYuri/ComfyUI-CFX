# Adversarial Review: comfyui_inpaint_crop_by_mask

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 padding 越界：先对齐再 clamp，`max(x0+1, min(x1, width))` 保证 ≥1px。
- §8.2 掩码贴边：对齐上取整后仍被图像边界截断，有测试。
- §8.3 `multiple_of` 过大：clamp 收缩到整图且不为空。
- §8.4 全空掩码：`torch.any` 判空后 `ValueError("crop_by_mask: mask is empty")`，有测试。
- §8.5 `[B,H,W]`：取第一项并升维回 `[1,H,W]`。
- `crop_data` 的 `width/height` 与返回张量空间维一致；无副作用。

## 未决疑点
1. 掩码与图像分辨率不一致时未显式校验，依赖索引 clamp；后续 stitch 节点需复用 `original_width/height`。
2. 多 batch 图像仅处理第一项，批量语义留给后续节点。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| padding 越界 | clamp | PASS |
| 掩码贴边 | 不越界 | PASS |
| multiple_of 过大 | ≥1px | PASS |
| 全空掩码 | ValueError | PASS |
| [B,H,W] | 取首项 | PASS |
