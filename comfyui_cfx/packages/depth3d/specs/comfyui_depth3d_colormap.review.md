# Adversarial Review: comfyui_depth3d_colormap

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2 形状：`image` 恒为 `[B,H,W,3]` 且连续，有单测。
- §2 值域：归一化/夹紧 + matplotlib 查表均保证输出落在 `[0,1]`，有单测。
- §2 常量输入：`span == 0` 时用 `torch.where` 返回全零，`clamp_min(eps)` 避免除零，输出有限常量、无 `NaN`，有单测。
- §2 `normalize=False`：越界输入 `clamp(0,1)` 夹紧，matplotlib 亦按约定夹紧，无 `NaN`，有单测。
- §2 `gray`：`d.unsqueeze(-1).repeat(1,1,1,3)`，与归一化深度逐通道相等，有单测。
- §2 色标：`from matplotlib import colormaps` 惰性导入，非 `gray` 分支取 `[..., :3]` 丢弃 alpha，转为 float32；`turbo` 与 `viridis` 结果不同，有单测。
- §2 batch 独立：按 `dim=(1,2)` 逐项求 min/max，各项互不影响。
- §6 无副作用：无文件/网络/全局状态；惰性导入不初始化绘图后端。
- §7 非法色标名：matplotlib 查表抛 `KeyError`，不静默降级。
- 许可：实现为本仓原创（行为参考 DepthAnythingV3/controlnet_aux 可视化惯例，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. `colormap` 非枚举值依赖 matplotlib `KeyError`，未包装为 `ValueError`；前端 COMBO 已限制取值，待产品确认是否需要更友好的报错。
2. `normalize=True` 对离群深度噪点敏感，线性拉伸可能压低主体对比；如需鲁棒归一化需另立节点。
3. matplotlib 首次导入延迟与线程安全未做基准测量（逐元素，优先级低）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 常量图（max==min）归一化 | 有限常量、无 NaN | PASS |
| normalize=False 越界输入 | 夹紧 [0,1]、无 NaN | PASS |
| gray vs turbo | 结果不相等 | PASS |
| batch=2 量纲悬殊 | 各自归一 | PASS |
| gray | 等于归一化深度复制 3x | PASS |
