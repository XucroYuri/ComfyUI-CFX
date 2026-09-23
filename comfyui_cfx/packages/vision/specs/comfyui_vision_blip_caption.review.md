# Adversarial Review: comfyui_vision_blip_caption

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- 延迟导入 `transformers`：模块导入不触发重依赖，便于测试与失败定位。
- §8.2 `vqa` 仓库走问答网络。
- batch 取首张，与 Florence-2 节点一致。

## 未决疑点
1. 模型缓存为模块级（持久）；绑定仓库名，最小化。
2. 真实推理未在 CI 覆盖（需权重），标记人工 VERIFY。
3. BLIP2/其他 VLM 未纳入；Qwen-VL 计划在 M3（GPL 隔离）。
