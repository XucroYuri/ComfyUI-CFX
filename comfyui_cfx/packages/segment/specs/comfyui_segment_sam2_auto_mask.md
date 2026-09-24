---
id: comfyui_segment_sam2_auto_mask
display_name: "ComfyUI-Segment · SAM2 Auto Mask"
category: "ComfyUI-Segment/SAM2"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "Sam2AutoSegmentation (ComfyUI-segment-anything-2，作为后端复用)"
  - "SAM2AutomaticMaskGenerator / auto mask 节点 (comfyui-sam2，重复实现)"
---

## 1. 目的
无需任何提示，用 SAM2 自动掩码生成器一次性分割图中所有物体，补足
`sam2_mask`（框）/`sam2_points`（点）之外的全自动路径。

## 2. 语义
- `sam2` 句柄必须由 loader 以 `segmentor='automaskgenerator'` 加载，否则抛
  `ValueError`（点名 loader 设置），避免在上游深层失败；
- 通过 `backend.auto_mask` 调用上游 `Sam2AutoSegmentation().segment(...)`；
- 上游该 `segment` 的全部参数**无默认值**，适配层补齐其默认值，节点只暴露
  最常用的三个调节项（`points_per_side` / `pred_iou_thresh` / `stability_score_thresh`），
  未暴露项用上游默认值；
- `keep_model_loaded` 透传上游（False 时推理后 offload 释放显存）；
- **刻意丢弃上游的预览图**（`segmented_image`）：本节点只输出合并掩码与
  每掩码 bbox，叠加效果由调用方自行合成。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | sam2 | CFX_SAM2 | 是 | - |
| in | image | IMAGE | 是 | - |
| in | keep_model_loaded | BOOLEAN | 否 | False |
| in | points_per_side | INT | 否 | 32 |
| in | pred_iou_thresh | FLOAT | 否 | 0.8 |
| in | stability_score_thresh | FLOAT | 否 | 0.95 |
| out | mask | MASK | - | - |
| out | bboxes | JSON | - | - |

## 4. 执行与缓存
单图确定性；批次按上游逐图处理。输出 `mask` 为上游合并掩码（BHW），`bboxes`
为上游 `item['bbox']` 列表（每个 `[x, y, w, h]`）。

## 5. 资源
`keep_model_loaded=False` 时推理后 offload（上游行为）。自动掩码按
`points_per_side²` 个点采样，显存/耗时随该值显著上升。

## 6. 副作用与安全
无文件/网络。

## 7. 错误行为
句柄 `segmentor != 'automaskgenerator'` → `ValueError`（含所需 loader 设置）；
后端缺失 → `FileNotFoundError`；超出上游参数范围的取值由上游校验。

## 8. 对抗性反例
1. `single_image`/`video` 句柄 → 上游前即抛 `ValueError`，且不调用后端；
2. 仅暴露 3 个调节项，`points_per_side=1` 等极小值上游可运行（质量差但不报错）；
3. `keep_model_loaded` 两种取值均可运行；
4. 无检测结果 → 上游返回空 bbox 列表，非错误。

## 9. 验收
`tests/test_segment_sam2_auto.py`（返回值/透传/错误/接口）；真实推理人工 VERIFY。
