---
id: comfyui_primitives_json_bbox
display_name: "ComfyUI-Primitives · JSON BBox"
category: "ComfyUI-Primitives/JSON"
version: 1.0.0
license: MIT
since: 2026-09-25
replaces:
  - "(no upstream equivalent)"
---

## 1. 目的
把检测结果字典（Florence-2 / GroundingDINO 的 `bboxes` / `polygons`）中的单个条目
拆成四个 `INT` 坐标，供 `comfyui_vision_florence2_region` 等下游节点当作区域框使用。

## 2. 语义
- 输入 `annotations` 为字典，需包含 `bboxes`（`[x0, y0, x1, y1]` 列表）或
  `polygons`（点列表的列表）之一；两者都存在时优先 `bboxes`。
- 取第 `index` 个条目；`polygons` 条目以其所有点的最小/最大角作为外接框。
- 归一化保证 `x1 >= x0`、`y1 >= y0`（坐标倒序时交换）。
- 坐标四舍五入为 `INT`；`bbox` 输出为 `{"bbox": [x0, y0, x1, y1], "index": index}`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | annotations | JSON | 是 | - |
| in | index | INT | 是 | 0 |
| out | x0 / y0 / x1 / y1 | INT | - | - |
| out | bbox | JSON | - | - |

## 4. 执行与缓存
确定性；无随机；不定义 `IS_CHANGED`。

## 5. 资源
纯 Python；仅读取传入的字典，不做拷贝。

## 6. 副作用与安全
无文件/网络；不修改输入 `annotations`。

## 7. 错误行为
- 既无 `bboxes` 也无 `polygons` → `ValueError`（消息含可用条目数 0）；
- `index` 越界（含负值）→ `ValueError`（消息含可用条目数）；
- `annotations` 非字典 → `ValueError`。

## 8. 对抗性反例
1. `{"bboxes": []}` → `ValueError`（0 条可用）；
2. `index=5` 但仅 1 条 → `ValueError`；
3. 两个键都缺失 → `ValueError`；
4. `bboxes=[[80, 60, 20, 10]]`（`x1 < x0`）→ 归一化为 `[20, 10, 80, 60]`；
5. 多边形点顺序任意 → 外接框不变；
6. 浮点坐标 `[1.4, 2.6, 9.5, 4.4]` → 就近取整。

## 9. 验收
`tests/test_primitives_json_bbox.py`。
