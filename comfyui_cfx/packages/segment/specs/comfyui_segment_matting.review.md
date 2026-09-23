# Adversarial Review: comfyui_segment_matting

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- **许可干净**：使用 MIT 的 `rembg`，未复制 GPL 的 rmbg 代码。
- `alpha_to_mask` 纯函数，有测试（含非 4 通道报错）。
- §8.3 RGBA 输出在 SPEC 明示，避免下游误判通道数。

## 未决疑点
1. `rembg` 为新运行依赖（已安装 2.0.77）；已加入 requirements 说明（见 DEVLOG）。
2. 真实推理未在 CI 覆盖（需下载模型），人工 VERIFY。
3. 输出 IMAGE 为 4 通道；若下游节点不支持 RGBA 请改用 `mask`。
