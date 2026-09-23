---
id: comfyui_vision_tags_filter
display_name: "ComfyUI-Vision · Tags Filter"
category: "ComfyUI-Vision/Text"
version: 1.0.0
license: MIT
since: 2026-09-23
---

## 1. 目的
按包含/排除子串过滤标签串，并去重、限数。

## 2. 语义
- 按 `delimiter` 切分、strip、去空；
- 去重（默认大小写不敏感）；
- `include` 非空时保留匹配任一 include 子串的标签；
- `exclude` 命中任一子串则丢弃；
- `max_tags>0` 时截断。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | tags | STRING | 是 | "" |
| in | include | STRING | 是 | "" |
| in | exclude | STRING | 是 | "" |
| in | delimiter | STRING | 是 | ", " |
| in | case_sensitive | BOOLEAN | 是 | False |
| in | max_tags | INT | 是 | 0 |
| out | tags | STRING | - | - |

## 4. 执行与缓存
确定性。

## 5. 资源
纯字符串。

## 6. 副作用与安全
无。

## 7. 错误行为
无。

## 8. 对抗性反例
1. 全部被 exclude → 空串；
2. 去重（大小写不敏感）；
3. `max_tags=1` 只留首个；
4. include 为空 → 不限制。

## 9. 验收
`tests/test_vision_tags_filter.py`。
