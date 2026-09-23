---
id: comfyui_primitives_math
display_name: "ComfyUI-Primitives · Math"
category: "ComfyUI-Primitives/Math"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "MathExpression|pysssss (custom-scripts)"
  - "SimpleMath+ (essentials)"
  - "AGSoftMathExpression"
  - "easy math* / simpleMath* (easy-use)"
  - "Math Expression (mtb)"
  - "Number Operation (WAS)"
---

## 1. 目的
唯一数值表达式求值，替代 ~40 个数学节点。

## 2. 语义
在 `a,b,c` 与常量 `pi,e` 上求值 `expression`，输出 `int` 与 `float`。
函数白名单：`min,max,abs,round,floor,ceil,sqrt,pow,sum,len`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | expression | STRING | 是 | `a + b` |
| in | a/b/c | INT,FLOAT | 否 | 0 |
| out | int | INT | - | - |
| out | float | FLOAT | - | - |

## 4. 执行与缓存
确定性；无随机（随机归 Seed 节点）。

## 5. 资源
纯 Python/AST。

## 6. 副作用与安全
**AST 白名单**：拒绝属性访问、下标、推导式、lambda、导入、赋值等；
`eval` 以 `{"__builtins__": {}}` 执行，名字解析仅限白名单。

## 7. 错误行为
空表达式 / 超长（>4096）/ 非法语法 / 未知名字 / 除零 / 非有限结果 / 非数值结果 → `ValueError`。

## 8. 对抗性反例
1. `__import__("os").system("...")` → 拒绝（Call 目标不在白名单）；
2. `a.__class__` → 拒绝（Attribute 不允许）；
3. `1/0` → `ValueError`；
4. `sqrt(-1)` → 非有限 → `ValueError`；
5. 超长表达式 → `ValueError`；
6. `open("x")` → 未知名字 → `ValueError`。

## 9. 验收
`tests/test_primitives_math.py`。
