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
1. 真实推理未在 CI 覆盖（需大权重），标记人工 VERIFY。
2. `do_sample=False` 时 `temperature=None` 传入 `generate`，避免 transformers 警告。
3. GGUF 量化 VLM 未纳入（需 llama.cpp 后端，属另一实现）。
4. 模型缓存为模块级持久；绑定仓库名，最小化并文档化。
