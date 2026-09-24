# Adversarial Review: comfyui_sampling_sigma_shift

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- 契约：id/显示名/分类/`RETURN_TYPES`/`RETURN_NAMES`/`FUNCTION=run` 与 SPEC 一致。
- 语义：返回 `sigmas * factor` 的 `.contiguous()` 新张量，保持 dtype 与 device。
- 单位元：`factor=1.0` 数值不变，但仍返回新张量，未共享存储。
- 缩放：`factor=2.0` 每个元素翻倍。
- 校验：非一维输入 `ValueError`。
- 无副作用：不就地修改输入；无文件/网络/全局状态。
- 注册：`nodes/__init__.py` 以元组循环合并 `sigmas` 与 `shift`，重复 id 抛
  `RuntimeError(f"duplicate node ids in sampling: {sorted(_duplicates)}")`。

## 未决疑点
1. `factor` 的 FLOAT 控件下限 0.001，排除 0 与负值；此为契约内的调度缩放语义。
2. 输入假定为 `SIGMAS` 类型；非张量输入会自然抛 `AttributeError`，不在本节点契约内。
