# Adversarial Review: comfyui_depth3d_normalize_depth

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2 形状：`image` 恒为 `[B,H,W,3]`、`mask` 恒为 `[B,H,W]`，有单测。
- §2 值域：`minmax` 归一与 `clamp` 截断均保证输出落在 `[0,1]`，有单测。
- §2 常量输入：`span == 0` 时用 `torch.where` 返回全零，`clamp_min(eps)` 避免除零，无 `NaN`，有单测。
- §2 batch 独立：按 `dim=(1,2)` 逐项求 min/max，量纲悬殊的两项各自归一，有单测。
- §2 `invert`：归一化后 `1 - d`，与 `invert=False` 互补，值域保持 `[0,1]`，有单测。
- §2 深度通道：`mean(dim=-1)` 与 `ensure_image` 配合，1/3/4 通道输入均可。
- §7 非法输入：交给 `ensure_image` 统一抛错，不静默降级。
- §6 无副作用：无文件/网络/全局状态，纯张量运算。
- 许可：实现为本仓原创（行为参考 DepthAnythingV3/controlnet_aux，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. `mode` 非枚举值落入 `clamp` 分支（`else`）而非报错；前端 COMBO 已限制取值，API 直调时行为为“静默截断”，待产品确认是否需要显式 `ValueError`。
2. `minmax` 对离群值（如深度噪点）敏感，线性拉伸可能压低主体对比；如需鲁棒归一化需另立节点。
3. 大 batch/大图显存峰值未做基准测量（逐元素运算，优先级低）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 常量图（max==min） | minmax 全零且有限 | PASS（无 NaN） |
| clamp 越界输入 | 值域 [0,1] | PASS |
| invert=True | 等于 1-基准 | PASS |
| batch=2 量纲悬殊 | 各自归一 | PASS |
| 非常量输入 | 同时有 0.0 与 1.0 | PASS |
