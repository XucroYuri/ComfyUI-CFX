---
id: comfyui_depth3d_colormap
display_name: "ComfyUI-Depth3D · Colormap"
category: "ComfyUI-Depth3D/Process"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
将单目深度估计输出的深度图着色为可视化 `IMAGE`：既支持直接复制为灰度三通道，
也支持通过 `matplotlib` 色标（turbo/viridis/…）映射为彩色 RGB，供预览、合板或导出复用。

## 2. 语义
- 输入 `IMAGE` 经 `core.types.ensure_image` 归一为 `[B,H,W,C]` float32。
- 深度通道 `d = img.mean(dim=-1)`，形状 `[B,H,W]`。
- `normalize is True`：对每个 batch 项独立用该项的 `min`/`max` 线性缩放到 `[0,1]`。
  当 `max == min` 时该项输出**全零**，绝不产生 `NaN`/`Inf`。
- `normalize is False`：不做缩放，仅将 `d` 截断到 `[0,1]`（越界值夹紧，不产生 `NaN`）。
- `colormap == "gray"`：输出为 `d` 复制 3 通道，形状 `[B,H,W,3]`。
- 其余色标名：经 `matplotlib.colormaps[name]` 映射到 RGB，值域 `[0,1]`。
- 输出 `image`：`[B,H,W,3]`，float32，连续内存，值域 `[0,1]`。
- 各 batch 项相互独立，互不影响。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | image | IMAGE | 是 | - | BHWC float32 深度图；逐项求均值得到单通道深度 |
| in | colormap | COMBO | 是 | turbo | `gray` 直出灰度；其余用 matplotlib 色标映射 |
| in | normalize | BOOLEAN | 是 | True | True 逐项缩放到 [0,1]；False 仅截断到 [0,1] |
| out | image | IMAGE | - | - | 着色结果 [B,H,W,3]，float32，[0,1] |

## 4. 执行与缓存
- 确定性：同输入逐元素可复现；色标查表确定，无随机性、无全局状态。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。
- 纯张量 + 色标查表，无模型加载。

## 5. 资源
- 纯 CPU 上的逐元素张量运算与色标查表；峰值内存 ≈ 输入 + 单通道中间量 + 输出。
- 输出张量为 float32 且连续。
- 依赖：`torch`、`matplotlib`（仅在非 `gray` 分支惰性导入色标表）。

## 6. 副作用与安全
- 无文件、无网络、无全局状态修改。
- 惰性 `matplotlib` 导入不初始化后端/不弹窗（只取色标表）。
- 不写入 shared/temp 目录，不访问任何外部路径。

## 7. 错误行为
- `colormap` 非枚举值：`matplotlib` 色标表查不到时抛出清晰异常（`KeyError`），不静默降级。
- `normalize=False`：越界输入夹紧到 `[0,1]`，绝不产生 `NaN`。
- 常量输入：`normalize=True` 返回有限常量向量，绝不产生 `NaN`。
- 非张量 / 非法 shape：由 `core.types.ensure_image` 抛出清晰异常，不静默降级。

## 8. 对抗性反例
1. 常量深度图（`max == min`）且 `normalize=True` → 输出为有限常量，无 `NaN`；
2. 越界输入（大负 / 大于 1）且 `normalize=False` → 输出夹紧在 `[0,1]`，无 `NaN`；
3. `gray` 与 `turbo` 同输入 → 两者取色机制不同，结果不相等；
4. batch=2 且两项量纲悬殊 → 各自归一到 `[0,1]`，互不干扰；
5. `gray` 输出 == 归一化后的深度逐通道复制 3 次。

## 9. 验收
- `tests/test_depth3d_colormap.py`：形状/连续、值域、`gray` 等于归一化深度复制、不同色标结果不同、常量输入有限常量、`normalize=False` 越界夹紧；
- CPU 上 fp32 断言；
- `tools/spec_lint.py` 与 `tools/license_gate.py` 通过。
