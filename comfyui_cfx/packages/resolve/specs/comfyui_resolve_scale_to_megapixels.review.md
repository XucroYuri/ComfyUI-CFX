# Adversarial Review: comfyui_resolve_scale_to_megapixels

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2 总像素推导：`scale = (megapixels * 1e6 / (w*h)) ** 0.5`，宽高比不变。
- §2 对齐：每边 `max(multiple_of, round(v/multiple_of)*multiple_of)`，防 0px。
- §3 接口：INPUT_TYPES / RETURN_TYPES / RETURN_NAMES / CATEGORY 与规格一致。
- §4 确定性：无随机性，不使用 `torch.no_grad` 包装。
- §6 无副作用：不写文件、无网络、无全局状态。
- §7 输入归一：经 `core.types.ensure_image`，非法输入抛清晰异常。
- 许可：实现为本仓原创（行为参考核心 scale-to-total-pixels，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. 下采样质量：统一使用用户选定采样方式；未按上/下采样自动切换。
2. 对齐使用四舍五入，极端非整数倍可能出现 1px 抖动（已由 `max` 兜底）。
3. dtype：内部固定 float32；未在 GPU 上验证大图收益（本节点不涉及模型）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 512x512 @ 1.0 MP | 1000x1000 | PASS |
| 800x400 宽图 | 宽高比保持 2:1 | PASS |
| multiple_of=64 | 两边均为 64 倍数 | PASS |
| 极小 megapixels | 不产生 0px | PASS（clamp） |
| 输出 shape | 等于返回 w/h | PASS |
