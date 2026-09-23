# ComfyUI-Flow · 开发记录（DEVLOG）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 伞仓记录：`../../DEVLOG.md`

## 1. 使命与边界
- 使命：连线/广播/上下文/控制流/UI 辅助的规范化与统一契约。
- 不负责：图像/模型推理原语。
- 来源插件：rgthree(**MIT**)、cg-use-everywhere(**Apache-2.0**)、custom-scripts/pysssss(**MIT**)。
- 许可：**MIT**（可包装宽松上游，保留署名/NOTICE）。

## 2. 状态看板
| 节点 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_flow_string_function` | specs/….md | nodes/string_function.py | ….review.md | tests/test_flow_string_function.py | VERIFY |
| `comfyui_flow_show_text` | specs/….md | nodes/show_text.py | ….review.md | tests/test_flow_show_text.py | VERIFY |
| `comfyui_flow_constrain_image` | specs/….md | nodes/constrain_image.py | ….review.md | tests/test_flow_constrain_image.py | VERIFY |
| `comfyui_flow_repeater` | specs/….md | nodes/repeater.py | ….review.md | tests/test_flow_repeater.py | VERIFY |
| `comfyui_flow_load_text` | specs/….md | nodes/text_file.py | ….review.md | tests/test_flow_text_file.py | VERIFY |
| `comfyui_flow_save_text` | specs/….md | nodes/text_file.py | ….review.md | tests/test_flow_text_file.py | VERIFY |

### 决策：不写包装代码
- `rgthree` / `cg-use-everywhere`：**推荐可选依赖**，不包装、不复制（避免耦合其前端注入）。
- **不移植** `PlaySound` / `SystemNotification`（OS 副作用、低价值、额外依赖）。

## 3. 里程碑
- M1 — pysssss 子集（6 节点）完成并通过审查/测试 | 状态：VERIFY
- M2 — 文档化 rgthree / cg-use-everywhere 兼容边界 | 状态：DONE

## 4. 变更日志（追加）
- 2026-09-23 | Architect | 建立 Flow 包与开发记录 | SPEC.md | DONE
- 2026-09-23 | Architect | 决策：不写包装代码，只重写 pysssss 薄节点；不移植 PlaySound/SystemNotification | SPEC.md | DONE
- 2026-09-23 | Spec-Writer/Implementer/Adversary | string_function/show_text/constrain_image/repeater/load_text/save_text 全链路 PASS | nodes/*.py, specs/*.md | DONE
- 2026-09-23 | Verifier | 6 节点单测通过 | tests/test_flow_*.py | VERIFY

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| cg-use-everywhere 前端变动（已到 8.0/Nodes 2.0） | 包装层易碎 | 隔离层 + 锁定兼容版本 | WATCH |
| rgthree 大量 monkey-patch | 升级易破坏 | 固定版本 + 冒烟工作流 | WATCH |

## 6. 下一步
1. 列 rgthree 需包装节点与其 `class_type` 快照；
2. 定义 wrap 边界（禁跨模块全局状态）。
