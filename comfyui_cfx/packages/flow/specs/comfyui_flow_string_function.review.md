# Adversarial Review: comfyui_flow_string_function

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §8.1 空 `other` 的 replace 原样返回。
- §8.2 非法正则 `ValueError`，有测试。
- §8.3 tidy 行为确定，有测试。
- 独立重写，未复制 pysssss 代码（仅行为参考，MIT）。

## 未决疑点
1. `tidy` 的分隔符固定为 `", "`（danbooru 风格），不随 `delimiter` 变化；已在 SPEC 说明。
