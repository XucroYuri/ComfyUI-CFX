---
id: comfyui_primitives_image_transform
display_name: "ComfyUI-Primitives · Image Transform"
category: "ComfyUI-Primitives/Image"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Image Rotate / Image Flip / Image Transpose (WAS)"
  - "ImageFlip+ (essentials)"
  - "JWImageFlip (various)"
---

## 1. 目的
唯一无损旋转/翻转/转置，不重采样。

## 2. 语义
`operation ∈ {rotate90, rotate180, rotate270, flip_h, flip_v, transpose}`，
分别对应 `rot90(k=1/2/3)`、沿宽度轴翻转、沿高度轴翻转、`H↔W` 转置。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | operation | COMBO | 是 | rotate90 |
| out | image | IMAGE | - | - |

## 4. 执行与缓存
确定性；无重采样，输出为输入元素的置换。

## 5. 资源
无额外分配（除 contiguous 拷贝）。

## 6. 副作用与安全
无。

## 7. 错误行为
未知 `operation` → `ValueError`。

## 8. 对抗性反例
1. `rotate90` 后 H/W 交换；
2. `rotate90` 四次回到原图；
3. `flip_h` 与 `flip_v` 不同轴；
4. 非方形与 batch 处理。

## 9. 验收
`tests/test_primitives_image_transform.py`。
