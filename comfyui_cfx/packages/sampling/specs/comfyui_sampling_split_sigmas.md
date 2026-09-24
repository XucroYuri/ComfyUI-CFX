---
id: comfyui_sampling_split_sigmas
display_name: "ComfyUI-Sampling · Split Sigmas"
category: "ComfyUI-Sampling/Sigmas"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "SplitSigmas (RES4LYF, behaviour reference)"
---

## 1. 目的
把一条降序 sigma 序列在给定步长处切成 `sigmas_high`（前缀）与 `sigmas_low`（后缀），
用于两阶段采样/细节增强时的调度分段。

## 2. 语义
输入 `sigmas` 为 ComfyUI 的 `SIGMAS` 类型，即一维 `torch.Tensor`，按降序排列。
返回 `(sigmas[:step], sigmas[step:])`，两个结果均 `.contiguous()`，保持输入 dtype 与 device。
`step=0` 时第一路为空张量、第二路为完整输入；`step=len(sigmas)` 时相反。
不修改输入（切片产新张量，`.contiguous()` 在必要时拷贝）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | sigmas | SIGMAS | 是 | - |
| in | step | INT | 是 | 0（min 0，max 10000） |
| out | sigmas_high | SIGMAS | - | - |
| out | sigmas_low | SIGMAS | - | - |

## 4. 执行与缓存
纯函数、确定性；仅依赖输入张量与 `step`，无随机、无全局状态。

## 5. 资源
时间 O(len(sigmas)) 的视图切片，必要时一次连续化拷贝；内存与输入同量级。sigma 序列通常极短。

## 6. 副作用与安全
无文件、网络或全局状态副作用。不就地修改输入张量。

## 7. 错误行为
- `sigmas` 非一维（`dim() != 1`）→ `ValueError`。
- `step > len(sigmas)` → `ValueError`。
- `step` 由 INT 控件约束为 `[0, 10000]`，不出现负值。

## 8. 对抗性反例
1. 10 元素、`step=4` → high 4 个、low 6 个；拼接 `cat(high, low)` 等于原序列；
2. `step=0` → high 为空、low 等于原序列；
3. `step=len` → high 等于原序列、low 为空；
4. 非一维输入（如 `[2,3]`）→ `ValueError`；
5. `step=len+1` → `ValueError`；
6. `float64` 输入 → 两路 dtype 仍为 `float64`，device 不变。

## 9. 验收
`tests/test_sampling_sigmas.py`。
