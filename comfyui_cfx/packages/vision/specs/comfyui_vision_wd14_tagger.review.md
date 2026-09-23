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
1. 预处理采用 SmilingWolf 标准（白边 + BGR）；**未经真实模型验证**，标记人工 VERIFY。
2. 会话为模块级缓存（持久）；绑定模型文件路径，最小且职责清晰，符合核心规范例外。
3. `exclude_tags` 为子串匹配（大小写不敏感）。
