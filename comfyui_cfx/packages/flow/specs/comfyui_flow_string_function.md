---
id: comfyui_flow_string_function
display_name: "ComfyUI-Flow · String Function"
category: "ComfyUI-Flow/Text"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "StringFunction|pysssss (comfyui-custom-scripts)"
---

## 1. 目的
文本追加/前置/替换/正则替换，附可选标签整理（tidy）。行为参考 MIT 的 pysssss，独立重写。

## 2. 语义
- `append`：`text + delimiter + other`；`prepend` 反向。
- `replace`：字面量 `other → replacement`（`other` 为空则原样）。
- `regex_replace`：`re.sub(other, replacement, text)`；非法正则 → `ValueError`。
- `tidy=true`：按 `,` 切分、逐段 strip、去空段，再用 `", "` 连接。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | action | COMBO | 是 | append |
| in | text / other / replacement | STRING | 是 | "" |
| in | delimiter | STRING | 是 | ", " |
| in | tidy | BOOLEAN | 是 | False |
| out | text | STRING | - | - |

## 4. 执行与缓存
确定性；无随机。

## 5. 资源
纯字符串。

## 6. 副作用与安全
正则引擎为标准库 `re`；不做 ReDoS 防护（与上游一致，输入为本地文本）。

## 7. 错误行为
未知 `action`、非法正则 → `ValueError`。

## 8. 对抗性反例
1. `other=""` 的 replace → 原样；
2. 非法正则 `"("` → 报错；
3. tidy 去重空段与首尾空白；
4. 空 text + append → 返回 other。

## 9. 验收
`tests/test_flow_string_function.py`。
