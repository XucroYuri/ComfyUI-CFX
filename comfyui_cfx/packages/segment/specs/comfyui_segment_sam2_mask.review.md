# Adversarial Review: comfyui_segment_sam2_mask

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §7 缺 `bboxes` 抛 `ValueError`，有测试（`annotations_to_box_batch`）。
- 批次形状转换集中在 `geometry.annotations_to_box_batch`，可离线测试。
- `keep_model_loaded` 透传上游，不自行管理显存（职责边界清晰）。

## 未决疑点
1. 仅支持框提示；点提示/掩码提示未暴露（上游支持，后续按需加）。
2. 多边形标注未转换为点序列（上游无多边形输入）。
3. 真实推理未在 CI 覆盖（需权重），人工 VERIFY。
