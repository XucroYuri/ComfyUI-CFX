# ComfyUI-Depth3D · 开发记录（DEVLOG）

> 建仓日期：2026-09-24 ｜ 维护：只追加 ｜ 伞仓记录：`../../../DEVLOG.md`

## 1. 使命与边界
- 使命：深度结果处理与 3D 出口。
- 不负责：ControlNet 深度预处理器。
- 来源插件：DepthAnythingV3、controlnet_aux、mixlab。
- 许可：**MIT**。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_depth3d_normalize_depth` | specs/….md | nodes/normalize.py | ….review.md | tests/test_depth3d_normalize.py | VERIFY |
| `comfyui_depth3d_colormap` | specs/….md | nodes/colormap.py | ….review.md | tests/test_depth3d_colormap.py | VERIFY |

## 3. 里程碑
- M1 — 深度归一化节点 | 状态：VERIFY
- M2 — 深度着色节点 | 状态：VERIFY

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Depth3D 包与开发记录 | SPEC.md | DONE
- 2026-09-24 | Implementer | 实现深度归一化节点（minmax/clamp + invert，IMAGE+MASK） | nodes/normalize.py | IMPL
- 2026-09-24 | Scribe | 补写契约与对抗性审查并注册节点 | specs/comfyui_depth3d_normalize_depth.md, specs/comfyui_depth3d_normalize_depth.review.md, nodes/__init__.py | REVIEW
- 2026-09-24 | Verifier | pytest + spec_lint + license_gate 全绿 | tests/test_depth3d_normalize.py | VERIFY
- 2026-09-24 | Spec-Writer | 补写 colormap 契约与对抗性反例 | specs/comfyui_depth3d_colormap.md | SPEC
- 2026-09-24 | Implementer | 实现 CFXDepthColormap（gray 直出 + matplotlib 色标） | nodes/colormap.py | IMPL
- 2026-09-24 | Adversary | 审查并给出 verdict PASS | specs/comfyui_depth3d_colormap.review.md | REVIEW
- 2026-09-24 | Verifier | pytest + spec_lint + license_gate + ruff 全绿 | tests/test_depth3d_colormap.py, nodes/__init__.py | VERIFY
