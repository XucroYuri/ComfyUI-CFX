# ComfyUI-Vision · SPEC

## 使命
打标/描述/VLM 的统一节点面、模型复用与单一缓存。

## 不负责
控制流、分割、文本提示生成（后者移出到文本域）。

## 来源
florence2（MIT，自带实现）、WD14（MIT）、Miaoshouai（MIT）、QwenVL（**GPL-3.0**）、
was(BLIP, MIT)、mixlab(MIT)、AcademiaSD(MIT)。

## 许可
本包 MIT。**QwenVL 的 GPL 代码必须隔离**为可选 `ComfyUI-Vision-Community` 包，默认不启用。

## 依赖与后端（已定）
- **禁止 `trust_remote_code`**（ADR-0002）。
- Florence-2 统一复用 `comfyui-florence2`（MIT）的**自带实现**（`comfy.ops`，无 remote code），
  经 `backend.load_florence2` 适配；路径可用 `CFX_FLORENCE2_DIR` 覆盖，缺失时报清晰错误。
- `QwenVL` 的 GPL-3.0 代码**不进入本包**，隔离为可选 `ComfyUI-Vision-Community`。
- 删除计划：`rmbg` 的 `AILab_Florence2*`（与 comfyui-florence2 重复）与
  `qwen3vl_caption_bridge.py`（已证必崩且绕过核心入口）。

## 节点 ID 前缀
`comfyui_vision_<verb>_<noun>` · 分类 `ComfyUI-Vision/<Sub>`
