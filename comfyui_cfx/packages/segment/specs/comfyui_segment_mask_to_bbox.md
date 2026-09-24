---
id: comfyui_segment_mask_to_bbox
display_name: "ComfyUI-Segment · Mask to BBox"
category: "ComfyUI-Segment/Geometry"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "MaskBoundingBox+ (comfyui_essentials, MIT — 仅参考行为)"
---

## 1. 目的
`annotations_to_mask` 的逆：把 MASK 的每个 batch 项还原为像素级包围盒，
供检测/裁剪/标注消费。

## 2. 语义
- 逐 batch 项取像素 `> threshold` 的包围盒 `[x0, y0, x1, y1]`，`x1`/`y1` 为**开区间**。
- 盒子按 `multiple_of` **向外**对齐（`x0`/`y0` 向下取整，`x1`/`y1` 向上取整）后夹取到图像范围内。
- 完全为空的项不产生条目；结果按 batch 顺序排列。
- `area` 为对齐并夹取后的盒子面积 `(x1-x0)*(y1-y0)`。
- 输出 `bboxes` 为 dict 列表 `{"bbox": [...], "area": int}`；`summary` 为简短人类可读串，
  如 `2 box(es); first: [x0, y0, x1, y1]`，全空时为 `0 box(es)`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | mask | MASK | 是 | - |
| in | threshold | FLOAT | 否 | 0.5（0.0–1.0, step 0.01） |
| in | multiple_of | INT | 否 | 1（1–256） |
| out | bboxes | JSON | - | - |
| out | summary | STRING | - | - |

## 4. 执行与缓存
确定性纯几何，无模型、无缓存。

## 5. 资源
numpy `nonzero` + 整数对齐，无额外依赖。

## 6. 副作用与安全
无。

## 7. 错误行为
非 `[H,W]`/`[B,H,W]` 的 mask → `ValueError`；helper 收到非 3D 数组 → `ValueError`。

## 8. 对抗性反例
1. 2D `[H,W]` → 视为 batch=1；
2. 空项 → 不产生条目，summary 为 `0 box(es)`；
3. 贴边 mask + `multiple_of` 大于图像 → 向外对齐后夹取，不越界；
4. `threshold` 为严格大于：等于阈值的像素不计入；
5. 多 batch 项 → 每项一个条目，按索引排序。

## 9. 验收
`tests/test_segment_mask_to_bbox.py`。
