---
id: comfyui_vision_florence2_run
display_name: "ComfyUI-Vision · Florence-2 Run"
category: "ComfyUI-Vision/Florence2"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Florence2Run (comfyui-florence2)"
  - "AILab_Florence2 (comfyui-rmbg, GPL)"
  - "Miaoshouai_Tagger（改为经本节点 + 共享后端）
---

## 1. 目的
单一 Florence-2 任务节点，覆盖 13 类任务（caption/tags/OCR/bbox/polygon）。

## 2. 语义
- `task` 友好名 → 任务 token（`registry.FLORENCE2_TASKS`）。
- 取 batch 第一张，转 CHW 交给上游 `Processor`；`generate` 后 `post_process_generation`。
- `STRING` 输出为纯文本任务的结果；`JSON` 输出为解析结果（文本任务为字符串，检测任务为结构）。
- **不在本节点释放模型**：句柄可能被多个 Run 节点复用，显存由 ComfyUI 模型管理统一回收。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | florence2 | CFX_FLORENCE2 | 是 | - |
| in | image | IMAGE | 是 | - |
| in | task | COMBO | 是 | more_detailed_caption |
| in | max_new_tokens | INT | 否 | 1024 |
| in | num_beams | INT | 否 | 3 |
| in | do_sample | BOOLEAN | 否 | False |
| out | text | STRING | - | - |
| out | parsed | JSON | - | - |

## 4. 执行与缓存
确定性（`do_sample=False` 时）。

## 5. 资源
单张推理；结束后释放。

## 6. 副作用与安全
无文件/网络。

## 7. 错误行为
未知 task → `ValueError`；非法句柄 → `KeyError`。

## 8. 对抗性反例
1. `task` 未知 → `ValueError`；
2. 纯文本任务 → `text` 非空、`parsed` 为字符串；
3. 检测任务 → `parsed` 为结构，`text` 为空串；
4. 多 batch 输入 → 取首张（文档化）。

## 9. 验收
`tests/test_vision_florence2.py`（任务映射与接口）；真实推理为人工 VERIFY。
