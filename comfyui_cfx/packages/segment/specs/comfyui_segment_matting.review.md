# Adversarial Review: comfyui_segment_matting

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- **许可干净**：使用 MIT 的 `rembg`，未复制 GPL 的 rmbg 代码。
- `alpha_to_mask` 纯函数，有测试（含非 4 通道报错）。
- §8.3 RGBA 输出在 SPEC 明示，避免下游误判通道数。

## 未决疑点
1. `rembg` 为新运行依赖（已安装 2.0.77，并已声明在 `requirements.txt`）。
2. 真实推理已验证（见下）。
3. 输出 IMAGE 为 4 通道；若下游节点不支持 RGBA 请改用 `mask`。

## 实测修正（L3）
真实推理暴露并修复 1 处缺陷：
- `first` 已是 ndarray 却调用 `.clamp().numpy()` → `AttributeError`；改为在 tensor 上 clamp 再转 numpy。
修复后真实输出：MASK `(1,768,768)`（覆盖 0.289）+ RGBA `(1,768,768,4)`，模型 `u2net`。
