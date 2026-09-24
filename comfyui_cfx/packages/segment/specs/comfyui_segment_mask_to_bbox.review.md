# Adversarial Review: comfyui_segment_mask_to_bbox

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 2D `[H,W]` 提升为 batch=1，有测试。
- §8.2 空项不产条目 + `0 box(es)` summary，有测试。
- §8.3 向外对齐后夹取到图像范围（`multiple_of` > 边长），有测试。
- §8.4 严格 `>` 阈值，等于阈值的像素被排除，有测试。
- §8.5 多 batch 项 → 两条目且按索引排序，有测试。
- 纯几何 helper 与节点分离：helper 只吃 numpy，节点负责 MASK→numpy 与 summary。
- 与 `annotations_to_mask`（`boxes_to_mask`）语义互逆，未复制 GPL 代码；essentials 仅行为参考（MIT）。

## 未决疑点
1. `area` 定义为对齐并夹取后的**盒子面积**（非掩码像素数）；若下游需要像素数可另加字段。
2. helper 要求 `[B,H,W]`；2D 输入由节点负责提升，helper 直接调用需自行加 batch 维。
