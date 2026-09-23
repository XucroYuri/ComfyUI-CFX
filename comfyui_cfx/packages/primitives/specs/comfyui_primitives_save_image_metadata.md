---
id: comfyui_primitives_save_image_metadata
display_name: "ComfyUI-Primitives · Save Image (Metadata)"
category: "ComfyUI-Primitives/IO"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Save Image w/Metadata (comfy-image-saver)"
  - "Image Save (WAS)"
  - "Image Save with Prompt (WLSH)"
  - "AGSoftSaveImage"
---

## 1. 目的
唯一带元数据保存：写入输出目录，PNG 内嵌 `parameters` 与工作流，可选侧车 `.txt`。

## 2. 语义
- 文件名/子目录由 `filename_prefix` 决定，`folder_paths.get_save_image_path` 分配目录与计数器。
- PNG：`parameters`（正/负提示 + 尺寸）+ `prompt` + `extra_pnginfo`。
- JPG/WEBP：按 `quality` 保存（无色度子采样控制）。
- `save_metadata_txt` 时写同名 `.txt`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | images | IMAGE | 是 | - |
| in | filename_prefix | STRING | 是 | ComfyUI-CFX |
| in | positive / negative | STRING | 是 | "" |
| in | format | COMBO | 是 | png |
| in | quality | INT | 是 | 95 |
| in | embed_workflow | BOOLEAN | 是 | True |
| in | save_metadata_txt | BOOLEAN | 是 | False |
| hidden | prompt / extra_pnginfo | - | 否 | - |
| out | （UI images） | - | - | - |

## 4. 执行与缓存
输出节点；无 `IS_CHANGED`（每次执行写盘）。

## 5. 资源
逐张转 uint8；不保留浮点副本超过当前循环。

## 6. 副作用与安全
- 写文件（输出目录）。
- `filename_prefix` **必须**相对路径，且拒绝 `..`（`validate_prefix`）。
- 目录由 `folder_paths` 解析，禁止越出输出根。

## 7. 错误行为
- 绝对路径 / 含 `..` 的前缀 → `ValueError`；
- 非法 `format` 由 widget 约束。

## 8. 对抗性反例
1. `../evil` 前缀 → 报错；
2. 绝对路径前缀 → 报错；
3. jpg + 4 通道（RGBA）→ 转 RGB 后保存；
4. batch=N → N 个文件且计数器递增；
5. `embed_workflow=False` → 不写 `prompt`/`extra_pnginfo`。

## 9. 验收
`tests/test_primitives_save.py`（仅测试前缀校验与 UI 返回，不实际依赖 ComfyUI 运行时可写目录）。
