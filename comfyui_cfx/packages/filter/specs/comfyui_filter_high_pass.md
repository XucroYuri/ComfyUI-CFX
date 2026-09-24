---
id: comfyui_filter_high_pass
display_name: "ComfyUI-Filter · High Pass"
category: "ComfyUI-Filter/Image"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "HighPass (comfyui_image_filters / was-node-suite)"
---

## 1. 目的
提供确定性、无模型、无网络的图像高通（钝化掩蔽 / unsharp）滤镜。
通过分离式高斯模糊提取高频分量，再按 `strength` 叠加回原图以增强边缘与细节。

## 2. 语义
- 输入 `IMAGE` 经 `core.types.ensure_image` 归一为 `[B,H,W,C]` float32，值域 `[0,1]`。
- 高斯核：`sigma = max(0.5, radius/2)`，尺寸 `2*radius+1`，归一化（核和一）。
- 模糊：先把 `[B,H,W,C]` 折为 `[B*C,1,H,W]`，用 `reflect` 填充 `radius` 像素，
  再以核分别做两次 `F.conv2d`（水平核 `[1,1,1,k]`、垂直核 `[1,1,k,1]`），即分离式高斯；
  与 `primitives/nodes/mask.py` 的 `_blur` 同一算法。折批处理使每通道独立模糊。
- 高通：`high = img - blur`。
- 输出：`clamp(img + high * strength, 0, 1)`，还原为 `[B,H,W,C]` float32。
- `strength == 0` 时输出等于 `clamp(img,0,1)`，即原图（合法输入下逐元素不变）。
- 常量图：归一化核保证 `blur == img`，故 `high == 0`，输出等于原常量。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | image | IMAGE | 是 | - | BHWC float32；1/3/4 通道 |
| in | radius | INT | 是 | 4 | 高斯半径，[1,256] |
| in | strength | FLOAT | 是 | 1.0 | 高通增益，[0.0,10.0]，步长 0.01 |
| out | image | IMAGE | - | - | 锐化后图像 [B,H,W,C]，值域 [0,1] |

## 4. 执行与缓存
- 确定性：同输入逐元素可复现；无随机性、无全局状态。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。
- 核在每次调用时按 `radius` 重建，无跨调用缓存。

## 5. 资源
- 纯张量运算，CPU/GPU 随输入设备；峰值内存 ≈ 输入 + 两次模糊中间缓冲。
- 模块导入仅依赖 `torch` 与 `core.types`，无第三方原生依赖。
- 输出张量 float32、连续内存。

## 6. 副作用与安全
- 无文件、无网络、无全局状态修改。
- 不写入 shared/temp 目录；不读取任何路径。

## 7. 错误行为
- 非张量 / 非法 shape / 非法通道数 → 由 `core.types.ensure_image` 抛 `TypeError`/`ValueError`。
- `reflect` 填充要求 `radius < H` 且 `radius < W`；不满足时由 `F.pad` 直接抛错（不静默降级为其它填充）。
- 不吞异常、不做隐式类型转换。

## 8. 对抗性反例
1. `strength = 0` → 输出逐元素等于 `clamp(img,0,1)`（合法输入下等于原图）；
2. 常量图 → `high = 0`，输出仍为常量、无 NaN；
3. 阶跃边缘（低振幅，如 0.4/0.6）→ 边缘过冲使 `std` 单调不减/增大（`strength>0`）；
4. 随机噪声图（含边界值）→ 输出严格落在 `[0,1]`；
5. `radius` 大于图像短边 → 报错，不静默裁剪或换填充模式。

## 9. 验收
- `tests/test_filter_high_pass.py`：形状保持、`strength=0` allclose、常量不变、值域 `[0,1]`、阶跃边缘 `std` 增大；
- CPU 上 fp32 断言；`torch` 缺失时 skip；
- `tools/spec_lint.py` 与 `tools/license_gate.py` 通过。
