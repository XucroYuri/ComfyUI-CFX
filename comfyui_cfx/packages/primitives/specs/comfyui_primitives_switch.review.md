# Adversarial Review: comfyui_primitives_switch

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- any 类型接线：使用 `core.anytype.any_type`，ComfyUI 接受任意上游类型。
- §7.1 索引越界：clamp 到 [0,7]，有测试。
- §7.2 未连接：抛出 `ValueError`，不静默返回 None，有测试。
- §8.3 假值处理：`0`/`False`/`""` 视为已连接（`is not None`），避免误判。
- §6 无副作用：只读引用，不修改输入。

## 未决疑点
1. 输入顺序依赖节点上 `input1..input8` 的固定命名；未来若升级 `io.Autogrow`，需保持同样的顺序语义。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| index=-1 / 99 | clamp | PASS |
| 选中未连接 | 报错 | PASS |
| 值为 0/False | 正常返回 | PASS |
| 全未连接 first_connected | 报错 | PASS |
