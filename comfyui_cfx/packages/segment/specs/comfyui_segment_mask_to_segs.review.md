# Adversarial Review: comfyui_segment_mask_to_segs

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 全空 MASK → `[]`，有测试。
- §8.2 单图 + 多 MASK 项 → 图像广播，每项一条，有测试。
- §8.3 贴边 mask → bbox 夹取到图像范围，裁剪不越界（复用 `mask_to_bboxes` 的夹取），有测试覆盖。
- §8.4 严格 `>` 阈值来自 helper，恰好 0.5 的像素不产生条目。
- §8.5 多 MASK 项按 batch 顺序产生多条 SEGS，有测试。
- 结构与 dtype/shape 断言覆盖全部键：`cropped_image`/`cropped_mask` 为 float32 张量，
  `crop_region`/`bbox` 为 `(x0, y0, x1, y1)` 元组，`control_net_wrapper` 为 `None`，有测试。
- **许可**：不导入 impact-pack（GPL-3.0），不复制其代码，仅按公开数据格式构造 `SEGS`；
  `SEGS` 以字符串类型登记，无需 GPL 依赖即可与下游按类型名互通。

## 未决疑点
1. `cropped_image` 的通道数随输入 IMAGE（通常 3）；公开格式示例为 `[h,w,3]`，未强制归一为 3 通道。
2. IMAGE 与 MASK 批次不匹配且 IMAGE 批次非 1 时按下标取图，越界即 `IndexError`（有意 fail loudly）。
