---
id: comfyui_audio_normalize
display_name: "ComfyUI-Audio · Normalize"
category: "ComfyUI-Audio/Process"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
把一段音频的响度抬升或压低到指定 dBFS 目标，供拼接、混音或下游分析前做统一电平，同时保证不削波。

## 2. 语义
- AUDIO 为 dict：`{"waveform": Tensor[B, C, N], "sample_rate": int}`；只读取，不修改。
- 依据 `mode` 取测度：`"peak"` → `peak = waveform.abs().max()`；`"rms"` → `rms = waveform.pow(2).mean().sqrt()`。
- 目标幅度 `target = 10 ** (target_dbfs / 20)`（`target_dbfs <= 0` ⇒ `target <= 1.0`）。
- 若测度 `measured == 0`（纯静音）→ 原样返回，不做除法：返回新 dict，`waveform` 引用同一张量、内容不变。
- 否则增益 `gain = target / measured`；若 `gain * peak > 1.0` 则夹取 `gain = 1.0 / peak`，保证输出绝对值不超过 ±1.0（不削波、不静默削顶）。
- 返回**新 dict**：`{"waveform": waveform * gain, "sample_rate": 同一 sample_rate}`；`waveform * gain` 生成新张量，输入不被就地修改。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | audio | AUDIO | 是 | - |
| in | target_dbfs | FLOAT | 是 | -1.0（-60.0..0.0，step 0.1） |
| in | mode | COMBO `["peak","rms"]` | 是 | "peak" |
| out | audio | AUDIO | - | - |

## 4. 执行与缓存
确定性；纯张量运算，无随机、无外部状态、无模型。相同输入与参数 → 相同输出。增益为标量，逐样本等比缩放。

## 5. 资源
输出形状与输入相同 `[B, C, N]`，为 `waveform * gain` 的新张量，显存与输入同阶；输入张量不被复制、不被修改。

## 6. 副作用与安全
无；不访问文件系统、网络或全局状态；不修改传入的 `audio` dict 或其 `waveform`。

## 7. 错误行为
- `audio` 缺少 `waveform`/`sample_rate` 键 → `KeyError`，不静默降级。
- 非张量 waveform → 由 `abs`/`pow` 抛出 `AttributeError`/`TypeError`。
- `N == 0`（空波形）→ `"peak"` 模式 `max()` 抛出 `RuntimeError`；`"rms"` 模式测度为 `nan`，输出仍为空张量。
- 未知 `mode`（非 `"peak"`）→ 按 RMS 分支计算；ComfyUI 组合框不会产生该值。
- 夹取保证 `peak > 0` 时 `gain <= 1.0 / peak`，输出恒在 ±1.0 内。

## 8. 对抗性反例
1. `mode="peak"`、安静信号 → `max(abs(out)) ≈ 10 ** (target_dbfs / 20)`。
2. `mode="rms"`、峰值已接近满刻度但 RMS 较小的信号、`target_dbfs=0.0` → 理论增益使峰值超过 1.0，夹取后 `max(abs(out)) <= 1.0`。
3. 纯静音（`measured == 0`）→ 原样返回，长度与内容不变。
4. `sample_rate` 在所有路径原样保留。
5. 输入 dict 与 waveform 不被就地修改（内容与形状不变）。
6. 多声道 `[1, 2, N]` → 单一标量增益作用于全部声道，输出形状不变。
7. RMS 测度下输出为有限值且 `max(abs(out)) <= 1.0`。

## 9. 验收
`tests/test_audio_normalize.py`。
