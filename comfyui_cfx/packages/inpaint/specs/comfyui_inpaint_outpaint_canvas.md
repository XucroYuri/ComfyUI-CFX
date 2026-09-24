---
id: comfyui_inpaint_outpaint_canvas
display_name: "ComfyUI-Inpaint · Outpaint Canvas"
category: "ComfyUI-Inpaint/Crop"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
把图像放到更大的画布上（四边外扩），新增边框用常量 `fill` 填充，并在掩码上把边框标为 `1.0`（待重绘的 outpaint 区域），供后续 outpaint 采样使用。

## 2. 语义
- `image` 经 `ensure_image` 归一为 `[B,H,W,C]` float32。
- `mask` 归一为 `[1,H,W]` float 并 clamp 到 `[0,1]`；接受 `[H,W]` 或 `[B,H,W]`，取首个 batch 项；空间维必须与 `image` 一致，否则报错。
- 新画布尺寸为 `(H+top+bottom, W+left+right)`，用 `fill` 填充，dtype/device/channels 与 `image` 一致。
- 把 `image` 贴在画布 `(left, top)` 处（batch 维保留）。
- 输出掩码与新画布同尺寸：边框（新增区域）为 `1.0`，原图区域写入输入掩码（贴在 `(left, top)`）。
- 四个边距全为 0 时，直接返回归一化后的 `image` 与 `mask`，不拷贝。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | mask | MASK | 是 | - |
| in | left | INT | 是 | 0 |
| in | right | INT | 是 | 0 |
| in | top | INT | 是 | 0 |
| in | bottom | INT | 是 | 0 |
| in | fill | FLOAT | 是 | 0.0 |
| out | image | IMAGE | - | - |
| out | mask | MASK | - | - |

约束：`left/right/top/bottom` 范围 `[0,4096]`；`fill` 范围 `[0.0,1.0]`，步长 `0.01`。

## 4. 执行与缓存
确定性；无随机、无状态；相同输入总是得到相同输出。

## 5. 资源
纯张量分配/切片；无模型、无外部文件。内存约为 `(H+top+bottom)*(W+left+right)*C`。

## 6. 副作用与安全
不修改输入张量；输出为新建画布。无其他副作用。

## 7. 错误行为
- `mask` 非 2D/3D → `ValueError("outpaint: mask must be 2D or 3D, ...")`。
- `mask` 空间维与 `image` 不符（且边距非全 0）→ `ValueError("outpaint: mask ... does not match image ...")`。
- 非法图像 shape → `ValueError`（来自 `ensure_image`）。

## 8. 对抗性反例
1. 四边全 0 → 原样返回归一化输入，画布不重建；
2. 只扩一边 → 仅该边为 `fill`/掩码 `1.0`；
3. 多个 batch 图像 → batch 维保留，掩码仍取首项；
4. `mask` 为 `[H,W]` → 归一为 `[1,H,W]` 并正确写入原图区域；
5. `mask` 空间维不符 → 报错，不静默广播；
6. `fill` 取边界值 `0.0`/`1.0` → 边框像素精确等于该值。

## 9. 验收
`tests/test_inpaint_outpaint.py`。
