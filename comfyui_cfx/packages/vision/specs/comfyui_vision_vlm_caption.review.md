# Adversarial Review: comfyui_vision_vlm_caption

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- **GPL 隔离**：实现为自有代码，使用 native `AutoModelForImageTextToText`；未引用或复制
  `ComfyUI-QwenVL`（GPL-3.0）。
- §6 **无 remote code**：`from_pretrained` 不使用 `trust_remote_code`，符合 ADR-0002。
- 延迟导入 `transformers`：模块导入不触发重依赖。
- §8.3 batch 取首张；§8.4 输出裁剪到新 token，不回显 prompt。

## 未决疑点
1. 真实推理已验证（见下）。
2. `do_sample=False` 时 `temperature=None` 传入 `generate`，避免 transformers 警告。
3. GGUF 量化 VLM 未纳入（需 llama.cpp 后端，属另一实现）。
4. 模型缓存为模块级持久；绑定仓库名，最小化并文档化。

## 实测修正（L3）
真实推理前发现并修复 1 处缺陷：
- `load()` 中的相对导入写成 `from ....core.device`，而该模块位于 `packages/vision/`（比 `nodes/` 少一层）
  → `ImportError: attempted relative import beyond top-level package`；已改为 `from ...core.device`。
修复后真实输出：`The image is a colorful drawing of a character with large, yellow ears and blue eyes, ...`
（首次下载遇网络中断，HF 断点续传后通过；非节点缺陷）。
