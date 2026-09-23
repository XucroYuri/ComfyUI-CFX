# Adversarial Review: comfyui_primitives_image_split

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- `OUTPUT_IS_LIST` 正确声明；返回形态为 `([...],)`。
- 顺序与 batch 一致，有测试。
- 每项 `[1,H,W,C]` 且 contiguous。

## 未决疑点
1. 大量项（B 很大）会生成许多小张量，属 ComfyUI 列表语义固有成本。
