# Adversarial Review: comfyui_audio_normalize

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 `mode="peak"` 时增益 `target / peak`，输出峰值精确等于 `10 ** (target_dbfs / 20)`，有测试。
- §8.2 `mode="rms"` 且峰值接近满刻度、`target_dbfs=0.0` 时，理论增益会使峰值 > 1.0；`gain * peak > 1.0` 时夹取为 `1.0 / peak`，输出峰值 ≤ 1.0，有测试。
- §8.3 `measured == 0` 提前返回，不做除法，输出与输入逐位相等、长度不变，有测试。
- §8.4 `sample_rate` 在所有返回路径原样带入新 dict，有测试。
- §8.5 只读取 `audio["waveform"]`/`audio["sample_rate"]`，从不写入；`waveform * gain` 生成新张量，输入未变，有测试。
- §8.6 `[1, 2, N]` 立体声经同一标量增益缩放，输出形状不变，有测试。
- §8.7 RMS 模式输出 `torch.isfinite` 全真且峰值 ≤ 1.0，有测试。
- `gain * peak > 1.0` 的判断保证 `peak > 0` 时 `gain <= 1.0 / peak`，输出恒在 ±1.0 内。

## 未决疑点
1. 增益为全局标量（batch/声道共用），非逐声道归一化；AUDIO 常规为 `B=1`，与 trim 的聚合约定一致。
2. `mode` 只识别 `"peak"`，其余值（含 `"rms"`）都走 RMS 分支；ComfyUI 组合框不会产生非法值，故不额外校验。
3. `target_dbfs=0.0` 在 peak 模式下增益 `1/peak`，安静信号会被放幅；由夹取保证不削波，符合"响度优先但不削顶"的语义。
