---
id: comfyui_segment_text_to_mask
display_name: "ComfyUI-Segment · Text to Mask"
category: "ComfyUI-Segment/Detect"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "GroundingDinoSAM2Segment 全链路 (comfyui-sam2)"
  - "手工连接 grounding_dino → sam2_mask 的常见工作流"
---

## 1. 目的
把「文本 → 框 → 掩码」的经典全链路收进一个组合节点：
GroundingDINO 文本检测 → SAM2 框提示分割，减少中间 JSON 连线。

## 2. 语义
- 复用 `nodes/detect.py` 的 `CFXGroundingDinoDetect().run(...)` 得到 `detections`
  （`{"bboxes": [[x0,y0,x1,y1], ...], "labels": [...]}`），不复制检测逻辑；
- 若提供 `sam2` 且检测到框：`backend.segment(sam2, image, bboxes=annotations_to_box_batch(detections), keep_model_loaded=...)`；
- 若未提供 `sam2`：用 `geometry.boxes_to_mask(detections["bboxes"], H, W)` 几何回退
  （`H, W` 取自 `core.types.ensure_image`）；
- 无框（含空 `bboxes`）→ 全 0 MASK，**绝不抛错**；
- `detections` 原样透传（同一对象），便于下游继续使用。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | prompt | STRING | 是 | person. dog. |
| in | detect_model | COMBO | 是 | IDEA-Research/grounding-dino-tiny |
| in | box_threshold | FLOAT | 是 | 0.30 |
| in | text_threshold | FLOAT | 是 | 0.25 |
| in | sam2 | CFX_SAM2 | 否 | - |
| in | keep_model_loaded | BOOLEAN | 否 | False |
| out | mask | MASK | - | - |
| out | detections | JSON | - | - |

## 4. 执行与缓存
检测模型按仓库名缓存于 `detect._CACHE`；SAM2 显存由 `keep_model_loaded` 透传上游管理。
本节点不额外缓存。

## 5. 资源
检测为 fp32（GroundingDINO 对半精度敏感）；SAM2 精度/设备由加载器决定。
回退路径纯几何，无 GPU 占用。

## 6. 副作用与安全
首次检测使用下载权重（用户触发）；无 remote code；无文件/网络写入。

## 7. 错误行为
- 空 `bboxes` → 全 0 MASK（不抛错，且不调用 SAM2）；
- SAM2 后端缺失 → `FileNotFoundError`（经 `backend` 透传）；
- 检测依赖/模型缺失 → transformers 异常透传。

## 8. 对抗性反例
1. 阈值过高导致零检测 → 全 0 mask，且 `segment` 不被调用；
2. 提供 `sam2` 但无框 → 走零 mask 分支，不触发 SAM2；
3. `keep_model_loaded` 两种取值均可运行；
4. 多框 → 整体批次交给 SAM2；回退时全部框填充；
5. batch 图像 → `ensure_image` 取 `[B,H,W,C]` 的 H/W，检测取首张（沿用 detect 语义）。

## 9. 验收
`tests/test_segment_text_to_mask.py`（monkeypatch 检测与后端，离线可跑）；
真实推理人工 VERIFY。
