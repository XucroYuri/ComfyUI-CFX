# Adversarial Review: comfyui_primitives_json_bbox

reviewer: Adversary
date: 2026-09-25
verdict: PASS

## 通过项
- §2 条目选择、`bboxes` 优先、polygon 外接框语义与 GroundingDINO / Florence-2 输出一致。
- §2 归一化对倒序坐标生效，`x1 >= x0`、`y1 >= y0` 恒成立。
- §3 输出签名 `("INT","INT","INT","INT","JSON")` / `("x0","y0","x1","y1","bbox")` 与契约一致。
- 确定性、无副作用、不修改输入字典。
- 错误路径均为 `ValueError` 且消息含可用条目数。

## 已证伪项（已在实现中修正）
1. 负数 `index` 会被 Python 负索引静默接受（返回末条）——已改为显式 `index < 0` 判定并在测试中断言。

## 未决疑点
1. `bboxes` 与 `polygons` 同时存在时优先 `bboxes`；若后续需要合并多源标注，另开节点。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 空 `bboxes` | `ValueError`（0） | PASS |
| 越界 `index` | `ValueError` | PASS |
| 两键缺失 | `ValueError` | PASS |
| 倒序 box | 归一化 | PASS |
| 乱序 polygon | 外接框不变 | PASS |
| 浮点坐标 | 就近取整 | PASS |
