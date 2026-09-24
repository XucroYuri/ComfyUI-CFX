# Adversarial Review: comfyui_controlnet_normal_map_from_depth

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2 形状：`image` 恒为 `[B,H,W,3]`，有单测。
- §2 值域：`(n+1)/2` 编码保证输出落在 `[0,1]`，有单测。
- §2 深度通道：`mean(dim=-1)` 与 `ensure_image` 配合，1/3/4 通道输入均可。
- §2 梯度：内部中心差分、边界单侧差分，边缘安全；沿 dim=1/2 分别得 dy/dx，有平坦反例。
- §2 单位化：`z=1` 保证模长 `>= 1`，除零不可能，解码向量单位长度，有单测。
- §2 `invert`：`depth=1-depth`，x/y 编码互补、z 不变，有单测。
- §2 batch：逐项独立，输出 batch 维保持，有单测。
- §7 非法输入：交给 `ensure_image` 统一抛错，不静默降级。
- §6 无副作用：无文件/网络/全局状态，纯张量运算。
- 许可：实现为本仓原创（行为参考 controlnet_aux，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. 单侧边界差分在图像边缘的梯度幅值弱于中心差分，边缘一圈法线可能略有偏差；当前不引入填充/外推。
2. `strength` 仅线性缩放梯度，未做深度尺度自适应；不同深度量纲的输入需调用方自行调参。
3. 大 batch/大图显存峰值未做基准测量（逐元素运算，优先级低）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 平坦深度图 | z 主导 `[0.5,0.5,1.0]` | PASS |
| 任意深度图 | 解码单位长度 | PASS |
| invert=True | x/y 与基准互补 | PASS |
| 常量图 | 有限无 NaN | PASS |
| batch=2 | 输出 batch=2 | PASS |
