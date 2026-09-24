---
id: comfyui_sampling_sigma_shift
display_name: "ComfyUI-Sampling · Sigma Shift"
category: "ComfyUI-Sampling/Sigmas"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "SigmaShift (RES4LYF, behaviour reference)"
---

## 1. 目的
把一条 sigma 序列整体乘以一个常数因子，用于在不改变调度形状的前提下统一缩放噪声强度
（例如细节增强阶段的整体冷热偏移）。

## 2. 语义
输入 `sigmas` 为 ComfyUI 的 `SIGMAS` 类型，即一维 `torch.Tensor`。
返回单个新张量 `sigmas * factor`，结果 `.contiguous()`，保持输入 dtype 与 device，
不修改输入张量（乘法律产生新张量，`.contiguous()` 在必要时再拷贝）。
`factor=1.0` 时数值与原序列相同（但仍是新张量）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | sigmas | SIGMAS | 是 | - |
| in | factor | FLOAT | 是 | 1.0（min 0.001，max 10.0，step 0.001） |
| out | sigmas | SIGMAS | - | - |

## 4. 执行与缓存
纯函数、确定性；仅依赖输入张量与 `factor`，无随机、无全局状态。

## 5. 资源
时间 O(len(sigmas))，一次逐元素乘法并可能一次连续化拷贝；内存与输入同量级。sigma 序列通常极短。

## 6. 副作用与安全
无文件、网络或全局状态副作用。不就地修改输入张量。

## 7. 错误行为
- `sigmas` 非一维（`dim() != 1`）→ `ValueError`。
- `factor` 由 FLOAT 控件约束为 `[0.001, 10.0]`，不出现零或负值。

## 8. 对抗性反例
1. `factor=1.0` → 数值与输入逐元素相等，且不共享存储（输入未被修改）；
2. `factor=2.0` → 每个元素翻倍；
3. 非一维输入（如 `[2,3]`）→ `ValueError`；
4. `float64` 输入、`factor=2.0` → 输出 dtype 仍为 `float64`，device 不变；
5. 输入为切片等非连续张量 → 输出仍为连续张量；
6. 调用后输入张量内容与调用前一致（无就地修改）。

## 9. 验收
`tests/test_sampling_shift.py`。
