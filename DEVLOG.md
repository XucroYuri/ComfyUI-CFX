# ComfyUI-CFX · 开发记录（DEVLOG · 伞仓总账）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 本文件是**汇总索引**，各子包另有自己的 `DEVLOG.md`

## 1. 使命与边界
- 使命：以 Monorepo 承载各 `ComfyUI-<Domain>` 子包，统一 CI / 类型格 / 版本 / 许可门。
- 目录：`custom_nodes/ComfyUI-CFX/`；子包发布名 = `ComfyUI-<Domain>`。
- 开发位置：`D:\Comfy-Desktop\ComfyUI-CFX`（稳定后再 junction 进 `custom_nodes`）。

## 2. 子仓状态总览
| 子仓 | 节点 | 状态 |
|---|---|---|
| ComfyUI-Core | — | ADR-0001/0002 + types/paths/logging/anytype/images |
| ComfyUI-TestKit | — | fixtures/matrix/memory + tools(spec_lint/license_gate/migrate) |
| ComfyUI-Primitives | 14 | ✅ 完成 |
| ComfyUI-Flow | 6 | ✅ 完成 |
| ComfyUI-Vision | 7 | ✅ 完成（L3 通过） |
| ComfyUI-Segment | 6 | ✅ 完成（L3 通过） |
| ComfyUI-Inpaint | 4 | ✅ |
| ComfyUI-ControlNet | 3 | ✅ |
| ComfyUI-Resolve | 2 | ✅（L3 通过） |
| ComfyUI-Depth3D | 2 | ✅ |
| ComfyUI-Sampling | 2 | ✅ |
| ComfyUI-Video | 2 | ✅ |
| ComfyUI-Flux | 2 | ✅ |
| ComfyUI-Audio | 2 | ✅ |
| ComfyUI-Loaders | 2 | ✅ |
| ComfyUI-Filter | 2 | ✅ |
| **合计** | **56** | 347 单测；L3 9 项；画布实测通过 |

## 3. 决策索引（ADR）
- ADR-0001 统一类型格 → `core/docs/adr/0001-type-lattice.md`
- ADR-0002 依赖与 transformers 基线 → `core/docs/adr/0002-dependency-baseline.md`

## 4. 全局变更日志（追加）
- 2026-09-23 | Architect | 建立伞仓骨架（core/testkit/4×P0 包 + tools + CI + DEVLOG） | 本仓 | DONE
- 2026-09-23 | Architect | 重构为 `__init__.py` 薄壳 + 可导入 `comfyui_cfx` 包，解决 pytest 收集冲突 | 本仓 | DONE
- 2026-09-23 | Verifier | 10 项单测通过；spec_lint / license_gate 通过 | 本仓 | DONE
- 2026-09-23 | Implementer | 首个模板节点 image_resize 全链路跑通 | packages/primitives | DONE
- 2026-09-23 | Implementer | M2：switch/boolean/math/text 四节点完成并过审查 | packages/primitives | DONE
- 2026-09-23 | Implementer | M3：crop/transform/stitch/mask_ops 完成 | packages/primitives | DONE
- 2026-09-23 | Implementer | M4：batch/split/seed/resolution/save 完成，primitives 收口（14 节点） | packages/primitives | VERIFY
- 2026-09-24 | Implementer | P1 首节点：resolve scale / controlnet canny / inpaint crop-by-mask | packages/* | DONE
- 2026-09-24 | Implementer | P1 次节点：lineart / inpaint stitch / resolve tiled upscale | packages/* | DONE
- 2026-09-24 | Implementer | P2 骨架 + 首节点：depth3d / sampling / video / flux | packages/* | DONE
- 2026-09-24 | Verifier | L3 真实验证 9 项全部通过；修复 9 处节点缺陷（含 5 处 clamp-on-ndarray，抽 `core.images`） | tools/verify/*, packages/* | DONE
- 2026-09-24 | Integrator | 建立 GitHub 远端并推送（private，main） | https://github.com/XucroYuri/ComfyUI-CFX | DONE
- 2026-09-24 | Implementer | P3 骨架 + 首节点（audio/loaders/filter）+ 各包深化 8 节点，共 56 节点 | packages/* | DONE
- 2026-09-24 | Integrator | 收尾：README 安装/启用文档；junction 接入 custom_nodes；**画布实测两条链路通过** | README.md, tools/verify/canvas_smoke.py | DONE
- 2026-09-25 | Implementer | 深化模型类：BLIP2 / Florence-2 区域 / SAM2 自动分割 / SEGS 双向（L3 新增 3 项） | packages/* | DONE
- 2026-09-25 | Implementer | 新增桥接节点 `comfyui_primitives_json_bbox`（检测 JSON → 4×INT） | packages/primitives | DONE
- 2026-09-25 | Verifier | **跨节点串联验证 3 条链通过**（Vision 内部 / Segment 内部 / 跨包），并修掉 5 处集成层问题 | tools/verify/canvas_chains.py | DONE

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| GPL/无证来源 | 许可污染 | `tools/license_gate.py` + Community 隔离 | WATCH |
| 模型类节点依赖上游后端（florence2/SAM2/AutoCropFaces） | 上游改签名会破坏 | 后端适配器 + `CFX_*_DIR` 覆盖 | WATCH |

## 6. 下一步
1. 继续深化模型类节点（Vision/Segment）并按需补 L3；
2. CI 首次运行确认（ruff/spec_lint/license_gate/test-pure/test-full）；
3. 可选：仓库转公开、加 Release（v0.1.0）。
