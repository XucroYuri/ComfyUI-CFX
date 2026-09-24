# Adversarial Review: comfyui_filter_sharpen

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2 形状：输出恒为 `[B,H,W,C]`，与输入同形，有单测。
- §2 值域：`clamp(...,0,1)` 保证输出严格落在 `[0,1]`，有单测。
- §2 `amount=0`：`img + diff*0 == img`，合法输入下逐元素等于原图，有 allclose 单测。
- §2 常量图：归一化核 + `reflect` 填充使 `blur == img`、`diff == 0`，输出不变且有限，有单测。
- §2 高斯模糊：复用 `high_pass._blur`（两次 `F.conv2d` + `reflect`，折批使每通道独立），与 High Pass 同算法，1/3/4 通道均可。
- §2 阈值门控：`torch.where(diff.abs() <= threshold, 0, diff)`，`threshold=1.0` 时全部置零，输出回到原图，有 allclose 单测。
- §2 锐化方向：`img + diff*amount`，边缘处过冲，`amount>0` 提升对比（`std` 增大），有单测。
- §7 非法输入：交给 `ensure_image` 统一抛错；`radius >=` 图像短边时 `F.pad` 直接报错，不静默降级。
- §6 无副作用：无文件/网络/全局状态，纯张量运算。
- 许可：实现为本仓原创（行为参考 Image-Filters / was-node-suite，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. `threshold` 为全局标量，非逐像素/逐通道；对局部噪声与边缘共用同一门限，属有意简化。
2. 高斯核每次调用重建；超大 `radius` 时有微小重复开销，未做核缓存（遵循“无投机性辅助”约定）。
3. `amount` 上界 5 与 `radius` 上界 64 可触发裁剪；作为设计选择保留。
4. GPU/大图显存峰值未做基准测量（逐元素 + 两次卷积，优先级低）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| `amount=0` | 等于原图 | PASS（allclose） |
| 常量图 | 输出不变且有限 | PASS |
| 阶跃边缘 | `std` 增大 | PASS |
| 大 `threshold` | 近似等于原图 | PASS（allclose） |
| 随机图 | 值域 [0,1] | PASS |
| `radius` 过大 | 报错 | PASS（F.pad 抛错） |
