---
id: comfyui_primitives_text
display_name: "ComfyUI-Primitives · Text"
category: "ComfyUI-Primitives/Text"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Text Concatenate (WAS)"
  - "CR Text Concatenate / CR Text Replace (Comfyroll)"
  - "JWStringConcat / JWStringReplace (various)"
  - "ttN concat (tinyterra)"
  - "JjkConcat"
  - "AGSoftTextConcatenate"
---

## 1. 目的
唯一文本拼接/替换，替代 ~30 个实现；以 WAS `Text Concatenate` 的
trim / 跳空串 / 换行语义为行为基准。

## 2. 语义
- `operation=concat`：按 `text1..text8` 顺序拼接，可选 `clean_whitespace`（逐段 strip）
  与 `skip_empty`（跳过空串）。
- `operation=replace`：在 `text1` 上做字面量 `search → replace`。
- `delimiter` 支持转义 `\n`、`\t`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | operation | COMBO | 是 | concat |
| in | delimiter | STRING | 是 | ", " |
| in | clean_whitespace | BOOLEAN | 是 | True |
| in | skip_empty | BOOLEAN | 是 | True |
| in | search / replace | STRING | 是 | "" |
| in | text1..text8 | STRING | 否 | "" |
| out | text | STRING | - | - |

## 4. 执行与缓存
确定性；无随机；不定义 `IS_CHANGED`。

## 5. 资源
纯 Python 字符串。

## 6. 副作用与安全
无文件/网络。

## 7. 错误行为
全空输入 → 返回空串（不报错）。无其他失败路径。

## 8. 对抗性反例
1. 全空 / 全空白 → 空串；
2. `delimiter="\\n"` → 真实换行；
3. 未连接槽被跳过（不产生多余分隔符）；
4. `replace` 的 `search` 为空 → 不改变原文（`str.replace("", x)` 会插入，需特判）。

## 9. 验收
`tests/test_primitives_text.py`。
