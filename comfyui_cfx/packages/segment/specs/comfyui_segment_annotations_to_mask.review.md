# Adversarial Review: comfyui_segment_annotations_to_mask

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 反向框自动归一，有测试。
- §8.2 点数不足跳过，有测试。
- §8.3 尺寸 clamp 到 ≥1。
- §8.4 无 bbox/polygon 报错，有测试。
- 行为重写（rmbg 对应节点为 GPL），未复制代码。

## 未决疑点
1. 坐标假定为像素绝对坐标（Florence-2 post_process 已按 image_size 反量化）。
2. 仅支持 dict 输入；如需列表输入可后续加 adapter。
