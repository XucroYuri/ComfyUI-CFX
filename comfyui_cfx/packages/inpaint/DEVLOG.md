# ComfyUI-Inpaint · 开发记录（DEVLOG）

> 建仓日期：2026-09-24 ｜ 维护：只追加 ｜ 伞仓记录：`../../../DEVLOG.md`

## 1. 使命与边界
- 使命：重绘/扩图/crop-stitch 的统一实现。
- 不负责：掩码生成（Segment）、基础几何原语（Primitives）。
- 来源插件：inpainteasy、LanPaint、layerdiffuse、easy-use(**GPL**)、impact-pack(**GPL**)、wlsh(**GPL**)。
- 许可：**MIT**；GPL 只做行为参考。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_inpaint_crop_by_mask` | specs/….md | nodes/crop.py | ….review.md | tests/test_inpaint_crop.py | TODO |

## 3. 里程碑
- M1 — crop-by-mask（纯几何，含 crop data JSON） | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Inpaint 包与开发记录 | SPEC.md | DONE

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| crop/stitch 重复实现多 | 重复 | 先做纯几何的 crop，stitch 复用 Primitives 能力 | WATCH |

## 6. 下一步
1. 实现 `comfyui_inpaint_crop_by_mask`。
