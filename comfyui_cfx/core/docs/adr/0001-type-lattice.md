# ADR-0001: 统一类型格

状态：Accepted（2026-09-23）
背景：现状至少 5 套隐式约定（Comfyroll 的 `show_help`、WAS 的 `"true"/"false"`、`easy ` 前缀、
mtb `(mtb)` 后缀、rgthree typed context），导致同名能力无法互换。

## 决策
`core/types.py` 定义唯一类型格，所有 cfx 节点只使用下列类型：

| 类型 | 载体 | 约定 |
|---|---|---|
| `IMAGE` | `torch.Tensor` | `[B,H,W,C]` float32，值 [0,1] |
| `MASK` | `torch.Tensor` | `[B,H,W]` float32，值 [0,1] |
| `LATENT` | `dict` | 至少含 `{"samples": [B,C,h,w]}` |
| `CONDITIONING` | `list` | ComfyUI 原生结构，透传 |
| `BOOLEAN` | Python `bool` | 不接受 `"true"/"false"` 字符串 |

## 规则
1. 一个输出只有一个类型；`OUTPUT_IS_LIST` 与类型语义一致。
2. 不做隐式跨类型转换（如 IMAGE→LATENT），必须经显式节点。
3. 张量布局在边界归一化；节点内部不做 CPU↔GPU 往返。
4. 旧约定只由迁移别名层吸收，不进入类型格。

## 后果
正：可组合、可测试、跨库一致。负：需要迁移别名层，旧工作流需一次转换。
