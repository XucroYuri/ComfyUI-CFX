---
id: comfyui_vision_clip_interrogator
display_name: "ComfyUI-Vision · CLIP Interrogator"
category: "ComfyUI-Vision/Caption"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "clip-interrogator 直连脚本"
---

## 1. 目的
用 CLIP Interrogator 把图像反推为提示词风格的文本（正向或负向）。

## 2. 语义
- `mode=fast` → `interrogate_fast`；
- `mode=classic` → `interrogate_classic`；
- `mode=best` → `interrogate`；
- `mode=negative` → `interrogate_negative`（该后端方法不接受 `max_flavors`）；
- `clip_interrogator` 延迟导入（首次调用 `_load` 时），`Interrogator` 按 `clip_model` 缓存于
  `clip_interrogator._CACHE`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | clip_model | COMBO | 是 | ViT-L-14/openai |
| in | mode | COMBO | 是 | fast |
| in | max_flavors | INT | 是 | 4 |
| out | text | STRING | - | - |

## 4. 执行与缓存
`Config(clip_model_name=clip_model)` 构造 `Interrogator`，按模型名缓存；参数与实现解耦为
模块级 `MODE_METHODS`，可在无模型时单测。

## 5. 资源
CLIP/BLIP 权重由 `clip_interrogator` 自身管理（首次使用下载）。

## 6. 副作用与安全
首次使用会下载模型权重（用户触发）。

## 7. 错误行为
未知 `mode` → `ValueError`（在加载模型之前）；缺失依赖/模型 → 由 `clip_interrogator` 异常透传。

## 8. 对抗性反例
1. `mode=negative` 调用不接受 `max_flavors`，须单独分派；
2. 未知 `mode` 必须在 `_load` 之前抛出，避免无谓下载；
3. batch 取首张，与同包其他图像节点一致。

## 9. 验收
`tests/test_vision_clip_interrogator.py`（`MODE_METHODS`/COMBO/延迟导入/未知 mode）；
真实推理为 L3 人工 VERIFY（由集成方执行）。
