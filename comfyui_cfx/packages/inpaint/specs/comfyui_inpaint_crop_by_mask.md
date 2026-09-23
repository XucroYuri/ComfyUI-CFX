---
id: comfyui_inpaint_crop_by_mask
display_name: "ComfyUI-Inpaint · Crop by Mask"
category: "ComfyUI-Inpaint/Crop"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
按掩码包围盒裁剪图像与掩码，并输出可复用的 `crop_data`（供后续 stitch 还原）。

## 2. 语义
- 取掩码中 `> 0.5` 像素的包围盒 `[x0, x1) × [y0, y1)`；全空则报错。
- 四边外扩 `padding`；再向**外**对齐到 `multiple_of`（`x0/y0` 下取整、`x1/y1` 上取整）。
- 对齐后 clamp 到图像范围，且保证每边至少 1px。
- 图像只取第一个 batch 项，输出 `[1, h, w, C]`；掩码输出 `[1, h, w]`。
- `crop_data` 为 `{x, y, width, height, original_width, original_height}`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | mask | MASK | 是 | - |
| in | padding | INT | 是 | 32 |
| in | multiple_of | INT | 是 | 8 |
| out | image | IMAGE | - | - |
| out | mask | MASK | - | - |
| out | crop_data | JSON | - | - |

## 4. 执行与缓存
确定性；无随机。

## 5. 资源
纯张量切片（`contiguous`）；无模型、无外部文件。

## 6. 副作用与安全
无。

## 7. 错误行为
- 掩码无 `> 0.5` 像素 → `ValueError("crop_by_mask: mask is empty")`。
- 掩码非 2D/3D → `ValueError`。
- 非法图像 shape → `ValueError`（来自 `ensure_image`）。

## 8. 对抗性反例
1. padding 把框推到图像外 → clamp 到边界；
2. 掩码贴边 → 对齐仍不越界；
3. `multiple_of` 大于图像 → 结果收缩到整图（≥1px）；
4. 全空掩码 → 抛错，不返回退化结果；
5. 掩码为 `[B,H,W]` → 取第一项。

## 9. 验收
`tests/test_inpaint_crop.py`。
