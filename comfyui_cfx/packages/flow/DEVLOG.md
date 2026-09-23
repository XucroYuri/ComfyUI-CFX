# ComfyUI-Flow · 开发记录（DEVLOG）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 伞仓记录：`../../DEVLOG.md`

## 1. 使命与边界
- 使命：连线/广播/上下文/控制流/UI 辅助的规范化与统一契约。
- 不负责：图像/模型推理原语。
- 来源插件：rgthree(**MIT**)、cg-use-everywhere(**Apache-2.0**)、custom-scripts/pysssss(**MIT**)。
- 许可：**MIT**（可包装宽松上游，保留署名/NOTICE）。

## 2. 状态看板
| 模块 | 策略 | 来源 | 状态 |
|---|---|---|---|
| Context / Context Big / Merge / Switch | KEEP-DESIGN 包装 | rgthree | TODO |
| Any Switch / Seed / Power Primitive / Power Puter | KEEP-DESIGN 包装 | rgthree | TODO |
| Display Any/Int（并入 Show Text） | 合并 | rgthree+pysssss | TODO |
| Reroute / 静音旁路编排 / 进度条 / Link Fixer | KEEP-DESIGN 包装 | rgthree | TODO |
| Anything Everywhere / Combo Clone / 虚拟连线引擎 | KEEP-DESIGN **隔离**包装 | cg-use-everywhere | TODO |
| StringFunction / Load-SaveText / ConstrainImage / Repeater / PlaySound / SystemNotification | REIMPLEMENT | pysssss | TODO |
| `pysssss.binding` 控件绑定 DSL | 保留概念重实现 | pysssss | TODO |

## 3. 里程碑
- M1 — 成功 wrap rgthree 且旧 `class_type` 不变 | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-23 | Architect | 建立 Flow 包与开发记录，确定 wrap/隔离/重实现三分法 | SPEC.md | DONE

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| cg-use-everywhere 前端变动（已到 8.0/Nodes 2.0） | 包装层易碎 | 隔离层 + 锁定兼容版本 | WATCH |
| rgthree 大量 monkey-patch | 升级易破坏 | 固定版本 + 冒烟工作流 | WATCH |

## 6. 下一步
1. 列 rgthree 需包装节点与其 `class_type` 快照；
2. 定义 wrap 边界（禁跨模块全局状态）。
