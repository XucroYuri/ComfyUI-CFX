# ComfyUI-TestKit · 开发记录（DEVLOG）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 伞仓记录：`../../DEVLOG.md`

## 1. 使命与边界
- 使命：可复用测试基建（夹具 / dtype-device 矩阵 / 显存回归 / 金标准工作流夹具 / 规范与许可校验工具）。
- 不负责：业务节点；不依赖任何具体域包。
- 许可：**MIT**。

## 2. 状态看板
| 模块 | 实现 | 状态 |
|---|---|---|
| `fixtures.py` | testkit/fixtures.py | IMPL |
| `matrix.py` | testkit/matrix.py | IMPL |
| `memory.py` | testkit/memory.py | IMPL |
| `golden.py` | — | TODO |
| `tools/spec_lint.py` | tools/spec_lint.py | IMPL |
| `tools/license_gate.py` | tools/license_gate.py | IMPL |

## 3. 里程碑
- M1 — `spec_lint` + `license_gate` 可在 CI 拦截缺 SPEC / 非 MIT 包 | 状态：IMPL

## 4. 变更日志（追加）
- 2026-09-23 | Implementer | 落地 fixtures/matrix/memory 与两个校验工具 | testkit/, tools/ | IMPL

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| CI 无 GPU | dtype 矩阵未覆盖 CUDA | CPU 必测，CUDA 定时/可选 | WATCH |

## 6. 下一步
1. 实现 `golden.py`（最小 PromptExecutor 夹具）；
2. 补 `specs/*.md`。
