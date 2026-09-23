---
id: comfyui_primitives_seed
display_name: "ComfyUI-Primitives · Seed"
category: "ComfyUI-Primitives/Seed"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Seed (rgthree)"
  - "CR Seed (Comfyroll)"
  - "Seed Generator (comfy-image-saver)"
  - "WAS Seed"
---

## 1. 目的
唯一 seed 节点，显式控制固定/随机/递增/递减。

## 2. 语义
- `fixed`：原样返回；
- `randomize`：返回 `[0, 2^64-1]` 均匀随机；
- `increment` / `decrement`：在 `[0, 2^64-1]` 上环形加减 1。

`control != fixed` 时 `IS_CHANGED` 返回 `NaN` 强制每次重算。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | seed | INT | 是 | 0 |
| in | control | COMBO | 是 | fixed |
| out | seed | INT | - | - |

## 4. 执行与缓存
非 fixed 时强制重算（`NaN != NaN`）；fixed 时以 seed 值参与缓存键。

## 5. 资源
纯 Python。

## 6. 副作用与安全
使用模块级 `random`；不改全局随机状态语义（不影响 torch seed）。

## 7. 错误行为
无（输入越界由 widget 约束）。

## 8. 对抗性反例
1. `seed=MAX` 时 increment 回到 0（环形）；
2. `seed=0` 时 decrement 回到 MAX；
3. `fixed` 两次执行结果相同；
4. `randomize` 的 `IS_CHANGED` 为 NaN。

## 9. 验收
`tests/test_primitives_seed.py`。
