# ComfyUI-CFX · 开发记录（DEVLOG · 伞仓总账）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 本文件是**汇总索引**，各子包另有自己的 `DEVLOG.md`

## 1. 使命与边界
- 使命：以 Monorepo 承载各 `ComfyUI-<Domain>` 子包，统一 CI / 类型格 / 版本 / 许可门。
- 目录：`custom_nodes/ComfyUI-CFX/`；子包发布名 = `ComfyUI-<Domain>`。
- 开发位置：`D:\Comfy-Desktop\ComfyUI-CFX`（稳定后再 junction 进 `custom_nodes`）。

## 2. 子仓状态总览
| 子仓 | 优先级 | 里程碑 | 状态 |
|---|---|---|---|
| ComfyUI-Core | P0 | ADR-0001/0002 + 类型格 | IMPL |
| ComfyUI-TestKit | P0 | fixtures/matrix/memory | IMPL |
| ComfyUI-Primitives | P0 | image_resize 模板链路 | VERIFY |
| ComfyUI-Flow | P0 | wrap rgthree | TODO |
| ComfyUI-Vision | P0 | Loader + Florence-2 Tasks | TODO |
| ComfyUI-Segment | P0 | Loader + Detect + Mask | TODO |
| ComfyUI-Resolve / ControlNet / Inpaint | P1 | — | TODO |
| ComfyUI-Depth3D / Sampling / Video / Flux | P2 | — | TODO |
| ComfyUI-Audio / Loaders / Filter | P3 | — | TODO |

## 3. 决策索引（ADR）
- ADR-0001 统一类型格 → `core/docs/adr/0001-type-lattice.md`
- ADR-0002 依赖与 transformers 基线 → `core/docs/adr/0002-dependency-baseline.md`

## 4. 全局变更日志（追加）
- 2026-09-23 | Architect | 建立伞仓骨架（core/testkit/4×P0 包 + tools + CI + DEVLOG） | 本仓 | DONE
- 2026-09-23 | Architect | 重构为 `__init__.py` 薄壳 + 可导入 `comfyui_cfx` 包，解决 pytest 收集冲突 | 本仓 | DONE
- 2026-09-23 | Verifier | 10 项单测通过；spec_lint / license_gate 通过 | 本仓 | DONE
- 2026-09-23 | Implementer | 首个模板节点 image_resize 全链路跑通 | packages/primitives | DONE
- 2026-09-23 | Implementer | M2：switch/boolean/math/text 四节点完成并过审查 | packages/primitives | VERIFY

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| GPL/无证来源 | 许可污染 | `tools/license_gate.py` + Community 隔离 | WATCH |

## 6. 下一步
1. 完成 `core` 与 `testkit` 最小实现并跑测试；
2. 落地首个模板节点 `comfyui_primitives_image_resize` 全链路。
