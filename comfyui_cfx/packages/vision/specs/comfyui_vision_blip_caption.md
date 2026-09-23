---
id: comfyui_vision_blip_caption
display_name: "ComfyUI-Vision · BLIP Caption"
category: "ComfyUI-Vision/Caption"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "BLIP Model Loader + BLIP Analyze Image (was-node-suite)"
---

## 1. 目的
用 BLIP 做图像描述（caption）或视觉问答（interrogate）。

## 2. 语义
- `mode=caption`：`BlipForConditionalGeneration.generate`；
- `mode=interrogate`：`BlipForQuestionAnswering.generate(question)`；
- `transformers` 与模型**延迟加载**（首次调用时），处理器/模型按仓库名缓存。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | model | COMBO | 是 | Salesforce/blip-image-captioning-base |
| in | mode | COMBO | 是 | caption |
| in | question | STRING | 是 | What is in the image? |
| in | max_new_tokens | INT | 是 | 64 |
| out | text | STRING | - | - |

## 4. 执行与缓存
确定性（贪心解码）；模型缓存于 `blip._CACHE`。

## 5. 资源
模型经 `core.device.compute_device` 放到计算设备。

## 6. 副作用与安全
首次使用会下载模型权重（用户触发）。

## 7. 错误行为
缺失依赖/模型 → 由 transformers 异常透传。

## 8. 对抗性反例
1. `interrogate` 未提供 question → 使用默认；
2. 非 caption 模型走 VQA 分支（`vqa` 仓库）；
3. batch 取首张。

## 9. 验收
`tests/test_vision_blip.py`（接口/延迟导入）；真实推理为人工 VERIFY。
