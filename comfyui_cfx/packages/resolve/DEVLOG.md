# ComfyUI-Resolve · 开发记录（DEVLOG）

> 建仓日期：2026-09-24 ｜ 维护：只追加 ｜ 伞仓记录：`../../../DEVLOG.md`

## 1. 使命与边界
- 使命：分辨率/总像素/放大的端到端图像操作。
- 不负责：纯分辨率计算（Primitives）、掩码/模型加载。
- 来源插件：UltimateSDUpscale、Resolution-Master、find-perfect-resolution、scale-to-total-pixels、wlsh(**GPL**)、efficiency、Comfyroll(**无证**)。
- 许可：**MIT**；GPL/无证只做行为参考。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_resolve_scale_to_megapixels` | specs/….md | nodes/scale.py | ….review.md | tests/test_resolve_scale.py | TODO |

## 3. 里程碑
- M1 — 总像素缩放节点全链路 | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Resolve 包与开发记录 | SPEC.md | DONE

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| 与 Primitives 的职责重叠 | 重复 | 纯计算留 Primitives，本包只做端到端图像操作 | WATCH |

## 6. 下一步
1. 实现 `comfyui_resolve_scale_to_megapixels`。
