# ComfyUI-Sampling · 开发记录（DEVLOG）

> 建仓日期：2026-09-24 ｜ 维护：只追加 ｜ 伞仓记录：`../../../DEVLOG.md`

## 1. 使命与边界
- 使命：sigma/调度操作与细节增强的规范化。
- 不负责：基础 KSampler。
- 来源插件：RES4LYF、detail-daemon、LanPaint（许可待审计）。
- 许可：**MIT**。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_sampling_split_sigmas` | specs/….md | nodes/sigmas.py | ….review.md | tests/test_sampling_sigmas.py | VERIFY |
| `comfyui_sampling_sigma_shift` | specs/….md | nodes/shift.py | ….review.md | tests/test_sampling_shift.py | VERIFY |

## 3. 里程碑
- M1 — sigma 拆分节点 | 状态：VERIFY

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Sampling 包与开发记录 | SPEC.md | DONE
- 2026-09-24 | Spec-Writer | split_sigmas 契约：前/后缀切片、边界与错误行为 | specs/comfyui_sampling_split_sigmas.md | DONE
- 2026-09-24 | Implementer | 实现 CFXSplitSigmas 并注册进 sampling 节点表 | nodes/sigmas.py, nodes/__init__.py | DONE
- 2026-09-24 | Adversary | 对抗性审查通过 | specs/comfyui_sampling_split_sigmas.review.md | DONE
- 2026-09-24 | Verifier | 单测覆盖切片/边界/dtype/错误路径 | tests/test_sampling_sigmas.py | VERIFY
- 2026-09-24 | Spec-Writer | sigma_shift 契约：整体缩放、单位元与错误行为 | specs/comfyui_sampling_sigma_shift.md | DONE
- 2026-09-24 | Implementer | 实现 CFXSigmaShift 并注册进 sampling 节点表 | nodes/shift.py, nodes/__init__.py | DONE
- 2026-09-24 | Adversary | 对抗性审查通过 | specs/comfyui_sampling_sigma_shift.review.md | DONE
- 2026-09-24 | Verifier | 单测覆盖缩放/单位元/dtype/不可变性/错误路径 | tests/test_sampling_shift.py | VERIFY
