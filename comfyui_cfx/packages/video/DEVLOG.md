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
| `comfyui_video_frame_range` | specs/….md | nodes/frames.py | ….review.md | tests/test_video_frames.py | TODO |

## 3. 里程碑
- M1 — 帧区间选择 | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-24 | Architect | 建立 Video 包与开发记录 | SPEC.md | DONE
