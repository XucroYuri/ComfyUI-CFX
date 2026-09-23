---
id: comfyui_vision_florence2_loader
display_name: "ComfyUI-Vision · Florence-2 Loader"
category: "ComfyUI-Vision/Loaders"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "DownloadAndLoadFlorence2Model / Florence2ModelLoader (comfyui-florence2)"
  - "AILab_Florence2 的加载部分 (comfyui-rmbg, GPL)"
---

## 1. 目的
统一的 Florence-2 加载入口，复用 `comfyui-florence2`（MIT）的**自带实现**
（基于 `comfy.ops`，无 `transformers` remote code）。

## 2. 语义
- `model` 选中仓库名；本地目录为 `models/LLM/<repo 名>`，缺失时 `snapshot_download`。
- 通过上游 `load_florence2(path, dtype)` 构建 `ModelPatcher` 与 `Processor`。
- 返回句柄 `{"patcher","processor","dtype","path"}`（类型 `CFX_FLORENCE2`）。
- 调用 `mm.load_model_gpu` 载入计算设备。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | model | COMBO | 是 | MiaoshouAI/Florence-2-base-PromptGen-v2.0 |
| in | precision | COMBO | 是 | fp16 |
| out | florence2 | CFX_FLORENCE2 | - | - |

## 4. 执行与缓存
加载由 ComfyUI 模型管理托管；句柄在图中传递。

## 5. 资源
按 `precision` 载入；显存由 `model_management` 管理。

## 6. 副作用与安全
可能在首次使用时下载模型（用户触发、限量单一 artifact）。

## 7. 错误行为
后端 `comfyui-florence2` 未安装 → `FileNotFoundError`，信息含期望目录。

## 8. 对抗性反例
1. 后端缺失 → 清晰报错；
2. 本地已有模型 → 不下载；
3. 未知 precision → `ValueError`（`resolve_dtype`）。

## 9. 验收
`tests/test_vision_florence2.py`（仅测注册表/接口/后端定位；真实加载为人工 VERIFY）。
