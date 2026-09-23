---
id: comfyui_primitives_resolution
display_name: "ComfyUI-Primitives · Resolution"
category: "ComfyUI-Primitives/Resolution"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Resolutions by Ratio (WLSH)"
  - "SDXL Resolutions (WLSH)"
  - "CR Aspect Ratio (Comfyroll)"
  - "GetImageSizeRatio (controlaltai)"
  - "AGSoft_Img_Res"
---

## 1. 目的
唯一分辨率/宽高比推导，输出宽高（INT）。

## 2. 语义
- `preset` 提供比例；`orientation` 可交换长边/短边。
- 无覆盖时：按 `megapixels` 与比例解出 `w,h`。
- 覆盖时：给定一侧按比例推导另一侧；两侧都给则直接采用。
- 输出对齐 `multiple_of`，且不低于 `multiple_of`。

**刻意不输出 LATENT**：不同模型族的 latent 通道数不同，硬编码会产出错误结果；
空 latent 交由 ComfyUI 原生空 latent 节点处理。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | preset | COMBO | 是 | 1:1 |
| in | megapixels | FLOAT | 是 | 1.0 |
| in | orientation | COMBO | 是 | landscape |
| in | multiple_of | INT | 是 | 8 |
| in | width_override / height_override | INT | 否 | 0 |
| out | width / height | INT | - | - |

## 4. 执行与缓存
确定性。

## 5. 资源
纯 Python。

## 6. 副作用与安全
无。

## 7. 错误行为
未提供比例与覆盖的合法组合时仍有默认（`1:1`），不报错。

## 8. 对抗性反例
1. `megapixels` 极小 → 由 `_align` 保证 ≥`multiple_of`；
2. 只给 `width_override` → 高度按比例推导；
3. `portrait` 交换长短边；
4. 非法枚举由 widget 约束。

## 9. 验收
`tests/test_primitives_resolution.py`。
