---
id: comfyui_primitives_boolean
display_name: "ComfyUI-Primitives · Boolean"
category: "ComfyUI-Primitives/Logic"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Logic Boolean / Comparison* (WAS)"
  - "BooleanBasic / BooleanReverse (controlaltai)"
  - "CR Set Value On Boolean (Comfyroll)"
  - "easy boolean / if (easy-use)"
---

## 1. 目的
统一布尔真值语义（真 `bool`，杜绝 `"true"/"false"` 字符串），替代 5 套不一致实现。

## 2. 语义
对 `a`、`b` 两个布尔执行 `operation`：
`and / or / xor / nand / nor / a_implies_b / not_a / not_b`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | a | BOOLEAN | 是 | False |
| in | operation | COMBO | 是 | and |
| in | b | BOOLEAN | 否 | False |
| out | result | BOOLEAN | - | - |

## 4. 执行与缓存
确定性；无随机。

## 5. 资源
纯 Python。

## 6. 副作用与安全
无。

## 7. 错误行为
未知 `operation` → `ValueError`。

## 8. 对抗性反例
1. `not_a` / `not_b` 忽略 `b`；
2. `a_implies_b` 真值表正确（False→True 为真）；
3. 输入为 `0/1` 时按 bool 解释。

## 9. 验收
`tests/test_primitives_boolean.py`。
