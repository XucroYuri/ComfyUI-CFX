---
id: comfyui_segment_sam2_mask
display_name: "ComfyUI-Segment · SAM2 Mask"
category: "ComfyUI-Segment/SAM2"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "Sam2Segmentation 的框提示路径 (ComfyUI-segment-anything-2，作为后端复用)"
  - "GroundingDinoSAM2Segment 的分割阶段 (comfyui-sam2)"
---

## 1. 目的
用框提示（来自检测/标注 JSON）驱动 SAM2 生成掩码，形成
`检测/标注 → SAM2 → MASK` 的完整链。

## 2. 语义
- `annotations` 必须是含 `bboxes` 的 dict（Florence-2 / GroundingDINO 输出格式）；
- 转换为上游期望的 per-image 批次形状后调用 `Sam2Segmentation().segment(...)`；
- `keep_model_loaded` 透传上游（False 时推理后 offload 释放显存）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | sam2 | CFX_SAM2 | 是 | - |
| in | image | IMAGE | 是 | - |
| in | annotations | JSON | 是 | - |
| in | keep_model_loaded | BOOLEAN | 否 | False |
| out | mask | MASK | - | - |

## 4. 执行与缓存
单图确定性；批次按上游逐图处理。

## 5. 资源
`keep_model_loaded=False` 时推理后 offload 并 `soft_empty_cache`（上游行为）。

## 6. 副作用与安全
无文件/网络。

## 7. 错误行为
缺 `bboxes` → `ValueError`；后端缺失 → `FileNotFoundError`。

## 8. 对抗性反例
1. 空 bboxes → `ValueError`；
2. 反向框 → 上游/NVIDIA 侧处理（本层不做归一，交由上游）；
3. 多框 → 上游合并/取最优（其既有语义）。
4. `keep_model_loaded` 两种取值均可运行。

## 9. 验收
`tests/test_segment_sam2.py`（`annotations_to_box_batch` 与接口）；真实推理人工 VERIFY。
