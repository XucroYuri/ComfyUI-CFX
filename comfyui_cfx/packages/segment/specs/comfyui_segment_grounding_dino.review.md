# Adversarial Review: comfyui_segment_grounding_dino

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- **统一路径**：文本检测收敛到 transformers，弃 `groundingdino-py` 与 vendored fork（三套→一套）。
- **无 remote code**（符合 ADR-0002）。
- §8.1 无检测时返回空 bboxes 与全 0 mask，不报错。
- 行为重写，未复制 GPL 插件代码。

## 未决疑点
1. fp32 固定：未提供精度开关，GroundingDINO 半精度易退化，暂不做半精度。
2. 真实推理未在 CI 覆盖（需权重），标记人工 VERIFY。
3. 与 `ComfyUI-Segment`（P1 规划）的 SAM 掩码阶段尚未实现；本节点只到框 + 框掩码。
