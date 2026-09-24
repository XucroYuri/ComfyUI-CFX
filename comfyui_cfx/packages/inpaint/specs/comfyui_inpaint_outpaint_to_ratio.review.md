# Adversarial Review: comfyui_inpaint_outpaint_to_ratio

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §8.1 正方形 + `"16:9"`：`width*target_h (32*9=288) < height*target_w (32*16=512)` 成立，保留 `new_h=height`，`new_w=round(32*16/9)=57 > 32`，只扩宽；有测试。
- §8.2 正方形 + `"9:16"`：`288 > 512` 不成立，走 else 保留 `new_w=width`，`new_h=round(32*16/9)=57 > 32`，只扩高；有测试。
- §8.3 比例命中：整数叉乘 `width*target_h == height*target_w` 提前返回归一化输入（`1:1`/`16:9`），不重建画布，`torch.equal` 验证。
- §8.4 `anchor="start"`：偏移 `(0,0)`，原图贴左上，右侧新增区为 `fill` 且掩码为 `1.0`；有测试。
- §8.5 `anchor="end"`：偏移 `(new_w-width, new_h-height)`，原图贴右下，左侧新增区为 `fill` 且掩码为 `1.0`；有测试。
- §8.6 `anchor="center"`：两维 `//2` 居中，边框掩码逐边 `==1.0`，中心区域与输入掩码 `allclose`；有测试。
- §8.7 `fill` 边界：`torch.full` 用 `float(fill)` 精确填充，边框像素等于 `0.25`/默认 `0.0`。
- §8.8 `mask` 为 `[H,W]`：`dim()==2` 保持，clamp 后 `unsqueeze(0)` 成 `[1,H,W]`，写入原图区域。
- §8.9 尺寸不符：比例未命中且空间维与 `image` 不一致时报 `ValueError`，不依赖广播静默处理。
- 维度单调性：两个分支的新维均不小于原维（`round` 输入严格大于原维），偏移非负，切片不越界/不翻转。
- 副作用：新分配 `canvas`/`out_mask`，不修改输入张量；输出 dtype/device/channels 与 `image` 一致。
- 输出契约：`RETURN_TYPES=("IMAGE","MASK")`，`RETURN_NAMES=("image","mask")`，`FUNCTION="run"`，id/显示名/分类符合契约。

## 未决疑点
1. 掩码只取首个 batch 项，与 `crop_by_mask`/`stitch`/`outpaint_canvas` 的约定一致；多 batch 掩码其余项被忽略。
2. 比例命中时原样返回，即使 `mask` 空间维与 `image` 不符也不校验，保持“unchanged”语义。
3. 整数舍入可能使极小差值时新维等于原维（退化为原图大小），但不小于原维、不报错。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| 正方形 + 16:9 | 只扩宽 | PASS |
| 正方形 + 9:16 | 只扩高 | PASS |
| 输出与掩码同形 | shape 一致 | PASS |
| 中心边框掩码 1 / 中心等于输入 | 精确成立 | PASS |
| anchor=start | 左上贴放 | PASS |
| anchor=end | 右下贴放 | PASS |
| 比例命中 | 原样返回 | PASS |
| 未知 ratio/anchor | ValueError | PASS |
| mask 尺寸不符 | ValueError | PASS |
