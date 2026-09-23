---
id: comfyui_segment_matting
display_name: "ComfyUI-Segment · Matting"
category: "ComfyUI-Segment/Matting"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "RMBG / BiRefNetRMBG / AILab_SDMatte (comfyui-rmbg, GPL — 重写行为)"
  - "FaceSegment 之外的抠图路径"
---

## 1. 目的
统一抠图/去背，输出 alpha `MASK` 与 RGBA 抠图 `IMAGE`。

## 2. 语义
- 通过 `rembg`（MIT）的 `new_session(model)` + `remove(...)` 得到 RGBA 抠图；
- `mask = alpha / 255`；`image = RGBA / 255`；
- 会话按模型名缓存（`_SESSIONS`）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | model | COMBO | 是 | birefnet-general |
| out | mask | MASK | - | - |
| out | image | IMAGE (RGBA) | - | - |

## 4. 执行与缓存
确定性（同模型同输入）；会话按模型名缓存。

## 5. 资源
`rembg` 内部使用 onnxruntime；模型首次使用时下载。

## 6. 副作用与安全
首次使用下载模型权重（用户触发）；本地推理，无网络上传。

## 7. 错误行为
非 RGBA 结果 → `ValueError`（`alpha_to_mask`）；`rembg` 缺失 → `ImportError`。

## 8. 对抗性反例
1. alpha 全 0 / 全 255；
2. 非 4 通道数组 → 报错；
3. `image` 返回 RGBA（4 通道），下游需知情。

## 9. 验收
`tests/test_segment_matting.py`（`alpha_to_mask` 与接口）；真实推理人工 VERIFY。
