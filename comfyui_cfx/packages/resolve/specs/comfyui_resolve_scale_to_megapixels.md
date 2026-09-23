---
id: comfyui_resolve_scale_to_megapixels
display_name: "ComfyUI-Resolve · Scale to Megapixels"
category: "ComfyUI-Resolve/Scale"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "Image Scale to Total Pixels (ComfyUI core)"
  - "scale-to-total-pixels"
---

## 1. 目的
按目标总像素数缩放图像，保持原始宽高比，并将输出尺寸对齐到 `multiple_of`。
面向 SD/Flux 等对总像素与 8 的倍数敏感的下游节点。

## 2. 语义
- 目标尺寸按总像素推导：`scale = (megapixels * 1_000_000 / (width*height)) ** 0.5`，
  输出 `width*scale, height*scale`，因此宽高比不变。
- 每边独立对齐到 `multiple_of`：`max(multiple_of, round(v/multiple_of)*multiple_of)`，
  保证最小边不小于 `multiple_of`。
- 采样统一走 `comfy.utils.common_upscale`（`crop="disabled"`，即直接形变到目标尺寸）。
- 输入归一：`core.types.ensure_image`（HWC/BHWC/BCHW → BHWC float32）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | image | IMAGE | 是 | - | BHWC float32 |
| in | megapixels | FLOAT | 是 | 1.0 | 目标总像素（百万），min 0.01 max 64.0 |
| in | multiple_of | INT | 是 | 8 | 输出对齐，min 1 max 256 |
| in | upscale_method | COMBO | 是 | bicubic | bicubic/bilinear/area/nearest-exact/lanczos |
| out | image | IMAGE | - | - | 缩放结果 |
| out | width | INT | - | - | 对齐后宽度 |
| out | height | INT | - | - | 对齐后高度 |

## 4. 执行与缓存
- 确定性：同输入逐元素可复现；无随机性。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。

## 5. 资源
- 纯张量；峰值显存 ≈ 输入 + 输出。不加载模型。
- `ensure_image` 将输入归一为 float32 后运算；输出 dtype 与输入一致为 float32。

## 6. 副作用与安全
无文件/网络访问；无全局状态。

## 7. 错误行为
- 非张量或非法 shape → 由 `core.types.ensure_image` 抛出 `TypeError`/`ValueError`。
- 未支持采样方式 → 由 `comfy.utils.common_upscale` 抛出 `ValueError`。

## 8. 对抗性反例
1. 512x512 @ 1.0 MP → 1000x1000；
2. 极宽 800x400 → 输出宽高比仍为 2:1；
3. `multiple_of=64` → 输出两边均为 64 的倍数；
4. `megapixels` 极小 → 由 `max(multiple_of, …)` clamp，不产生 0px；
5. batch=N 与逐张执行结果一致（本实现整体处理 batch）。

## 9. 验收
- CPU fp32 断言输出形状与返回的 width/height 一致；
- 覆盖总像素、宽高比、对齐、极小值保护；
- 见 `tests/test_resolve_scale.py`。
