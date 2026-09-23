# ComfyUI-Core · 开发记录（DEVLOG）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 伞仓记录：`../../DEVLOG.md`

## 1. 使命与边界
- 使命：唯一类型格 + 设备/dtype/显存/路径安全/日志底座，被所有 `ComfyUI-*` 依赖。
- 不负责：任何业务节点；**不 import `transformers`**。
- 许可：**MIT**。

## 2. 状态看板
| 模块 | SPEC | 实现 | 审查 | 状态 |
|---|---|---|---|---|
| ADR-0001 类型格 | docs/adr/0001-type-lattice.md | — | — | DONE |
| ADR-0002 依赖基线 | docs/adr/0002-dependency-baseline.md | — | — | DONE |
| `types.py` | specs/types.md（待补） | core/types.py | — | IMPL |
| `device.py` | specs/device.md（待补） | core/device.py | — | IMPL |
| `paths.py` | specs/paths.md（待补） | core/paths.py | — | IMPL |
| `logging.py` | specs/logging.md（待补） | core/logging.py | — | IMPL |
| `anytype.py` | — | core/anytype.py | — | IMPL |

## 3. 里程碑
- M1 — ADR-0001/0002 定稿 + types/device/memory/paths 可用 | 状态：IMPL（等测试）

## 4. 变更日志（追加）
- 2026-09-23 | Architect | 冻结 ADR-0001/0002 | core/docs/adr | DONE
- 2026-09-23 | Implementer | 实现 types/device/paths/logging | core/*.py | IMPL
- 2026-09-23 | Implementer | 新增 anytype.py；移除未被调用的 memory.py（无死代码） | core/ | DONE

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| 类型格冻结前其它库先行 | 接口分叉 | Core 单写者，先冻结再并行 | CLOSED（ADR 已定稿） |

## 6. 下一步
1. 补 `specs/*.md` 契约；
2. 为 `types`/`paths` 添加单测。
