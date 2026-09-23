---
id: comfyui_segment_grounding_dino
display_name: "ComfyUI-Segment · GroundingDINO Detect"
category: "ComfyUI-Segment/Detect"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "GroundingDinoSAM2Segment 的检测阶段 (comfyui-sam2)"
  - "Segment / SegmentV2 (rmbg, GPL — 重写行为)"
---

## 1. 目的
文本→框的**唯一**检测实现，统一到 transformers 的
`AutoModelForZeroShotObjectDetection`，弃用 `groundingdino-py` 与 vendored fork。

## 2. 语义
- 原生 transformers 加载 GroundingDINO（无 `trust_remote_code`）；
- `box_threshold` / `text_threshold` 过滤；
- 输出 `detections = {"bboxes":[[x0,y0,x1,y1],...], "labels":[...]}` 与填充后的 `MASK`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | prompt | STRING | 是 | person. dog. |
| in | model | COMBO | 是 | IDEA-Research/grounding-dino-tiny |
| in | box_threshold | FLOAT | 是 | 0.30 |
| in | text_threshold | FLOAT | 是 | 0.25 |
| out | detections | JSON | - | - |
| out | mask | MASK | - | - |

## 4. 执行与缓存
推理确定性；模型按仓库名缓存于 `detect._CACHE`。

## 5. 资源
模型固定 fp32（GroundingDINO 对半精度敏感），经 `compute_device` 放置。

## 6. 副作用与安全
首次使用下载权重（用户触发）；无 remote code。

## 7. 错误行为
依赖/模型缺失 → transformers 异常透传。

## 8. 对抗性反例
1. 无检测结果 → 空 bboxes + 全 0 mask；
2. batch 取首张；
3. 阈值极端（0/1）行为稳定。

## 9. 验收
`tests/test_segment_detect.py`（接口/延迟导入）；真实推理人工 VERIFY。
