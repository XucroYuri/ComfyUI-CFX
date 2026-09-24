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
| `comfyui_resolve_scale_to_megapixels` | specs/comfyui_resolve_scale_to_megapixels.md | nodes/scale.py | specs/comfyui_resolve_scale_to_megapixels.review.md | tests/test_resolve_scale.py | VERIFY |
| `comfyui_resolve_upscale_tiled` | specs/comfyui_resolve_upscale_tiled.md | nodes/upscale.py | specs/comfyui_resolve_upscale_tiled.review.md | tests/test_resolve_upscale.py | VERIFY |

## 3. 里程碑
- M1 — 总像素缩放节点全链路 | 状态：VERIFY

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Resolve 包与开发记录 | SPEC.md | DONE
- 2026-09-24 | Spec-Writer | 编写总像素缩放合约与对抗审查 | specs/comfyui_resolve_scale_to_megapixels.md, specs/comfyui_resolve_scale_to_megapixels.review.md | REVIEW
- 2026-09-24 | Implementer | 实现并注册总像素缩放节点 | nodes/scale.py, nodes/__init__.py | IMPL
- 2026-09-24 | Adversary | 对抗性审查（反例与许可） | specs/comfyui_resolve_scale_to_megapixels.review.md | REVIEW
- 2026-09-24 | Verifier | 运行单测/spec_lint/license_gate | tests/test_resolve_scale.py | VERIFY
- 2026-09-24 | Spec-Writer | 编写分块放大合约与对抗审查 | specs/comfyui_resolve_upscale_tiled.md, specs/comfyui_resolve_upscale_tiled.review.md | REVIEW
- 2026-09-24 | Implementer | 实现并注册分块放大节点 | nodes/upscale.py, nodes/__init__.py | IMPL
- 2026-09-24 | Verifier | 运行单测/spec_lint/license_gate | tests/test_resolve_upscale.py | VERIFY

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| 与 Primitives 的职责重叠 | 重复 | 纯计算留 Primitives，本包只做端到端图像操作 | WATCH |

## 6. 下一步
1. 实现 `comfyui_resolve_scale_to_megapixels`。
