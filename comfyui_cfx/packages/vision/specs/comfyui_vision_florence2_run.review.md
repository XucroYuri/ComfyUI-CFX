# Adversarial Review: comfyui_vision_florence2_run

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §7 未知 task 经 `task_token` 抛 `ValueError`，有测试。
- §2 **不在 run 中释放模型**（修正）：句柄可被多个 Run 复用，释放交由 ComfyUI 模型管理。
  手动验证暴露了原「在 run 中 release」的隐患（导致 `ModelPatcher.__del__` 在退出期报错）。
- §8.4 多 batch 取首张，已在 SPEC 明示。
- `STRING`/`JSON` 双输出职责清晰（非多余透传）。

## 未决疑点
1. 仅处理 batch 首张，未做逐张循环；如需批量打标应外层用 `image_split` 列表语义。
2. 真实推理未在 CI 覆盖（需权重），标记为人工 VERIFY。
