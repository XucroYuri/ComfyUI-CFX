---
id: comfyui_inpaint_stitch
display_name: "ComfyUI-Inpaint · Stitch"
category: "ComfyUI-Inpaint/Crop"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
把处理后的局部图（`cropped`）按 `crop_data` 贴回原始整图，是 `comfyui_inpaint_crop_by_mask` 的精确逆操作。

## 2. 语义
- `image` 为原始整图；`cropped` 为处理后的裁剪块；`crop_data` 来自 crop 节点。
- 校验 `crop_data` 含 `x/y/width/height/original_width/original_height`；`original_width/height` 必须与 `image` 的空间维一致。
- `cropped` 的空间维必须等于 `(height, width)`，否则报错，**不自动缩放**。
- 目标矩形按整图 clamp；clamp 后仍非空才贴回，否则原样返回整图副本。
- 无 `mask`：直接赋值 `base[..., y0:y1, x0:x1, :] = patch`。
- 有 `mask`：`base*(1-m) + patch*m`；`m` 取首个 batch 项、clamp 到 `[0,1]`，可为 patch 尺寸或整图尺寸（整图尺寸时按目标矩形切片）。
- 返回与输入 `image` 同形的 `[B,H,W,C]`；内部克隆，绝不修改输入张量。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | cropped | IMAGE | 是 | - |
| in | crop_data | JSON | 是 | - |
| in | mask | MASK | 否 | - |
| out | image | IMAGE | - | - |

## 4. 执行与缓存
确定性；无随机。

## 5. 资源
纯张量切片/克隆；无模型、无外部文件。

## 6. 副作用与安全
不修改输入 `image`（`ensure_image` 后 `clone`）；无其他副作用。

## 7. 错误行为
- `crop_data` 缺任一键 → `ValueError("stitch: crop_data is missing '<key>'")`。
- `original_width/height` 与整图不符 → `ValueError`。
- `cropped` 尺寸与 `(height, width)` 不符 → `ValueError`。
- `mask` 非 2D/3D 或与 patch/整图尺寸都不符 → `ValueError`。
- 非法图像 shape → `ValueError`（来自 `ensure_image`）。

## 8. 对抗性反例
1. crop 后原样 stitch → 除贴回区域外与整图逐像素相等；
2. 目标矩形越出整图 → clamp 后仍贴回，不越界写入；
3. clamp 后矩形为空 → 原样返回整图副本；
4. patch 尺寸不符 → 报错，不缩放；
5. `crop_data` 缺键 → 报错；
6. `original_width/height` 不匹配 → 报错；
7. mask 提供时 → 输出为加权混合且被 clamp 到 `[0,1]`。

## 9. 验收
`tests/test_inpaint_stitch.py`。
