# Adversarial Review: comfyui_filter_high_pass

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2 形状：输出恒为 `[B,H,W,C]`，与输入同形，有单测。
- §2 值域：`clamp(...,0,1)` 保证输出严格落在 `[0,1]`，有单测。
- §2 `strength=0`：`img + high*0 == img`，合法输入下逐元素等于原图，有 allclose 单测。
- §2 常量图：归一化核 + `reflect` 填充使 `blur == img`、`high == 0`，输出不变且有限，有单测。
- §2 分离式高斯：与 `primitives/nodes/mask.py` 的 `_blur` 同算法（两次 `F.conv2d` + `reflect`）；折批处理使每通道独立，1/3/4 通道均可。
- §2 高通符号：`high = img - blur`，边缘处过冲，`strength>0` 提升对比（`std` 增大），有单测。
- §7 非法输入：交给 `ensure_image` 统一抛错；`radius >=` 图像短边时 `F.pad` 直接报错，不静默降级。
- §6 无副作用：无文件/网络/全局状态，纯张量运算。
- 许可：实现为本仓原创（行为参考 Image-Filters / was-node-suite，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. 核每次调用重建；超大 `radius` 时有微小重复开销，未做核缓存（遵循“无投机性辅助”约定）。
2. `strength` 上界 10 极易触发裁剪，作为设计选择保留；未对极端强度设防。
3. GPU/大图显存峰值未做基准测量（逐元素 + 两次卷积，优先级低）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| `strength=0` | 等于原图 | PASS（allclose） |
| 常量图 | 输出不变且有限 | PASS |
| 阶跃边缘 | `std` 增大 | PASS |
| 随机图 | 值域 [0,1] | PASS |
| `radius` 过大 | 报错 | PASS（F.pad 抛错） |
