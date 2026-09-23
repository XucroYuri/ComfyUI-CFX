---
id: comfyui_segment_annotations_to_mask
display_name: "ComfyUI-Segment · Annotations to Mask"
category: "ComfyUI-Segment/Geometry"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "AILab_Florence2ToCoordinates (rmbg, GPL — 重写行为)"
  - "Florence2toCoordinates (ComfyUI-segment-anything-2)"
---

## 1. 目的
把检测标注（Florence-2 风格的 bbox / polygon）栅格化为 MASK，作为检测→分割/抠图的桥。

## 2. 语义
- 输入为 dict：优先 `polygons`，否则 `bboxes`；两者都无则报错。
- 尺寸：连接了 `image` 时取其 H/W，否则用 `width`/`height`。
- `line_width=0` 填充；>0 只画边框；`invert` 反相。
- 输出 `MASK` 形状 `[1,H,W]`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | annotations | JSON | 是 | - |
| in | image | IMAGE | 否 | - |
| in | width / height | INT | 否 | 1024 |
| in | line_width | INT | 否 | 0 |
| in | invert | BOOLEAN | 否 | False |
| out | mask | MASK | - | - |

## 4. 执行与缓存
确定性。

## 5. 资源
PIL 栅格化 + numpy，转 float32。

## 6. 副作用与安全
无。

## 7. 错误行为
非 dict / 缺 bboxes 与 polygons → `ValueError`。

## 8. 对抗性反例
1. `x1<x0` / `y1<y0` 的框 → 自动交换；
2. 多边形点数 <3 → 跳过；
3. 尺寸为 0 → 至少 1px；
4. 空 bboxes 且空 polygons → 报错。

## 9. 验收
`tests/test_segment_annotations.py`、`tests/test_segment_geometry.py`。
