---
id: comfyui_flow_repeater
display_name: "ComfyUI-Flow · Repeater"
category: "ComfyUI-Flow/Util"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Repeater|pysssss"
---

## 1. 目的
把同一值重复成列表，供列表语义下游逐项执行。

## 2. 语义
`OUTPUT_IS_LIST=(True,)`；返回 `[value] * repeats`（同一对象引用，不做拷贝）。
类型为 any。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | value | * | 是 | - |
| in | repeats | INT | 是 | 2（1..64） |
| out | values | LIST[*] | - | - |

## 4. 执行与缓存
确定性。

## 5. 资源
仅列表引用。

## 6. 副作用与安全
无；不复制大型张量。

## 7. 错误行为
`repeats` 由 widget 约束在 1..64。

## 8. 对抗性反例
1. `repeats=1` → 单元素列表；
2. 大张量重复 → 仅引用，不额外占显存；
3. any 类型下接不同下游。

## 9. 验收
`tests/test_flow_repeater.py`。
