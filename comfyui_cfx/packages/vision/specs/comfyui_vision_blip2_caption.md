---
id: comfyui_vision_blip2_caption
display_name: "ComfyUI-Vision · BLIP2 Caption"
category: "ComfyUI-Vision/Caption"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "BLIP-2 直连脚本"
---

## 1. 目的
用 BLIP-2 做图像描述（caption）或视觉问答（vqa）。

## 2. 语义
- `mode=caption`：`processor(pil)` → `Blip2ForConditionalGeneration.generate`；
- `mode=vqa`：`processor(pil, question)` → `generate`；
- `transformers` 与模型**延迟加载**（首次调用 `_load` 时）；处理器/模型按 `(model, precision)`
  缓存于 `blip2._CACHE`；
- 输入张量移至计算设备，浮点张量（`pixel_values`）转换为模型 dtype。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | model | COMBO | 是 | Salesforce/blip2-opt-2.7b |
| in | mode | COMBO | 是 | caption |
| in | question | STRING | 是 | What is in the image? |
| in | max_new_tokens | INT | 是 | 64 |
| in | precision | COMBO | 是 | bf16 |
| out | text | STRING | - | - |

## 4. 执行与缓存
确定性（贪心解码）；模型按 `(model, precision)` 缓存于 `nodes/blip2._CACHE`，dtype 由
`core.device.resolve_dtype` 决定。

## 5. 资源
模型经 `core.device.compute_device` 放到计算设备；dtype 由 `precision` 决定。

## 6. 副作用与安全
首次使用会下载模型权重（用户触发）。

## 7. 错误行为
未知 `precision` → `ValueError`（`resolve_dtype`，在加载模型之前）；缺失依赖/模型 →
由 transformers 异常透传。

## 8. 对抗性反例
1. `mode=vqa` 未提供 question → 使用默认；
2. 未知 `precision` 必须在 `_load` 下载之前抛出，避免无谓下载；
3. batch 取首张；
4. 同一模型不同 `precision` 不得互相复用缓存。

## 9. 验收
`tests/test_vision_blip2_caption.py`（COMBO/默认值/延迟导入/未知 precision）；真实推理为人工 VERIFY。
