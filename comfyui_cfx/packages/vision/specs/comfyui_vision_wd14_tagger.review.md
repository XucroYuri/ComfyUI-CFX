# Adversarial Review: comfyui_vision_wd14_tagger

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §8.1 白边补齐不拉伸，单测覆盖（非正方形输入）。
- §8.2/§8.3 阈值与排序逻辑单测覆盖。
- §8.4 过滤逻辑单测覆盖。
- 预处理与阈值选择与 ONNX 会话解耦，可离线测试。

## 未决疑点
1. 预处理采用 SmilingWolf 标准（白边 + BGR）；**已经真实模型验证**。
2. 会话为模块级缓存（持久）；绑定模型文件路径，最小且职责清晰，符合核心规范例外。
3. `exclude_tags` 为子串匹配（大小写不敏感）。

## 实测修正（L3）
真实推理暴露并修复 3 处缺陷：
1. `run()` 先读 `selected_tags.csv` 再触发下载 → 干净安装时 `FileNotFoundError`；改为先 `download_model()`。
2. `first` 已是 ndarray 却调用 `.clamp().numpy()` → `AttributeError`；改为在 tensor 上 clamp 再转 numpy。
3. 输入尺寸取 `shape[-1]` 得到通道维 3（模型为 NHWC `[1,448,448,3]`）→ 3×3 输入报错；改为取 `shape[1:3]` 中的空间维。
修复后真实输出：`solo, smile, 1girl, outstretched arms, dress, ...`。
