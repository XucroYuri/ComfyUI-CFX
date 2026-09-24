# Adversarial Review: comfyui_vision_florence2_region

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 全零框显式判定为整图，与用户手动传 `0,0,W,H` 结果一致，有测试。
- §8.2 反向框在调用 `run_florence2` 之前抛 `ValueError`，测试通过 monkeypatch 确认推理未被触发。
- §8.3 `quantize` 上界用 `min(bins-1, ...)` 饱和，`size <= 0` 返回 0，覆盖 0 / size / 中值三类边界。
- §8.4 先校验后夹取：越界坐标被夹到 `[0, width]`/`[0, height]`，因此 `loc_string` 不会产出
  越界 token（`quantize` 亦独立饱和，双重保险）。
- `TASKS` 与 `task` COMBO 同源（`list(TASKS)`），键集合与选项不会漂移，有测试。
- 复用 `florence2.run_florence2` 与 `FLORENCE2_TYPE`，不重复实现加载/解析，符合「单一缓存」使命。

## 未决疑点
1. `max_new_tokens` 上限 4096、`num_beams` 上限 64，与 Florence-2 Run 一致，避免用户误设过大变慢。
2. 真实推理未在 CI 覆盖（需权重），标记 L3 人工 VERIFY，由集成方执行。
3. 仅处理 batch 首张（经 `ensure_image` + 共享后端），与同包其他图像节点一致。
