# ComfyUI-Core · SPEC

## 使命
唯一类型格 + 设备/dtype/显存/路径安全/日志底座，被所有 `ComfyUI-*` 依赖。

## 不负责
任何业务节点；**不 import `transformers`**。

## 许可
MIT。

## 模块
| 模块 | 说明 |
|---|---|
| `types.py` | ADR-0001 类型格与转换 |
| `device.py` | compute/offload 设备与 dtype 解析 |
| `memory.py` | 统一的模型释放序列 |
| `paths.py` | 路径归属校验（路径安全） |
| `logging.py` | 一次性告警 |

## 决策
- `docs/adr/0001-type-lattice.md`
- `docs/adr/0002-dependency-baseline.md`
