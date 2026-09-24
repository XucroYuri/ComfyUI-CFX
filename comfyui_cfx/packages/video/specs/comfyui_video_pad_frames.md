---
id: comfyui_video_pad_frames
display_name: "ComfyUI-Video · Pad Frames"
category: "ComfyUI-Video/Frames"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
把视频图像序列（批次）补足到目标帧数，供需要固定长度（如 81 帧）的下游补帧/生成节点使用。

## 2. 语义
- 用 `ensure_image` 归一为 `[B, H, W, C]` float32，`B = image.shape[0]`。
- 若 `B >= count`：不再补帧，原样返回归一化后的批次。
- 否则补 `missing = count - B` 帧，使输出批次恰好为 `count` 帧：
  - `repeat_last`：重复最后一帧 `img[-1:]` 共 `missing` 次；
  - `loop`：从起始帧循环，依次取 `img[:take]` 切片直至补满（`take = min(B, remaining)`）。
- 输出为 `torch.cat((img, pad), dim=0).contiguous()`，恒为连续 BHWC。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | count | INT | 是 | 81（1..100000） |
| in | mode | COMBO | 是 | repeat_last（repeat_last / loop） |
| out | image | IMAGE | - | - |

## 4. 执行与缓存
确定性；纯张量拼接。

## 5. 资源
输出为 `count` 帧的新连续张量，显存与 `count` 成正比；输入不被复制/修改。

## 6. 副作用与安全
无；不访问文件系统。

## 7. 错误行为
- 非张量或 channel 维度非法 → `TypeError`/`ValueError`（`ensure_image`）。
- 空批次（`B == 0`）且 `count >= 1` → `ValueError("pad_frames: empty image batch")`，不返回错误长度的张量。
- 未知 `mode` → `ValueError`（COMBO 已约束，直接调用时兜底）。

## 8. 对抗性反例
1. `B=4, count=10, mode=repeat_last` → 输出 10 帧，第 4..9 帧均等于 `img[-1]`；
2. `B=3, count=8, mode=loop` → 输出帧序 `[0,1,2,0,1,2,0,1]`，补的第一帧等于 `img[0]`；
3. `B=6, count=6` → 原样返回，shape 不变；
4. `B=6, count=3` → `B >= count`，原样返回，不截断；
5. 原有 `0..B-1` 帧内容与输入逐元素相等（补帧不触碰原帧）；
6. `count` 远大于 `B` 时 `loop` 多轮循环仍恰好补满 `count` 帧。

## 9. 验收
`tests/test_video_pad.py`。
