# ComfyUI-Video · 开发记录（DEVLOG）

> 建仓日期：2026-09-24 ｜ 维护：只追加 ｜ 伞仓记录：`../../../DEVLOG.md`

## 1. 使命与边界
- 使命：视频帧处理的统一入口。
- 不负责：音频。
- 来源插件：frame-interpolation、FlashVSR、TeleStyle、mixlab、AGSoft、was。
- 许可：**MIT**。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_video_frame_range` | specs/….md | nodes/frames.py | ….review.md | tests/test_video_frames.py | VERIFY |
| `comfyui_video_pad_frames` | specs/comfyui_video_pad_frames.md | nodes/pad.py | specs/comfyui_video_pad_frames.review.md | tests/test_video_pad.py | VERIFY |

## 3. 里程碑
- M1 — 帧区间选择 | 状态：VERIFY
- M2 — 帧补足（pad_frames） | 状态：VERIFY

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Video 包与开发记录 | SPEC.md | DONE
- 2026-09-24 | Spec-Writer/Implementer/Adversary | frame_range 全链路 PASS | nodes/frames.py, specs/*.md | DONE
- 2026-09-24 | Verifier | frame_range 单测通过 | tests/test_video_frames.py | VERIFY
- 2026-09-24 | Implementer/Spec-Writer/Adversary/Verifier | pad_frames 全链路 PASS（repeat_last/loop） | nodes/pad.py, specs/comfyui_video_pad_frames*.md, nodes/__init__.py, tests/test_video_pad.py | VERIFY
