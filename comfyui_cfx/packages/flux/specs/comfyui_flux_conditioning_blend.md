---
id: comfyui_flux_conditioning_blend
display_name: "ComfyUI-Flux · Conditioning Blend"
category: "ComfyUI-Flux/Conditioning"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "ConditioningKrea2Rebalance"
---

## 1. 目的
按线性系数融合两份 CONDITIONING（Flux/Krea2 条件再平衡的最小原语）。

## 2. 语义
- CONDITIONING 是 `[ [tensor, dict], ... ]` 列表。
- 要求两份输入均为**非空列表**且**长度相同**，否则 `ValueError`。
- 逐对计算：`blended = tensor_a * (1 - factor) + tensor_b.to(dtype=a.dtype, device=a.device) * factor`。
- 元数据保留 `a` 的 `dict`（浅拷贝，避免污染输入）。
- `factor=0` 等价于 `a` 的 tensor；`factor=1` 把 `b` 的值（转换到 `a` 的 dtype/device）混入。
- 返回新的列表，不共享 `a`/`b` 的条目对象。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | conditioning_a | CONDITIONING | 是 | - |
| in | conditioning_b | CONDITIONING | 是 | - |
| in | factor | FLOAT | 是 | 0.5（0.0..1.0，步长 0.01） |
| out | conditioning | CONDITIONING | - | - |

## 4. 执行与缓存
确定性；无状态；无随机数。

## 5. 资源
逐条新建张量，显存约等于输出 conditioning；`b` 的 dtype/device 转换会临时复制。

## 6. 副作用与安全
不修改输入（`dict` 浅拷贝）；不写文件；不触网。

## 7. 错误行为
- 非 `list` 输入 → `ValueError`；
- 空列表 → `ValueError`；
- 长度不一致 → `ValueError`。

## 8. 对抗性反例
1. `factor=0` → 张量等于 `a`；
2. `factor=1` → 张量等于 `b` 的值（dtype 转为 `a`）；
3. `factor=0.5` 且 `a=0`、`b=1` → 全 0.5；
4. `b` 为 float64 → 输出保持 `a` 的 float32；
5. 修改输出元数据 → 不影响输入 `dict`。

## 9. 验收
`tests/test_flux_blend.py`。
