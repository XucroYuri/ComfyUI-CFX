# Adversarial Review: comfyui_loaders_safetensors_info

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2/§8.1–8.2 `tensor_count`、dtype 直方图与 `metadata_keys` 取自 `safe_open`/`get_slice`，无元数据回退为空列表，有单测。
- §6 路径包含：经 `safe_join(folder_paths.models_dir, path)`，`..` 与绝对路径被拒绝，有测试。
- §5 仅解析头部与 dtype 元信息，不读取权重负载，不做张量实例化。
- §7 非 safetensors 内容被 `SafetensorError` 捕获并转为 `ValueError`，不静默降级。

## 未决疑点
1. dtype 名称沿用 safetensors 原生标识（如 `F32`/`I8`），未映射为 PyTorch 名称；契约以原生标识为准。
2. 元数据值不读取，仅返回键名；如需值需扩展契约。
