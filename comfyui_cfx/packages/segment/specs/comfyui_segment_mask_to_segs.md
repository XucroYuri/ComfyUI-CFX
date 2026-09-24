---
id: comfyui_segment_mask_to_segs
display_name: "ComfyUI-Segment · Mask to SEGS"
category: "ComfyUI-Segment/Compat"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "Impact Pack SEGS producer (impact-pack, GPL-3.0 — 仅参考公开数据格式，未复制代码)"
---

## 1. 目的
把 MASK 的每个非空 batch 项包装为 Impact Pack 的 `SEGS` 结构，作为**兼容垫层**
让本包节点与其下游互通。不导入 GPL 插件、不复制其代码，仅实现公开数据格式。

## 2. 语义
- `SEGS` 为列表，元素形如 `((H, W), {...})`，`(H, W)` 为**整图**尺寸。
- 逐 MASK batch 项用 `geometry.mask_to_bboxes(mask_np, threshold=0.5)` 取包围盒；
  完全为空的项跳过。`bbox`/`crop_region` 均为该盒 `(x0, y0, x1, y1)`。
- `cropped_image` = 归一化 IMAGE 在 `[y0:y1, x0:x1, :]` 的裁剪（`[h,w,C]`，通道数随输入）；
  `cropped_mask` = MASK 同区域裁剪（`[h,w]`）。二者均为 float32 连续张量。
- `confidence` 来自输入；`label` 来自输入；`control_net_wrapper` 恒为 `None`。
- 单图（batch=1）IMAGE 对多个 MASK 项广播；IMAGE 与 MASK 批次相等时按下标配对。
- MASK 全空 → 返回 `[]`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | mask | MASK | 是 | - |
| in | label | STRING | 否 | "segment" |
| in | confidence | FLOAT | 否 | 1.0（0.0–1.0, step 0.01） |
| out | segs | SEGS | - | - |

## 4. 执行与缓存
确定性纯几何，无模型、无缓存。

## 5. 资源
numpy 切片 + `geometry.mask_to_bboxes`，无额外依赖。

## 6. 副作用与安全
无。

## 7. 错误行为
非 `[H,W]`/`[B,H,W]` MASK → `ValueError`；非张量 MASK → `TypeError`；
非 IMAGE 张量 → `TypeError`；IMAGE 批次既非 1 也非 MASK 批次数 → `IndexError`（fail loudly）。

## 8. 对抗性反例
1. 全空 MASK → `[]`；
2. 单图 + 多 MASK 项 → 图像广播，每项一条；
3. 贴边 mask → bbox 夹取到图像范围，裁剪不越界；
4. `threshold=0.5` 严格大于：恰好 0.5 的像素不产生条目；
5. 多 MASK 项按 batch 顺序产生多条 SEGS。

## 9. 验收
`tests/test_segment_segs.py`。
