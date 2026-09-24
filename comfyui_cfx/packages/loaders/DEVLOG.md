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
| `comfyui_loaders_gguf_header` | specs/comfyui_loaders_gguf_header.md | nodes/quant.py | comfyui_loaders_gguf_header.review.md | tests/test_loaders_quant.py | VERIFY |
| `comfyui_loaders_safetensors_info` | specs/comfyui_loaders_safetensors_info.md | nodes/safetensors_info.py | comfyui_loaders_safetensors_info.review.md | tests/test_loaders_safetensors.py | VERIFY |

## 3. 里程碑
- M1 — GGUF 量化元信息解析（纯函数） | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Loaders 包与开发记录 | SPEC.md | DONE
- 2026-09-24 | Spec-Writer/Implementer/Adversary | gguf_header 全链路 PASS（仅读头部，路径包含校验） | nodes/quant.py, specs/comfyui_loaders_gguf_header.md | DONE
- 2026-09-24 | Verifier | gguf_header 单测通过 | tests/test_loaders_quant.py | VERIFY
- 2026-09-24 | Spec-Writer/Implementer/Adversary | safetensors_info 全链路 PASS（张量计数/dtype 直方图/元数据键，路径包含校验） | nodes/safetensors_info.py, specs/comfyui_loaders_safetensors_info.md | VERIFY
- 2026-09-24 | Verifier | safetensors_info 单测通过；spec_lint / license_gate / ruff 通过 | tests/test_loaders_safetensors.py | VERIFY
