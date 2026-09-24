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
| `comfyui_audio_trim_silence` | specs/….md | nodes/trim.py | ….review.md | tests/test_audio_trim.py | TODO |

## 3. 里程碑
- M1 — 静音裁剪（确定性） | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Audio 包与开发记录 | SPEC.md | DONE
