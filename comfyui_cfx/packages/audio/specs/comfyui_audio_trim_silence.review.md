# Adversarial Review: comfyui_audio_trim_silence

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 有静音首尾的合成波形裁剪后变短，且响段与 `waveform[..., start:end]` 逐位相等，有测试。
- §8.2 全静音 → `active.any()` 为假，走原样返回分支，长度不变，有测试。
- §8.3 全响 → `start==0 and end==N`，走原样返回分支，长度不变，有测试。
- §8.4 `sample_rate` 在裁剪与未裁剪两条路径都被原样带入新 dict，有测试。
- §8.5 只读取 `audio["waveform"]`/`audio["sample_rate"]`，从不写入，返回新 dict；有测试校验输入未变。
- §8.6 双声道 `[1, 2, N]`：逐声道帧 RMS 后对声道与 batch 求均值，输出 `[1, 2, N']`，有测试。
- `frame = max(1, ...)` 覆盖 `min_silence_ms=0`；尾部不足一帧用零补齐，不越界。

## 未决疑点
1. 跨 batch (`B > 1`) 时用 batch 均值决定单一裁剪区间，属有意的聚合约定；AUDIO 常规为 `B=1`。
2. `threshold=0.0` 时理论上要求 RMS 严格大于 0 才算有声；纯零信号的静音帧不会被选中，符合"无超阈值帧 → 原样"语义。
3. `min_silence_ms` 非整数倍采样率时按四舍五入取整到最近采样，已文档化。
