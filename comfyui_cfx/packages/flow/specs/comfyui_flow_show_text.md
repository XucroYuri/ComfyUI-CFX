---
id: comfyui_flow_show_text
display_name: "ComfyUI-Flow · Show Text"
category: "ComfyUI-Flow/Text"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "ShowText|pysssss (comfyui-custom-scripts)"
  - "Display Any (rgthree)"
---

## 1. 目的
在节点上显示文本，并向后传递（可串联调试）。

## 2. 语义
返回 `{"ui": {"text": [text]}, "result": (text,)}`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 |
|---|---|---|---|
| in | text | STRING（forceInput, multiline） | 是 |
| out | text | STRING | - |

## 4. 执行与缓存
输出节点；文本参与缓存键。

## 5. 资源
纯 Python。

## 6. 副作用与安全
无。

## 7. 错误行为
无。

## 8. 对抗性反例
1. 超长文本（仅 UI 显示，不截断）；
2. 空文本。

## 9. 验收
`tests/test_flow_show_text.py`。
