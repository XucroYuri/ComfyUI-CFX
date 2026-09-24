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
| `comfyui_sampling_split_sigmas` | specs/….md | nodes/sigmas.py | ….review.md | tests/test_sampling_sigmas.py | TODO |

## 3. 里程碑
- M1 — sigma 拆分节点 | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Sampling 包与开发记录 | SPEC.md | DONE
