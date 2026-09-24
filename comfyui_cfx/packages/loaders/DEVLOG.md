# ComfyUI-Loaders · 开发记录（DEVLOG）

> 建仓日期：2026-09-24 ｜ 维护：只追加 ｜ 伞仓记录：`../../../DEVLOG.md`

## 1. 使命与边界
- 使命：量化/格式加载统一入口。
- 不负责：模型推理。
- 来源插件：ComfyUI-GGUF、ComfyUI-INT8-Fast。
- 许可：**MIT**。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_loaders_gguf_quant_info` | specs/….md | nodes/quant.py | ….review.md | tests/test_loaders_quant.py | TODO |

## 3. 里程碑
- M1 — GGUF 量化元信息解析（纯函数） | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Loaders 包与开发记录 | SPEC.md | DONE
