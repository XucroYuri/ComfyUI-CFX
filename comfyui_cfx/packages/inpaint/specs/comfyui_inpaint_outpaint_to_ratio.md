---
id: comfyui_inpaint_outpaint_to_ratio
display_name: "ComfyUI-Inpaint · Outpaint to Ratio"
category: "ComfyUI-Inpaint/Crop"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
把图像外扩到目标宽高比：保留已满足比例的那一维（不裁剪），只向另一维扩展，新增边框用 `fill` 填充并在掩码上标为 `1.0`，供后续 outpaint 采样使用。

## 2. 语义
- `image` 经 `ensure_image` 归一为 `[B,H,W,C]` float32。
- `mask` 归一为 `[1,H,W]` float 并 clamp 到 `[0,1]`；接受 `[H,W]` 或 `[B,H,W]`，取首个 batch 项。
- `ratio` 解析为整数对 `(target_w, target_h)`（`"16:9"` → `(16,9)`）。
- 比例判定用整数叉乘：`width*target_h == height*target_w` 即已匹配，直接返回归一化后的 `image`/`mask`，不重建画布。
- 若 `width*target_h < height*target_w`（当前偏瘦），保留 `height`，令 `new_w = round(height * target_w / target_h)`。
- 否则（当前偏宽），保留 `width`，令 `new_h = round(width * target_h / target_w)`。四舍五入后新维不小于原维，不产生负偏移。
- `anchor` 决定原图贴放偏移：`"start"` → `(0,0)`（左上）；`"end"` → `(new_w-width, new_h-height)`（右下）；`"center"` → 两维均 `//2` 居中。
- 新画布尺寸 `(new_h, new_w)`，dtype/device/channels 与 `image` 一致；`image` 整体贴到 `(offset_x, offset_y)`，batch 维保留。
- 输出掩码与画布同尺寸：边框（新增区域）为 `1.0`，原图区域写入输入掩码。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | mask | MASK | 是 | - |
| in | ratio | COMBO | 是 | `"16:9"` |
| in | anchor | COMBO | 是 | `"center"` |
| in | fill | FLOAT | 是 | 0.0 |
| out | image | IMAGE | - | - |
| out | mask | MASK | - | - |

约束：`ratio ∈ ["1:1","4:3","3:2","16:9","9:16","2:3","3:4"]`；`anchor ∈ ["center","start","end"]`；`fill ∈ [0.0,1.0]`，步长 `0.01`。

## 4. 执行与缓存
确定性；无随机、无状态；相同输入总是得到相同输出。

## 5. 资源
纯张量分配/切片；无模型、无外部文件。内存约为 `new_h*new_w*C`。

## 6. 副作用与安全
不修改输入张量；输出为新建画布。无其他副作用。

## 7. 错误行为
- `mask` 非 2D/3D → `ValueError("outpaint_to_ratio: mask must be 2D or 3D, ...")`。
- `ratio` 不在白名单 → `ValueError("outpaint_to_ratio: unknown ratio ...")`。
- `anchor` 不在白名单 → `ValueError("outpaint_to_ratio: unknown anchor ...")`。
- `mask` 空间维与 `image` 不符（且比例未命中）→ `ValueError("outpaint_to_ratio: mask ... does not match image ...")`。
- 非法图像 shape → `ValueError`（来自 `ensure_image`）。

## 8. 对抗性反例
1. 正方形 + `"16:9"` → 保留高度，宽度变大；输出仍为单一 batch。
2. 正方形 + `"9:16"` → 保留宽度，高度变大。
3. 比例已命中（正方形 + `"1:1"`、16:9 图 + `"16:9"`）→ 原样返回，不重建画布。
4. `anchor="start"` → 原图贴左上，新增区域为 `fill`/掩码 `1.0`。
5. `anchor="end"` → 原图贴右下，新增区域为 `fill`/掩码 `1.0`。
6. `anchor="center"` → 边框掩码全为 `1.0`，中心区域等于输入掩码。
7. `fill` 取边界值 `0.0`/`1.0` → 边框像素精确等于该值。
8. `mask` 为 `[H,W]` → 归一为 `[1,H,W]` 并正确写入原图区域。
9. `mask` 空间维不符（且比例未命中）→ 报错，不静默广播。

## 9. 验收
`tests/test_inpaint_ratio.py`。
