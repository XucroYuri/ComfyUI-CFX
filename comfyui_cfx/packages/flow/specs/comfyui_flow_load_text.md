---
id: comfyui_flow_load_text
display_name: "ComfyUI-Flow · Load Text"
category: "ComfyUI-Flow/Text"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "LoadText|pysssss"
---

## 1. 目的
从**白名单目录**读取文本文件。

## 2. 语义
- 根目录：默认 `<output>/text`；可用环境变量 `CFX_TEXT_DIRS`（`os.pathsep` 分隔）覆盖。
- `path` 必须为相对路径，且解析后位于某个根之内。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | path | STRING | 是 | prompt.txt |
| out | text | STRING | - | - |

## 4. 执行与缓存
读取内容参与缓存键（内容变化会重算）。

## 5. 资源
纯文件读取。

## 6. 副作用与安全
**路径安全**：拒绝绝对路径；用 `commonpath` 校验归属，禁止 `..` 越界。

## 7. 错误行为
绝对路径 / 越界 / 文件不存在 → 抛错（`ValueError` 或 `FileNotFoundError`）。

## 8. 对抗性反例
1. `../outside.txt` → `ValueError`；
2. 绝对路径 → `ValueError`；
3. 不存在的文件 → `FileNotFoundError`；
4. 与 `save_text` 往返一致。

## 9. 验收
`tests/test_flow_text_file.py`。
