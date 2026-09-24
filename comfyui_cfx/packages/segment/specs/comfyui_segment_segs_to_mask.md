---
id: comfyui_segment_segs_to_mask
display_name: "ComfyUI-Segment · SEGS to Mask"
category: "ComfyUI-Segment/Compat"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "Impact Pack SEGS consumer (impact-pack, GPL-3.0 — 仅参考公开数据格式，未复制代码)"
---

## 1. 目的
`mask_to_segs` 的逆：把 `SEGS` 的 `cropped_mask` 依 `crop_region` 贴回并按位取并集，
得到单张 MASK。

## 2. 语义
- 输出 `[1, H, W]` float32 零张量；`H`/`W` 由 `height`/`width` 覆盖，均为 0/未传时取
  第一个段落的整图尺寸 `(H, W)`。
- 逐段把 `cropped_mask` 贴到 `crop_region` `(x0, y0, x1, y1)`，与画布按 `np.maximum`（OR）合并。
- 裁剪超出画布时按画布边界截断（不越界、不报错）。
- 空 `SEGS` → `ValueError("segs_to_mask: empty SEGS")`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | segs | SEGS | 是 | - |
| in | width | INT | 否 | 0（0 → 首段宽） |
| in | height | INT | 否 | 0（0 → 首段高） |
| out | mask | MASK | - | - |

## 4. 执行与缓存
确定性纯几何，无模型、无缓存。

## 5. 资源
numpy 切片 + `np.maximum`，无额外依赖。

## 6. 副作用与安全
无。

## 7. 错误行为
空 `SEGS` → `ValueError`。

## 8. 对抗性反例
1. 空 `SEGS` → `ValueError`（不静默返回空 mask）；
2. 两段重叠 → OR 并集，重叠处取 `max`；
3. `width`/`height` 覆盖 → 输出尺寸变化；
4. 段落区域超出覆盖后的画布 → 按画布边界截断，不越界。

## 9. 验收
`tests/test_segment_segs.py`。
