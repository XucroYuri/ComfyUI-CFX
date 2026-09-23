# Adversarial Review: comfyui_segment_sam2_loader

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- **单一实现**：复用 Apache-2.0 上游，不再 vendor 第二/第三份 SAM2。
- §8.1 CPU 强制 fp32，避免上游直接报错，行为有告警、有测试。
- §7 后端缺失报 `FileNotFoundError` 且含期望目录。
- 未复制 GPL 插件代码。

## 未决疑点
1. 依赖上游 `DownloadAndLoadSAM2Model` 的类/方法签名；上游改名会破坏。已提供 `CFX_SAM2_DIR` 覆盖。
2. 真实推理未在 CI 覆盖（需权重），人工 VERIFY。
