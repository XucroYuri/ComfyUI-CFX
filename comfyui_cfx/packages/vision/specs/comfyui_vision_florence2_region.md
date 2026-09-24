---
id: comfyui_vision_florence2_region
display_name: "ComfyUI-Vision · Florence-2 Region"
category: "ComfyUI-Vision/Florence2"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "Florence2 Region (comfyui-florence2)"
---

## 1. 目的
对图像上的指定像素框做区域精修：描述 / 分类 / OCR。

## 2. 语义
- `x0`/`y0`/`x1`/`y1` 为像素坐标；四者全为 0 表示整图。
- 非全零时要求 `x1 > x0` 且 `y1 > y0`，否则 `ValueError`；随后把框夹取到图像内。
- `task` 经 `TASKS` 映射为任务 token；坐标经 `quantize` 映射到 Florence-2 的 1000 格位置编码，
  拼成 `prompt = token + loc_string(...)`。
- 调用共享 `run_florence2(florence2, image, prompt, token, ...)`；`parse_task` 即该 token。
- `STRING` 输出为纯文本结果；`JSON` 为解析结果（与 Florence-2 Run 一致，均为后端透传）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | florence2 | CFX_FLORENCE2 | 是 | - |
| in | image | IMAGE | 是 | - |
| in | x0 | INT | 是 | 0 |
| in | y0 | INT | 是 | 0 |
| in | x1 | INT | 是 | 0 |
| in | y1 | INT | 是 | 0 |
| in | task | COMBO | 是 | region_to_description |
| in | max_new_tokens | INT | 否 | 256 |
| in | num_beams | INT | 否 | 3 |
| in | do_sample | BOOLEAN | 否 | False |
| out | text | STRING | - | - |
| out | parsed | JSON | - | - |

## 4. 执行与缓存
`quantize`/`loc_string` 为模块级纯函数，与推理解耦，可在无模型时单测。推理复用共享后端，
不重复加载模型。

## 5. 资源
单张推理；不释放句柄（句柄可被多个节点复用，回收交给 ComfyUI 模型管理）。

## 6. 副作用与安全
无文件/网络。

## 7. 错误行为
未知 `task` → `ValueError`（在推理之前）；非全零且 `x1 <= x0` 或 `y1 <= y0` → `ValueError`。

## 8. 对抗性反例
1. 全零框 → 整图（等价于 `loc_string(0, 0, W, H)`）；
2. 反向框（`x1 <= x0` 或 `y1 <= y0`）→ `ValueError`，且不触发推理；
3. `quantize` 上界饱和：`value >= size` → `bins-1`；`size <= 0` → 0；
4. 越界框先夹取到图像边界，再量化（避免产生超出 `bins` 的位置 token）。

## 9. 验收
`tests/test_vision_florence2_region.py`（quantize 边界/中值、loc_string 格式、TASKS 与 COMBO 一致、
反向框报错、全零框整图、prompt 构造与夹取）；真实推理为 L3 人工 VERIFY（由集成方执行）。
