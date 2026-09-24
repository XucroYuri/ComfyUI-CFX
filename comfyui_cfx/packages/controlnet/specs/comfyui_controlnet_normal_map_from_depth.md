---
id: comfyui_controlnet_normal_map_from_depth
display_name: "ComfyUI-ControlNet · Normal from Depth"
category: "ComfyUI-ControlNet/Preprocessors"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "NormalMapPreprocessor (controlnet_aux)"
  - "NormalMap (comfyui_controlnet_aux)"
---

## 1. 目的
从单通道（或可塌缩为单通道的）深度图估计切线空间法线图，供 ControlNet 条件图使用。
本节点为确定性、无模型、无网络的有限差分实现：对深度图求水平/垂直梯度，
构造单位法线并编码为 `[0,1]` 的 RGB 图像，避免下游重复计算。

## 2. 语义
- 输入 `IMAGE` 经 `core.types.ensure_image` 归一为 `[B,H,W,C]` float32。
- 深度通道 `depth = img.mean(dim=-1)`，形状 `[B,H,W]`。
- 若 `invert` 为真，`depth = 1 - depth`（远近语义翻转）。
- 梯度用**边缘安全**的中心差分：内部 `(d[i+1]-d[i-1])/2`，边界用单侧一阶差分
  `d[1]-d[0]` 与 `d[-1]-d[-2]`；沿高度轴得 `dy`（dim=1），沿宽度轴得 `dx`（dim=2）。
- 在末尾新增通道维：`n = normalize([-dx*strength, -dy*strength, 1])`。
  其中 `z=1`，故模长恒 `>= 1`，除零不可能。
- 编码 `(n + 1) / 2` 到 `[0,1]`。
- 输出 `image`：形状 `[B,H,W,3]`，float32，连续内存，值域 `[0,1]`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | image | IMAGE | 是 | - | BHWC float32 深度图；按通道均值取深度 |
| in | strength | FLOAT | 是 | 1.0 | 梯度缩放，[0,10]，步长 0.01 |
| in | invert | BOOLEAN | 是 | False | 为真时深度取 `1-x` |
| out | image | IMAGE | - | - | 法线图 [B,H,W,3]，float32，[0,1] |

## 4. 执行与缓存
- 确定性：同输入逐元素可复现；无随机性、无全局状态。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。
- 纯张量运算，无模型加载，可重复执行且结果一致。

## 5. 资源
- 纯 CPU/GPU 逐元素张量运算；峰值内存 ≈ 深度图 + 两个梯度 + 法线/编码。
- 输出张量 float32，`image` 连续内存（`contiguous`）。
- 无外部依赖，仅 `torch`。

## 6. 副作用与安全
- 无文件、无网络、无全局状态修改。
- 不写入 shared/temp 目录，不访问任何外部路径。

## 7. 错误行为
- 非张量 / 非法 shape → 由 `core.types.ensure_image` 抛出清晰异常，不静默降级。
- 常量深度图 → 梯度为零，法线 `[0,0,1]`（编码 `[0.5,0.5,1.0]`），有限无 `NaN`。
- 单像素边（`H<2` 或 `W<2`）→ 对应轴梯度为零（不越界、不报错）。

## 8. 对抗性反例
1. 平坦深度图 → 法线 `z` 主导，编码约为 `[0.5,0.5,1.0]`；
2. 任意深度图 → 解码法线 `2*out-1` 为单位长度；
3. `invert=True` → x/y 编码与 `invert=False` 互补（`1-x`），z 不变；
4. 常量图（无梯度）→ 输出有限，无 `NaN`/`Inf`；
5. batch=2 → 逐项独立计算，输出 batch 维与输入一致；
6. 编码保证值域严格落在 `[0,1]`。

## 9. 验收
- `tests/test_controlnet_normal.py`：形状 `[B,H,W,3]`、值域、平坦图 z 主导、单位长度、`invert` 翻转、batch=2；
- CPU 上 fp32 断言；
- `tools/spec_lint.py` 与 `tools/license_gate.py` 通过。
