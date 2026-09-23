---
id: comfyui_primitives_switch
display_name: "ComfyUI-Primitives · Switch"
category: "ComfyUI-Primitives/Logic"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "CR *Input Switch (Comfyroll)"
  - "Image/Latent/... Input Switch (WAS)"
  - "easy *IndexSwitch (easy-use)"
  - "TwoWaySwitch / ThreeWaySwitch (controlaltai)"
  - "YCSwitch"
---

## 1. 目的
唯一 any 类型路由/开关，替代按类型分裂的约 45 个旧开关。

## 2. 语义
- `mode=index`：选择 `input{index+1}`（0-based），索引越界时 clamp 到 `[0,7]`。
- `mode=first_connected`：按 `input1..input8` 顺序返回第一个非 `None` 的输入。
- "未连接" 以 `None` 表示。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | mode | COMBO | 是 | index | index / first_connected |
| in | index | INT | 是 | 0 | 0..7 |
| in | input1..input8 | * | 否 | - | 任意类型 |
| out | value | * | - | - | 选中值 |
| out | selected_index | INT | - | - | 实际位置 |

## 4. 执行与缓存
确定性；无随机；不定义 `IS_CHANGED`。

## 5. 资源
无模型、无显存；纯 Python 引用传递。

## 6. 副作用与安全
无文件/网络；不修改输入对象。

## 7. 错误行为
- 选中输入未连接 → `ValueError`（不静默返回 None）。
- `first_connected` 且全部未连接 → `ValueError`。

## 8. 对抗性反例
1. `index` 为负或 >7 → clamp；
2. 选中槽未连接 → 报错；
3. 值为 `0`/`False`/空字符串 → 视为"已连接"（`is not None`）；
4. `first_connected` 中前面槽为 None → 跳过。

## 9. 验收
`tests/test_primitives_switch.py`。
