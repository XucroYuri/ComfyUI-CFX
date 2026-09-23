---
id: comfyui_flow_save_text
display_name: "ComfyUI-Flow · Save Text"
category: "ComfyUI-Flow/Text"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "SaveText|pysssss"
---

## 1. 目的
把文本写入**白名单目录**。

## 2. 语义
- 根目录与校验同 `load_text`。
- `mode=overwrite` 覆盖；`append` 追加。
- 自动创建父目录。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | text | STRING | 是 | "" |
| in | path | STRING | 是 | prompt.txt |
| in | mode | COMBO | 是 | overwrite |
| out | （UI text） | - | - | - |

## 4. 执行与缓存
输出节点；每次执行写盘。

## 5. 资源
逐次写字符串。

## 6. 副作用与安全
写文件；**路径安全**同 `load_text`（相对路径 + 归属校验）。

## 7. 错误行为
绝对路径 / 越界 → `ValueError`。

## 8. 对抗性反例
1. `../evil.txt` → `ValueError`；
2. append 两次 → 内容拼接；
3. 子目录不存在 → 自动创建；
4. 绝对路径 → `ValueError`。

## 9. 验收
`tests/test_flow_text_file.py`。
