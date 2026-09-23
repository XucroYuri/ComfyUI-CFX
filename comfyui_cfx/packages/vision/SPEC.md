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

## 依赖约束
- 禁止 `trust_remote_code`（ADR-0002）。
- 4.x↔5.x 差异集中在 `packages/vision/compat.py`。

## 节点 ID 前缀
`comfyui_vision_<verb>_<noun>` · 分类 `ComfyUI-Vision/<Sub>`
