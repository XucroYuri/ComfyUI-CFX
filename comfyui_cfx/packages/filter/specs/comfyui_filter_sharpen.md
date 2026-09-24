---
id: comfyui_filter_sharpen
display_name: "ComfyUI-Filter · Sharpen"
category: "ComfyUI-Filter/Image"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "Sharpen (comfyui_image_filters / was-node-suite)"
---

## 1. 目的
提供确定性、无模型、无网络的锐化滤镜。以带阈值的钝化掩蔽（unsharp mask）增强边缘：
低于阈值的低对比细节不参与锐化，从而抑制平坦区域的噪声放大。

## 2. 语义
- 输入 `IMAGE` 经 `core.types.ensure_image` 归一为 `[B,H,W,C]` float32，值域 `[0,1]`。
- 高斯模糊复用 `nodes/high_pass.py` 的 `_blur`：核 `sigma = max(0.5, radius/2)`、尺寸 `2*radius+1`
  并归一化；把 `[B,H,W,C]` 折为 `[B*C,1,H,W]`，用 `reflect` 填充 `radius` 像素，
  再以水平核 `[1,1,1,k]` 与垂直核 `[1,1,k,1]` 各做一次 `F.conv2d`（分离式高斯）；
  折批使每通道独立模糊。
- 差值：`diff = img - blur`。
- 阈值门控：`|diff| <= threshold` 的位置令 `diff = 0`（忽略低对比细节）。
- 输出：`clamp(img + diff * amount, 0, 1)`，还原为 `[B,H,W,C]` float32、连续内存。
- `amount == 0` 时输出等于 `clamp(img,0,1)`，即原图（合法输入下逐元素不变）。
- `threshold >= max|diff|`（如 1.0）时全部细节被忽略，输出等于原图。
- 常量图：归一化核保证 `blur == img`，故 `diff == 0`，输出等于原常量。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | image | IMAGE | 是 | - | BHWC float32；1/3/4 通道 |
| in | radius | INT | 是 | 2 | 高斯半径，[1,64] |
| in | amount | FLOAT | 是 | 1.0 | 锐化增益，[0.0,5.0]，步长 0.01 |
| in | threshold | FLOAT | 是 | 0.0 | 细节阈值，`abs(diff) <= threshold` 置零，[0.0,1.0]，步长 0.01 |
| out | image | IMAGE | - | - | 锐化后图像 [B,H,W,C]，值域 [0,1] |

## 4. 执行与缓存
- 确定性：同输入逐元素可复现；无随机性、无全局状态。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。
- 高斯核每次调用时按 `radius` 由 `_blur` 重建，无跨调用缓存。

## 5. 资源
- 纯张量运算，CPU/GPU 随输入设备；峰值内存 ≈ 输入 + 模糊中间缓冲 + 差值缓冲。
- 模块导入仅依赖 `torch`、`core.types` 与同包 `high_pass._blur`，无第三方原生依赖。
- 输出张量 float32、连续内存。

## 6. 副作用与安全
- 无文件、无网络、无全局状态修改。
- 不写入 shared/temp 目录；不读取任何路径。

## 7. 错误行为
- 非张量 / 非法 shape / 非法通道数 → 由 `core.types.ensure_image` 抛 `TypeError`/`ValueError`。
- `reflect` 填充要求 `radius < H` 且 `radius < W`；不满足时由 `F.pad` 直接抛错（不静默降级为其它填充）。
- 不吞异常、不做隐式类型转换。

## 8. 对抗性反例
1. `amount = 0` → 输出逐元素等于 `clamp(img,0,1)`（合法输入下等于原图）；
2. 常量图 → `diff = 0`，输出仍为常量、无 NaN；
3. 阶跃边缘（低振幅，如 0.4/0.6）→ 边缘过冲使 `std` 增大（`amount=1`、`threshold=0`）；
4. 大 `threshold`（如 1.0）→ 全部 `|diff|<=1.0` 置零，输出近似等于原图；
5. 随机噪声图（含边界值）→ 输出严格落在 `[0,1]`；
6. `radius` 大于图像短边 → 报错，不静默裁剪或换填充模式。

## 9. 验收
- `tests/test_filter_sharpen.py`：形状保持、`amount=0` allclose、常量不变、值域 `[0,1]`、
  阶跃边缘 `std` 增大、大 `threshold` 抑制效果；
- CPU 上 fp32 断言；`torch` 缺失时 skip；
- `tools/spec_lint.py` 与 `tools/license_gate.py` 通过。
