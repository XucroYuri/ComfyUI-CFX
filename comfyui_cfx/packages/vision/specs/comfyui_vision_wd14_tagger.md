---
id: comfyui_vision_wd14_tagger
display_name: "ComfyUI-Vision · WD14 Tagger"
category: "ComfyUI-Vision/Tagging"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "WD14Tagger|pysssss (ComfyUI-WD14-Tagger)"
---

## 1. 目的
WD14 booru 打标（ONNX），统一 general/character 阈值与标签格式化。

## 2. 语义
- 读 `selected_tags.csv` 得 `(name, category)`；
- 图像预处理：转 RGB → 白边补成正方形 → 缩放到模型输入尺寸 → float32 HWC **BGR**；
- 阈值：`category==0` 用 `general_threshold`，`category==4` 用 `character_threshold`；
- 结果按分数降序，character 在前；`replace_underscore` 将 `_` 换空格；`exclude_tags` 子串过滤。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | model | COMBO | 是 | wd-v1-4-moat-tagger-v2 |
| in | general_threshold | FLOAT | 是 | 0.35 |
| in | character_threshold | FLOAT | 是 | 0.85 |
| in | replace_underscore | BOOLEAN | 是 | True |
| in | exclude_tags | STRING | 是 | "" |
| out | tags | STRING | - | - |

## 4. 执行与缓存
- 纯函数确定性；
- ONNX 会话按模型文件路径缓存（`wd14._SESSIONS`），避免每次执行重建。

## 5. 资源
ONNX Runtime；优先 `CUDAExecutionProvider`，否则 CPU。

## 6. 副作用与安全
首次使用会从 `SmilingWolf/<model>` 下载 `model.onnx` 与 `selected_tags.csv`（用户触发、单一 artifact）。

## 7. 错误行为
onnxruntime 缺失 / 模型下载失败 → 由底层异常透传。

## 8. 对抗性反例
1. 非正方形输入 → 白边补齐，不拉伸；
2. 全低分 → 空标签串；
3. character 阈值高 → 不误判；
4. `exclude_tags` 过滤生效。

## 9. 验收
`tests/test_vision_wd14.py`（纯函数）；ONNX 推理为人工 VERIFY（需模型）。
