# Adversarial Review: comfyui_segment_sam2_points

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §7 正点为空抛 `ValueError`，有测试。
- §7 非法 JSON / 形状 / 缺键均归一为 `ValueError`，有参数化测试。
- §8.3 无负点 → `negative=None`，有测试断言后端仅收到正点 JSON。
- §8.4 负点归一后透传，有测试。
- 点解析为纯函数，可离线测试；后端经 `backend.segment_points` 调用，无需模型即可测。
- 行为重写（上游 Apache-2.0 复用，未复制 GPL 代码）。

## 未决疑点
1. 点坐标为像素绝对坐标，范围由用户/上游保证。
2. 仅支持点提示；掩码提示（`mask`）未暴露。
3. 真实推理未在 CI 覆盖（需权重），人工 VERIFY。
