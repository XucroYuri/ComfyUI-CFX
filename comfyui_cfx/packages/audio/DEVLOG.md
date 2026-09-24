# ComfyUI-Audio · 开发记录（DEVLOG）

> 建仓日期：2026-09-24 ｜ 维护：只追加 ｜ 伞仓记录：`../../../DEVLOG.md`

## 1. 使命与边界
- 使命：音频/TTS 统一入口（先做确定性音频处理，模型类后置）。
- 不负责：视频画面。
- 来源插件：TTS-Audio-Suite、mixlab(audio)。
- 许可：**MIT**；逐项审计。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_audio_trim_silence` | specs/comfyui_audio_trim_silence.md | nodes/trim.py | specs/comfyui_audio_trim_silence.review.md | tests/test_audio_trim.py | VERIFY |
| `comfyui_audio_normalize` | specs/comfyui_audio_normalize.md | nodes/normalize.py | specs/comfyui_audio_normalize.review.md | tests/test_audio_normalize.py | VERIFY |

## 3. 里程碑
- M1 — 静音裁剪（确定性） | 状态：VERIFY

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Audio 包与开发记录 | SPEC.md | DONE
- 2026-09-24 | Implementer | 实现静音裁剪节点（逐帧 RMS + 首尾响段 + pad，返回新 dict） | nodes/trim.py | IMPL
- 2026-09-24 | Scribe | 补写契约与对抗性审查并注册节点 | specs/comfyui_audio_trim_silence.md, specs/comfyui_audio_trim_silence.review.md, nodes/__init__.py | REVIEW
- 2026-09-24 | Verifier | pytest + spec_lint + license_gate + ruff 全绿 | tests/test_audio_trim.py | VERIFY
- 2026-09-24 | Implementer | 实现响度归一化节点（peak/RMS 测度 + dBFS 目标 + 防削波增益上限，返回新 dict） | nodes/normalize.py | IMPL
- 2026-09-24 | Scribe | 补写契约与对抗性审查并注册节点 | specs/comfyui_audio_normalize.md, specs/comfyui_audio_normalize.review.md, nodes/__init__.py | REVIEW
- 2026-09-24 | Verifier | pytest + spec_lint + license_gate + ruff 全绿 | tests/test_audio_normalize.py | VERIFY
