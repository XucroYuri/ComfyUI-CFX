---
id: comfyui_video_frame_range
display_name: "ComfyUI-Video · Frame Range"
category: "ComfyUI-Video/Frames"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
从视频图像序列（批次）中按帧号区间选取一段，供下游补帧/超分/风格化使用。

## 2. 语义
- 用 `ensure_image` 归一为 `[B, H, W, C]` float32，`B = image.shape[0]`。
- `stop < 0` 或 `stop > B` → `stop = B`（-1 表示"到结尾"）。
- `start` 夹取到 `[0, B]`。
- 若 `start >= stop` → `ValueError("frame_range: empty range")`。
- 返回 `image[start:stop:step].contiguous()`，步长为 `step`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | start | INT | 是 | 0（0..100000） |
| in | stop | INT | 是 | -1（-1..100000） |
| in | step | INT | 是 | 1（1..1000） |
| out | image | IMAGE | - | - |

## 4. 执行与缓存
确定性；纯切片。

## 5. 资源
输出为切片的 `contiguous()` 副本，显存与选中帧数成正比；输入不被复制。

## 6. 副作用与安全
无；不访问文件系统。

## 7. 错误行为
- 非张量或 channel 维度非法 → `TypeError`/`ValueError`（`ensure_image`）。
- `start >= stop`（含 `start` 越界夹取后、空批次）→ `ValueError("frame_range: empty range")`。

## 8. 对抗性反例
1. `start=2, stop=6` → 取第 2..5 帧（不含 6）；
2. `stop=-1` → 取到最后一帧；
3. `step=2` → 每隔一帧采样；
4. `stop > B` → 夹取到 B，不越界；
5. `start >= stop` → 抛 `ValueError`，不返回空张量；
6. `start > B` → 夹取到 B 后与 stop 比较，仍为空则报错。

## 9. 验收
`tests/test_video_frames.py`。
