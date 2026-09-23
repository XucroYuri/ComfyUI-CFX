---
id: comfyui_primitives_mask_ops
display_name: "ComfyUI-Primitives · Mask Ops"
category: "ComfyUI-Primitives/Mask"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "MaskFillHoles / MaskSmoothRegion / MaskDilateRegion (WAS)"
  - "MaskFix+ (essentials)"
  - "AGSoft_Mask_Fix"
  - "ImpactDilateMask (impact-pack)"
---

## 1. 目的
唯一掩码运算节点：阈值化、反相、填洞、模糊、膨胀、收缩。

## 2. 语义
按固定顺序应用：`threshold → invert → fill_holes → blur → grow → shrink`。
- `threshold>=0` 时二值化（`> threshold`）；
- `blur/grow/shrink` 为像素半径，0 表示跳过；
- 输出 clamp 到 [0,1]。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | mask | MASK | 是 | - |
| in | threshold | FLOAT | 否 | -1.0（关闭） |
| in | invert | BOOLEAN | 否 | False |
| in | fill_holes | BOOLEAN | 否 | False |
| in | blur | INT | 否 | 0 |
| in | grow | INT | 否 | 0 |
| in | shrink | INT | 否 | 0 |
| out | mask | MASK | - | - |

## 4. 执行与缓存
确定性；无随机。

## 5. 资源
`grow/shrink` 用 `max_pool2d`；`blur` 用可分离高斯卷积；`fill_holes` 走 `scipy.ndimage`（CPU）。

## 6. 副作用与安全
`fill_holes` 会在 CPU 上处理 numpy 副本，不改动输入张量。

## 7. 错误行为
非 `[H,W]`/`[B,H,W]` → `ValueError`。

## 8. 对抗性反例
1. 全 0 / 全 1；
2. `grow` 与 `shrink` 同时 >0（按顺序都执行）；
3. `blur` 半径大于图像（reflect padding）；
4. 环形掩码 `fill_holes` 后中心为 1；
5. `[H,W]` 二维输入自动升为 `[1,H,W]`。

## 9. 验收
`tests/test_primitives_mask_ops.py`。
