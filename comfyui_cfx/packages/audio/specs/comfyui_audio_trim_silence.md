---
id: comfyui_audio_trim_silence
display_name: "ComfyUI-Audio · Trim Silence"
category: "ComfyUI-Audio/Process"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
裁掉音频首尾的静音段，只保留有效声音及其前后 `pad_ms` 的留白，供下游对齐、拼接或 TTS 后处理使用。

## 2. 语义
- AUDIO 为 dict：`{"waveform": Tensor[B, C, N], "sample_rate": int}`；只读取，不修改。
- 帧长 `frame = max(1, round(sample_rate * min_silence_ms / 1000))`（至少 1 个采样）。
- 帧数 `n_frames = ceil(N / frame)`；不足一帧的尾部用零补齐后再逐帧计算。
- 逐帧 RMS：对每声道在帧内取样点平方均值后开方，再对 batch 与声道求均值，得到一维逐帧能量 `rms`。
- 取 `rms > threshold` 的第一个帧 `first` 与最后一个帧 `last`；无任何帧超阈值 → 原样返回。
- 采样索引：`start = first * frame`，`end = min(N, (last + 1) * frame)`；再两侧各扩 `pad = round(sample_rate * pad_ms / 1000)`，夹取到 `[0, N]`。
- 若裁后区间为整段信号（`start == 0 and end == N`）→ 原样返回。
- 返回**新 dict**：`{"waveform": 切片.contiguous(), "sample_rate": 同一 sample_rate}`。未裁剪时也返回新 dict（waveform 引用同一张量，内容不变）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | audio | AUDIO | 是 | - |
| in | threshold | FLOAT | 是 | 0.01（0.0..1.0，step 0.001，RMS 幅度） |
| in | min_silence_ms | INT | 是 | 100（0..10000） |
| in | pad_ms | INT | 是 | 50（0..10000） |
| out | audio | AUDIO | - | - |

## 4. 执行与缓存
确定性；纯张量运算，无随机、无外部状态、无模型。相同输入与参数 → 相同输出。裁剪结果沿最后一维切片，位运算精确（不插值、不缩放）。

## 5. 资源
输出为 `[B, C, N']`（`N' <= N`）的 `contiguous()` 副本，显存与保留长度成正比；输入张量不被复制、不被修改。

## 6. 副作用与安全
无；不访问文件系统、网络或全局状态；不修改传入的 `audio` dict 或其 `waveform`。

## 7. 错误行为
- `audio` 缺少 `waveform`/`sample_rate` 键 → `KeyError`，不静默降级。
- 非张量 waveform → 由 `pow`/`reshape` 抛出 `AttributeError`/`TypeError`。
- `N == 0`（空波形）→ 无帧超阈值，原样返回空波形。
- 夹取保证切片索引不越界；`min_silence_ms=0` 时 `frame=1`，仍有效。

## 8. 对抗性反例
1. 前静音 + 中段 0.5 幅值 + 后静音 → 输出变短，响段样本逐位保留。
2. 全静音（`threshold > 0`）→ 无帧超阈值，长度不变。
3. 全响（所有帧超阈值）→ `first=0,last=n_frames-1`，夹取后为整段 → 长度不变。
4. `sample_rate` 在裁剪与未裁剪两种情况下均原样保留。
5. 输入 dict 与 waveform 不被就地修改（长度、内容不变）。
6. 双声道 `[1, 2, N]` → 逐声道 RMS 后对声道求均值，输出 `[1, 2, N']`。

## 9. 验收
`tests/test_audio_trim.py`。
