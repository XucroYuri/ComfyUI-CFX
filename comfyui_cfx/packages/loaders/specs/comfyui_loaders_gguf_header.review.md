# Adversarial Review: comfyui_loaders_gguf_header

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2/§8.1–8.2 魔数、version、tensor_count、metadata_kv_count 按 v2/v3 头布局解析，有单测。
- §6 路径包含：经 `safe_join(folder_paths.models_dir, path)`，`..` 与绝对路径被拒绝，有测试。
- §5 仅读 24 字节头部，不读取权重负载，不做张量反序列化。
- §7 魔数错误与截断分别抛 `ValueError`，错误信息明确，不静默降级。

## 未决疑点
1. 版本号不做 2/3 白名单校验：非 2/3 版本仍按公共头部布局解析；如需严格限制，应在后续版本显式拒绝。
2. 未解析 `metadata_kv_count` 之后的键值区；本节点契约只覆盖固定头部。
