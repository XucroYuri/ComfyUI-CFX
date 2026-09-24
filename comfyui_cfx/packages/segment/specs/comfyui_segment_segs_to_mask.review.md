# Adversarial Review: comfyui_segment_segs_to_mask

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 空 `SEGS` → `ValueError("segs_to_mask: empty SEGS")`，有测试。
- §8.2 两段并集按 `np.maximum` OR 合并，有测试与 `torch.maximum` 对照。
- §8.3 `width`/`height` 覆盖输出尺寸，有测试（`16×20`）。
- §8.4 超出覆盖后画布的区域按切片边界截断，不越界。
- 输出恒为 `[1,H,W]` float32；`H`/`W` 默认取首段整图尺寸，与 `mask_to_segs` 的第一元素一致，往返有测试。
- **许可**：不导入 impact-pack（GPL-3.0），不复制其代码；`SEGS` 仅为公开数据类型约定。

## 未决疑点
1. `crop_region` 与 `cropped_mask` 尺寸不一致时按两者较小边贴图（防御性截断），不在此处报错。
2. `width`/`height` 传负值不在合法范围内（widget `min=0`）；`0` 表示取首段尺寸。
