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
| `images.py` | IMAGE↔PIL 转换（模型节点共用，杜绝 `.clamp` on ndarray 一类重复缺陷） |
| `logging.py` | 一次性告警 |
| `anytype.py` | 任意类型 socket 助手 |

> `memory.py`（统一释放助手）已移除：当前无节点调用，遵循"无死代码"原则，待有模型节点需要时再加。

## 决策
- `docs/adr/0001-type-lattice.md`
- `docs/adr/0002-dependency-baseline.md`
