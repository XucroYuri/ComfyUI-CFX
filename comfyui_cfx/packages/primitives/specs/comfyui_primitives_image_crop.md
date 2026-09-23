---
id: comfyui_primitives_image_crop
display_name: "ComfyUI-Primitives · Image Crop"
category: "ComfyUI-Primitives/Image"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Image Crop Location (WAS)"
  - "Crop (mtb)"
  - "ycImageCrop"
  - "ImageCrop+ (essentials)"
  - "Image Inset Crop (rgthree)"
---

## 1. 目的
唯一图像裁剪：像素框或内缩（px/百分比），越界自动 clamp。

## 2. 语义
- `mode=pixel`：`x,y` 起点，`width/height` 为 0 时取到边缘。
- `mode=inset`：从四边内缩 `left/right/top/bottom`，`inset_unit` 为 `px` 或 `percent`。
- 结果至少 1px；所有值 clamp 在图像内。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | mode | COMBO | 是 | pixel |
| in | x / y / width / height | INT | 否 | 0 |
| in | left / right / top / bottom | FLOAT | 否 | 0 |
| in | inset_unit | COMBO | 否 | px |
| out | image | IMAGE | - | - |
| out | width / height | INT | - | - |

## 4. 执行与缓存
确定性；无随机。

## 5. 资源
纯张量切片（view→contiguous）。

## 6. 副作用与安全
无。

## 7. 错误行为
非法 shape → `ValueError`（来自 `ensure_image`）。

## 8. 对抗性反例
1. `x/y` 超出图像 → clamp 到最后一个像素；
2. inset 之和超过边长 → 至少保留 1px；
3. `width/height=0` → 取到边缘；
4. percent 单位换算正确。

## 9. 验收
`tests/test_primitives_image_crop.py`。
