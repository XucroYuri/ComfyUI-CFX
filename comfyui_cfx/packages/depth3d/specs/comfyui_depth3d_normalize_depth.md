---
id: comfyui_depth3d_normalize_depth
display_name: "ComfyUI-Depth3D · Normalize Depth"
category: "ComfyUI-Depth3D/Process"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
将单目深度估计输出的深度图归一化到 `[0,1]`，并同时输出三通道 `IMAGE` 与单通道 `MASK`，
供下游 ControlNet 条件图、遮罩合成或可视化复用，避免下游重复归一化。

## 2. 语义
- 输入 `IMAGE` 经 `core.types.ensure_image` 归一为 `[B,H,W,C]` float32。
- 深度通道 `d = img.mean(dim=-1)`，保留维不置位，形状 `[B,H,W]`。
- `mode == "minmax"`：对每个 batch 项独立用该项的 `min`/`max` 线性缩放到 `[0,1]`。
  当 `max == min` 时该项输出**全零**，绝不产生 `NaN`/`Inf`。
- `mode == "clamp"`：不做缩放，仅将 `d` 截断到 `[0,1]`。
- 归一化/截断之后，若 `invert` 为真，执行 `1 - d`。
- 输出 `image`：`d` 复制 3 通道，形状 `[B,H,W,3]`，float32，值域 `[0,1]`。
- 输出 `mask`：`d` 本身，形状 `[B,H,W]`，float32，值域 `[0,1]`。
- 各 batch 项相互独立，互不影响。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | image | IMAGE | 是 | - | BHWC float32 深度图；逐项求均值得到单通道深度 |
| in | mode | COMBO | 是 | minmax | `minmax` 逐项缩放到 [0,1]；`clamp` 仅截断 |
| in | invert | BOOLEAN | 是 | False | 归一化后取 `1-x` |
| out | image | IMAGE | - | - | 深度图 [B,H,W,3]，float32，[0,1] |
| out | mask | MASK | - | - | 深度掩码 [B,H,W]，float32，[0,1] |

## 4. 执行与缓存
- 确定性：同输入逐元素可复现；无随机性、无全局状态。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。
- 纯张量运算，无模型加载，可重复执行且结果一致。

## 5. 资源
- 纯 CPU/GPU 上的逐元素张量运算；峰值内存 ≈ 输入 + 单通道中间量 + 两个输出。
- 输出张量为 float32；`image` 为连续内存（`contiguous`）。
- 无外部依赖，仅 `torch`。

## 6. 副作用与安全
- 无文件、无网络、无全局状态修改。
- 不写入 shared/temp 目录，不访问任何外部路径。

## 7. 错误行为
- `mode` 非 `minmax`/`clamp`：落入 `clamp` 分支（`else`），不做静默缩放。
- 非张量 / 非法 shape：由 `core.types.ensure_image` 抛出清晰异常，不静默降级。
- 常量输入：`minmax` 返回全零（有限值），绝不产生 `NaN`。

## 8. 对抗性反例
1. 常量深度图（`max == min`）→ `minmax` 输出全零且有限，无 `NaN`；
2. 含负值 / 大于 1 的输入在 `clamp` 下 → 输出严格夹在 `[0,1]`；
3. `invert=True` → 输出等于 `1 - invert=False` 的输出，值域仍为 `[0,1]`；
4. batch=2 且两项量纲差异悬殊 → 各自归一到 `[0,1]`，互不干扰（全局归一化会使低幅项塌缩）；
5. `minmax` 输出同时出现 `0.0` 与 `1.0`（非常量输入）。

## 9. 验收
- `tests/test_depth3d_normalize.py`：形状、`minmax` 端点、`invert` 翻转、常量输入全零有限、`clamp` 值域、batch 独立性；
- CPU 上 fp32 断言；
- `tools/spec_lint.py` 与 `tools/license_gate.py` 通过。
