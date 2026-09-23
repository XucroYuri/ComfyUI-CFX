# Adversarial Review: comfyui_primitives_seed

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §8.1/§8.2 环形加减在边界正确，有测试。
- §8.4 `randomize` 的 `IS_CHANGED` 返回 NaN（强制重算），有测试。
- `fixed` 保持确定性。
- 不触碰 torch 全局 RNG，避免影响采样可复现性。

## 未决疑点
1. 未实现 rgthree 的「写回工作流元数据以复现」语义；如需可后续在 `IS_CHANGED`/隐藏输入上加。
