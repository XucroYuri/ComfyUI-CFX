# Adversarial Review: comfyui_segment_text_to_mask

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §7 空框不抛错：有 `test_empty_detections_give_zero_mask`，且断言 `segment` 未被调用。
- 检测复用 `CFXGroundingDinoDetect`，未复制推理逻辑（无重复模型加载/缓存）。
- SAM2 路径经 `annotations_to_box_batch` 统一批次形状，`test_sam2_path_uses_box_batch` 断言实参。
- `detections` 原样透传，测试以 `is` 断言同一对象。
- 回退路径形状由 `ensure_image` 推导，`test_fallback_boxes_to_mask` 断言 `(1,H,W)` 与填充位置。

## 未决疑点
1. 仅暴露框提示 SAM2；点/掩码提示不在本节点（沿用上游能力边界）。
2. 真实推理未在 CI 覆盖（需权重），人工 VERIFY。
3. 检测异常（依赖缺失）直接透传，未包装为自定义错误（符合「fail loudly」）。
