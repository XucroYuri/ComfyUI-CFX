# Adversarial Review: comfyui_primitives_text

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §2 拼接语义与 WAS 基准一致：trim、跳空串、未连接跳过，不产生多余分隔符。
- §8.2 转义：`\n` / `\t` 生效。
- §7 全空输入返回空串，无异常。
- 确定性、无副作用。

## 已证伪项（已在实现中修正）
1. `replace` 模式下 `search=""` 时 `str.replace("", x)` 会在每个字符间插入——已通过
   "空 search 则原样返回" 的判定修复，并在测试中断言。

## 未决疑点
1. 固定 8 路输入；后续如需任意数量，改 `io.Autogrow`（保持顺序语义）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 全空 | 空串 | PASS |
| `\n` 分隔符 | 真换行 | PASS |
| 跳空串 | 无多余分隔符 | PASS |
| 空 search 的 replace | 原文不变 | PASS |
