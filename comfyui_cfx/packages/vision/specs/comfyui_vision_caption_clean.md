---
id: comfyui_vision_caption_clean
display_name: "ComfyUI-Vision · Caption Clean"
category: "ComfyUI-Vision/Text"
version: 1.0.0
license: MIT
since: 2026-09-23
---

## 1. 目的
统一清洗生成式 caption：控制 token、空白、重复标签、长度。

## 2. 语义
按序：`strip_tokens`（去 `<s>`/`</s>`/任意 `<...>`）→ `collapse_whitespace`
（压缩空白）→ `dedupe_tags`（按分隔符去重，保留首次出现）→ `max_chars`
（0 表示不截断；截断优先在最后一个分隔符处断开）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | text | STRING | 是 | "" |
| in | strip_tokens | BOOLEAN | 是 | True |
| in | collapse_whitespace | BOOLEAN | 是 | True |
| in | dedupe_tags | BOOLEAN | 是 | False |
| in | delimiter | STRING | 是 | ", " |
| in | max_chars | INT | 是 | 0 |
| out | text | STRING | - | - |

## 4. 执行与缓存
确定性。

## 5. 资源
纯字符串。

## 6. 副作用与安全
无。

## 7. 错误行为
无（非法输入按空串处理）。

## 8. 对抗性反例
1. 未闭合 `<` → 原样保留；
2. 重复标签去重保持顺序；
3. `max_chars` 在分隔符处断开，不产生半截标签；
4. 纯空白 → 空串。

## 9. 验收
`tests/test_vision_caption_clean.py`。
