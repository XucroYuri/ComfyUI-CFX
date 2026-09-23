# Adversarial Review: comfyui_primitives_image_resize

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §7.1 数值：`stretch/crop/pad` 形状与语义断言通过（见单测）。
- §2 尺寸推导优先级：`scale_by > target_megapixels > (width,height)`，单边推导按比例。
- §2 对齐：`multiple_of` 生效，且 `max(multiple_of, ...)` 防止 0px。
- §8.1 无尺寸来源：抛出 `ValueError`，有测试。
- §8.4 `multiple_of` 大于边长：`max()` 保证不低于 `multiple_of`。
- §6 无副作用：不写文件、无网络、无全局状态。
- 许可：实现为本仓原创（行为参考 WAS/easy-use 等，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. 下采样质量：当前统一 `bicubic`；下采样用 `area` 可能更优，待基准测量后决定是否按方向自动切换。
2. `pad` 模式下极端的非整数内接尺寸可能有 1px 抖动，已用 `round` + clamp 缓解，待 CUDA/多 dtype 复测。
3. dtype：当前内部 float32；未在 GPU 上验证大图 fp16 收益（本节点不涉及模型，优先级低）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 无尺寸参数 | 报错 | PASS（ValueError） |
| 极小 megapixels | 不产生 0px | PASS（clamp） |
| 1:200 极窄 + pad | 内接边 ≥1 | PASS |
| multiple_of > 边长 | 输出 ≥ multiple_of | PASS |
| batch 一致性 | 与逐张一致 | PASS |
