# Adversarial Review: comfyui_vision_clip_interrogator

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- 延迟导入 `clip_interrogator`：模块导入不触发重依赖，测试与失败定位成本低。
- §8.1 `negative` 模式不接受 `max_flavors`，实现按模式分派，符合后端真实签名。
- §8.2 未知 `mode` 在 `_load` 之前抛出 `ValueError`，不会触发模型下载。
- `MODE_METHODS` 与 `mode` COMBO 同源（`list(MODE_METHODS)`），保证二者不漂移。
- batch 取首张，与 Florence-2/WD14/BLIP/VLM 节点一致（`core.images.first_image_to_pil`）。

## 未决疑点
1. `Interrogator` 为模块级缓存（持久）；绑定 `clip_model`，最小且职责清晰。
2. 真实推理未在 CI 覆盖（需权重），标记 L3 人工 VERIFY，由集成方执行。
3. `max_flavors` 上限 16，避免用户设置过大导致逐词遍历变慢。
