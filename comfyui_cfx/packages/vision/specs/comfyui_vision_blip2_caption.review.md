# Adversarial Review: comfyui_vision_blip2_caption

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- 延迟导入 `transformers`：模块导入不触发重依赖，便于测试与失败定位。
- §8.2 未知 `precision` 在 `_load` 内先经 `resolve_dtype` 校验，早于下载与导入。
- 缓存键为 `(model, precision)`：同仓库不同精度不会串用权重/dtype。
- §8.3 batch 取首张，与其他图像节点一致（`core.images.first_image_to_pil`）。
- §8.4 只对浮点张量（`pixel_values`）转换 dtype，整数张量（`input_ids`/`attention_mask`）保持原样。

## 未决疑点
1. 模型缓存为模块级（持久）；键绑定 `(model, precision)`，最小化。
2. 真实推理未在 CI 覆盖（需权重），标记人工 VERIFY。
3. `Blip2Processor.__call__` 的第二位置参数为 `text`（question），与实现一致；已在 5.14.1 上核对签名。

## 实测修正（L3）
- 原设为 `Salesforce/blip2-opt-350m`，真实推理时该仓库 **404（不存在）**；已改为 Hub 上真实存在的 caption 版
  `blip2-opt-2.7b` / `blip2-flan-t5-xl` / `blip2-opt-6.7b`（默认 2.7b），并同步测试与 SPEC。
