# Adversarial Review: comfyui_segment_sam2_auto_mask

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2/§7 句柄 `segmentor != 'automaskgenerator'` 在调用后端前抛 `ValueError`，消息点名
  所需 loader 设置，有测试断言未触碰 `auto_mask`。
- §2 上游 `segment` 无默认值：适配层 `_AUTO_MASK_DEFAULTS` 补齐未暴露参数，
  节点仅暴露 3 个调节项，职责边界清晰。
- §2 预览图刻意丢弃（`_preview`），在 spec 与本文件说明理由。
- §3 返回 `(MASK, JSON)`，`bboxes` 透传上游 `item['bbox']` 列表。
- `keep_model_loaded` 与调节项透传上游，不自行管理显存（有测试）。
- 行为重写（上游 Apache-2.0 复用，未复制 GPL 代码）。

## 未决疑点
1. 未暴露全部上游调节项（crop/NMS/use_m2m 等），按需再开。
2. 真实推理未在 CI 覆盖（需权重），人工 VERIFY。
