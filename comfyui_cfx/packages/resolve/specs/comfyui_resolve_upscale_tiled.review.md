# Adversarial Review: comfyui_resolve_upscale_tiled

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2 分块：`tile_ranges` 返回半开区间，步长 `max(1, tile-overlap)`，末窗口回退保持 `tile` 宽并终止于 `length`。
- §2 语义：仅处理 batch 第 0 张，输出 `[1, H*scale, W*scale, C]`，已文档化。
- §2 尺度推导：由首个 tile 的 `out_w / tile_w` 推导，无额外探针前向。
- §3 接口：INPUT_TYPES / RETURN_TYPES / RETURN_NAMES / CATEGORY 与规格一致。
- §3 模型依赖：运行时需 `UPSCALE_MODEL`，本节点不加载模型，仅调用核心 `ImageUpscaleWithModel`。
- §4 确定性：无随机性，无 `torch.no_grad`/`inference_mode` 包装。
- §6 无副作用：不写文件、无网络、无全局状态。
- §7 校验：`overlap >= tile_size` 抛 `ValueError`；空 tile 结果抛 `ValueError`。
- §8 权重：画布边界权重为 1，内部重叠区对称羽化，`acc` 下限保护避免除零。
- 许可：实现为本仓原创（行为参考 UltimateSDUpscale 的分块羽化思路，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. 缩放系数取自首块宽度，假定模型尺度在 H/W 一致；非等比模型未覆盖。
2. 非整数放大尺度下 `round` 定位可能有 1px 误差（模型通常为整数倍）。
3. 大图多块时的峰值显存未在真实模型上基准测试。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| tile_size >= 边长 | 单窗口整图 | PASS |
| overlap=0 精确切分 | 无羽化无缝 | PASS |
| overlap >= tile_size | 抛 ValueError | PASS |
| 非整除尺寸 | 完整覆盖且末窗口满宽 | PASS |
| batch=N | 仅第 0 张，输出 batch=1 | PASS |
| 输出形状 | `[1, H*2, W*2, C]` | PASS |
| 值与整图 nearest 参考 | 容差内一致 | PASS |
