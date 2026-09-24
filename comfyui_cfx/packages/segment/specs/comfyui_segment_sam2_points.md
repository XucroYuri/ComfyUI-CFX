---
id: comfyui_segment_sam2_points
display_name: "ComfyUI-Segment · SAM2 Points"
category: "ComfyUI-Segment/SAM2"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "Sam2Segmentation 的点提示路径 (ComfyUI-segment-anything-2，作为后端复用)"
  - "Florence2toCoordinates 的坐标序列 (comfyui-sam2，重复实现)"
---

## 1. 目的
用正/负点击点提示驱动 SAM2 生成掩码，补足 `sam2_mask` 仅支持框提示的缺口。

## 2. 语义
- `positive_points` / `negative_points` 接受 `[[x, y], ...]` 或 `[{"x": x, "y": y}, ...]` 文本；
- `parse_points` 归一为 `[{"x": float, "y": float}, ...]`，再 `json.dumps` 后透传上游；
- `positive_points` 解析为空 → `ValueError`；无负点 → `negative=None`；
- `keep_model_loaded` 透传上游（False 时推理后 offload 释放显存）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | sam2 | CFX_SAM2 | 是 | - |
| in | image | IMAGE | 是 | - |
| in | positive_points | STRING | 是 | "[[128, 128]]" |
| in | negative_points | STRING | 否 | "" |
| in | keep_model_loaded | BOOLEAN | 否 | False |
| out | mask | MASK | - | - |

## 4. 执行与缓存
单图确定性；批次按上游逐图处理。

## 5. 资源
`keep_model_loaded=False` 时推理后 offload 并 `soft_empty_cache`（上游行为）。

## 6. 副作用与安全
无文件/网络。

## 7. 错误行为
点文本不是 `[[x, y], ...]` / `[{"x": x, "y": y}, ...]` → `ValueError`；正点为空 → `ValueError`；后端缺失 → `FileNotFoundError`。

## 8. 对抗性反例
1. 空正点 → `ValueError`；
2. 非法 JSON / 非法形状 / 缺 `x`/`y` → `ValueError`；
3. 仅正点 → `negative=None`；
4. 正 + 负点 → 两者均归一为 JSON 字符串透传；
5. `keep_model_loaded` 两种取值均可运行。

## 9. 验收
`tests/test_segment_sam2_points.py`（`parse_points` 与接口）；真实推理人工 VERIFY。
