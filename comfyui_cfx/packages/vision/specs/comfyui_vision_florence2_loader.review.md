# Adversarial Review: comfyui_vision_florence2_loader

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §7 后端缺失时报错包含期望目录，便于用户安装。
- 复用上游自带实现（无 remote code），符合 ADR-0002。
- §8.3 `resolve_dtype` 对未知精度报 `ValueError`。

## 未决疑点
1. 依赖 `comfyui-florence2` 的内部函数 `load_florence2`；上游改签名会破坏。已用 `CFX_FLORENCE2_DIR`
   提供路径覆盖，并在 SPEC 记录该耦合。
2. 模型下载仅在首次；离线环境需预置 `models/LLM/<name>`。
