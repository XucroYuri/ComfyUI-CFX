---
id: comfyui_flux_conditioning_concat
display_name: "ComfyUI-Flux · Conditioning Concat"
category: "ComfyUI-Flux/Conditioning"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces: []
---

## 1. 目的
拼接两份 CONDITIONING，得到合并后的条件列表（区域条件合并的最小原语）。

## 2. 语义
- CONDITIONING 是 `[ [tensor, dict], ... ]` 列表。
- 要求两份输入均为**非空列表**，否则 `ValueError`。
- 返回**新列表**：`a` 的条目在前，`b` 的条目紧随其后（纯列表拼接）。
- 不复制、不克隆、不修改任何条目对象；输出与输入共享元素引用。
- 不修改输入列表本身。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | conditioning_a | CONDITIONING | 是 | - |
| in | conditioning_b | CONDITIONING | 是 | - |
| out | conditioning | CONDITIONING | - | - |

## 4. 执行与缓存
确定性；无状态；无随机数。

## 5. 资源
仅新建长度为 `len(a)+len(b)` 的列表，不新建张量。

## 6. 副作用与安全
不修改输入（列表或条目）；不写文件；不触网。

## 7. 错误行为
- 非 `list` 输入 → `ValueError`；
- 空列表 → `ValueError`。

## 8. 对抗性反例
1. `len(out) == len(a) + len(b)`；
2. 顺序为 `a` 在前、`b` 在后；
3. `out[i] is a[i]` / `out[len(a)+j] is b[j]`（引用共享）；
4. 调用后 `a`、`b` 内容与长度不变；
5. 空 `a` 或空 `b` → `ValueError`。

## 9. 验收
`tests/test_flux_concat.py`。
