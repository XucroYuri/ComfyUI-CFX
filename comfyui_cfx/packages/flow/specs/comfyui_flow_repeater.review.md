# Adversarial Review: comfyui_flow_repeater

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- `OUTPUT_IS_LIST` 正确；返回 `([...],)`。
- §8.2 仅重复引用，不深拷贝张量（避免显存放大）。
- any 类型 socket 使用 `core.anytype`。

## 未决疑点
1. 重复的是同一对象引用；若下游原地修改输入会互相影响（ComfyUI 节点约定不原地改输入）。
