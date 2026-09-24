# Adversarial Review: comfyui_sampling_split_sigmas

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- 契约：id/显示名/分类/`RETURN_TYPES`/`RETURN_NAMES`/`FUNCTION=run` 与 SPEC 一致。
- 语义：返回 `(sigmas[:step], sigmas[step:])`，两路均 `.contiguous()`，保持 dtype 与 device。
- 边界：`step=0` 给出空 high + 完整 low；`step=len` 给出完整 high + 空 low。
- 校验：非一维输入与 `step > len(sigmas)` 均 `ValueError`。
- 无副作用：不就地修改输入；无文件/网络/全局状态。
- 注册：`nodes/__init__.py` 以元组循环合并，重复 id 抛
  `RuntimeError(f"duplicate node ids in sampling: {sorted(_duplicates)}")`。

## 未决疑点
1. `step` 的 INT 控件上限 10000 远大于典型 sigma 长度，超长时由 `step > len` 校验兜底。
2. 输入假定为 `SIGMAS` 类型；非张量输入会自然抛 `AttributeError`，不在本节点契约内。
