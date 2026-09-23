---
id: comfyui_primitives_image_resize
display_name: "ComfyUI-Primitives · Image Resize"
category: "ComfyUI-Primitives/Image"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Image Resize (WAS)"
  - "JWImageResize* (various)"
  - "easy imageScale* (easy-use)"
  - "Image Scale By Factor (WLSH)"
  - "ImageResize+ (essentials)"
---

## 1. 目的
成为唯一图像缩放实现：由目标尺寸、缩放倍率或目标像素推导输出尺寸，并支持
`stretch / crop / pad` 三种适配方式。替代约 20 个分散实现。

## 2. 语义
- 尺寸推导优先级：`scale_by > target_megapixels > (width,height)`。
  - 只给 `width` 或只给 `height` 时按原始宽高比推导另一边。
  - `target_megapixels` 保持原始宽高比。
- 输出尺寸最终对齐到 `multiple_of`：`max(multiple_of, round(v/multiple_of)*multiple_of)`。
- 适配方式：
  - `stretch`：直接形变为目标尺寸。
  - `crop`：按目标宽高比裁切（锚点 `crop_position`），再缩放到目标尺寸。
  - `pad`：保持宽高比缩放到"内接矩形"，居中放入目标画布，空余用 `pad_color` 填充（letterbox）。
- 采样统一走 `comfy.utils.common_upscale`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | image | IMAGE | 是 | - | BHWC float32 |
| in | mode | COMBO | 是 | stretch | stretch/crop/pad |
| in | width | INT | 否 | 0 | 0=按 height 推导 |
| in | height | INT | 否 | 0 | 0=按 width 推导 |
| in | scale_by | FLOAT | 否 | 0.0 | >0 时优先 |
| in | target_megapixels | FLOAT | 否 | 0.0 | >0 时优先（保持比例） |
| in | multiple_of | INT | 否 | 8 | 输出对齐 |
| in | upscale_method | COMBO | 否 | bicubic | 采样方式 |
| in | crop_position | COMBO | 否 | center | mode=crop 锚点 |
| in | pad_color | FLOAT | 否 | 0.0 | mode=pad 填充灰度 |
| out | image | IMAGE | - | - | 缩放结果 |
| out | width | INT | - | - | 对齐后宽度 |
| out | height | INT | - | - | 对齐后高度 |

## 4. 执行与缓存
- 确定性：同输入逐元素可复现；无随机性。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。

## 5. 资源
- 纯张量；峰值显存 ≈ 输入 + 输出。不加载模型。
- dtype：内部按输入 dtype 运算；`ensure_image` 归一为 float32 后运算。

## 6. 副作用与安全
无文件/网络；无全局状态。

## 7. 错误行为
- 未提供任何尺寸来源（width/height/scale_by/target_megapixels）→ `ValueError`。
- 非法 shape → 由 `core.types.ensure_image` 抛出清晰 `ValueError`。

## 8. 对抗性反例
1. 全部尺寸参数为 0 → 报错；
2. `target_megapixels` 极小导致 0px → 由 `_align` clamp 到 `multiple_of`；
3. 极端宽高比 1:200 且 `pad` → 内接边取整不得为 0；
4. `multiple_of` 大于图像边长 → 输出不低于 `multiple_of`；
5. batch=N 与逐张执行结果一致。

## 9. 验收
- 属性测试覆盖 scale_by/width/height/megapixels/multiple_of/crop/pad；
- CPU 上 fp32 断言形状与数值；
- 见 `tests/test_primitives_image_resize.py`。
