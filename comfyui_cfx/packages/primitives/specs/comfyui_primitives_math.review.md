# Adversarial Review: comfyui_primitives_math

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- AST 白名单：仅允许 Expression/BinOp/UnaryOp/Compare/BoolOp/IfExp/Call/Name/Constant 及运算符节点。
- 注入阻挡：`__import__`、属性访问、下标、lambda、推导式均被拒绝（有测试）。
- `eval` 环境：`{"__builtins__": {}}`，名字解析仅限白名单函数与常量。
- 失败行为：除零、非有限、非数值、空/超长表达式均 `ValueError`。
- 确定性：无随机源。

## 未决疑点
1. `sum`/`len` 目前无序列来源，实际用途有限；保留但非核心。
2. 尺寸内省（`.width`）显式**不**支持，避免开放 Attribute 攻击面；如需另设专用节点。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| `__import__('os')` | 拒绝 | PASS |
| `a.__class__` | 拒绝 | PASS |
| `1/0` | 报错 | PASS |
| `sqrt(-1)` | 报错 | PASS |
| 超长表达式 | 报错 | PASS |
| `open('x')` | 未知名字报错 | PASS |
