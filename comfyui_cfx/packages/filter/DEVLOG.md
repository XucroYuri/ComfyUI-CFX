# ComfyUI-Filter · 开发记录（DEVLOG）

> 建仓日期：2026-09-24 ｜ 维护：只追加 ｜ 伞仓记录：`../../../DEVLOG.md`

## 1. 使命与边界
- 使命：图像后期/滤镜统一入口。
- 不负责：基础几何原语。
- 来源插件：Image-Filters、was、RES4LYF、mixlab。
- 许可：**MIT**。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_filter_high_pass` | specs/….md | nodes/high_pass.py | ….review.md | tests/test_filter_high_pass.py | VERIFY |

## 3. 里程碑
- M1 — 高斯高通滤镜（确定性） | 状态：VERIFY

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Filter 包与开发记录 | SPEC.md | DONE
- 2026-09-24 | Implementer | 实现高斯高通滤镜（分离式高斯 + 钝化掩蔽） | nodes/high_pass.py | IMPL
- 2026-09-24 | Scribe | 补写契约与对抗性审查并注册节点 | specs/comfyui_filter_high_pass.md, specs/comfyui_filter_high_pass.review.md, nodes/__init__.py | REVIEW
- 2026-09-24 | Verifier | pytest + spec_lint + license_gate + ruff 全绿 | tests/test_filter_high_pass.py | VERIFY
