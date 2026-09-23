# ComfyUI-ControlNet · 开发记录（DEVLOG）

> 建仓日期：2026-09-24 ｜ 维护：只追加 ｜ 伞仓记录：`../../../DEVLOG.md`

## 1. 使命与边界
- 使命：ControlNet/IPAdapter/预处理器的统一契约；保留高可靠上游设计。
- 不负责：语义分割模型本体、深度后处理。
- 来源插件：controlnet_aux(**Apache-2.0**)、advanced-controlnet、ipadapter_plus。
- 许可：**MIT**（包装宽松上游，保留 NOTICE）。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_controlnet_canny` | specs/….md | nodes/canny.py | ….review.md | tests/test_controlnet_canny.py | TODO |

## 3. 里程碑
- M1 — Canny 预处理器（cv2 实现，确定性） | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 ControlNet 包与开发记录 | SPEC.md | DONE

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| controlnet_aux 运行时安装/依赖较重 | 环境脆弱 | 优先用 cv2/自带实现，不依赖其内部 | WATCH |

## 6. 下一步
1. 实现 `comfyui_controlnet_canny`。
