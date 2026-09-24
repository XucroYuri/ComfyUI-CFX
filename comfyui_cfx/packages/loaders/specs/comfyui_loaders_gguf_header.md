---
id: comfyui_loaders_gguf_header
display_name: "ComfyUI-Loaders · GGUF Header"
category: "ComfyUI-Loaders/Quant"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
在不加载权重的前提下，读取 `.gguf` 文件头的元信息（版本、张量数、元数据 KV 数），供工作流做模型格式自检与分支决策。

## 2. 语义
- `path` 为**相对 ComfyUI models 目录**的路径；用 `core.paths.safe_join(folder_paths.models_dir, path)` 解析并做包含性校验。
- 以二进制打开文件，仅读取头部固定 24 字节：
  - 偏移 0，4 字节：魔数，必须等于 `b"GGUF"`，否则 `ValueError("not a GGUF file")`；
  - 偏移 4，uint32 小端：`version`；
  - 偏移 8，uint64 小端：`tensor_count`；
  - 偏移 16，uint64 小端：`metadata_kv_count`。
- 返回单个 JSON 值：`{"magic": "GGUF", "version": v, "tensor_count": t, "metadata_kv_count": k}`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | path | STRING | 是 | ""（相对 models 目录的 `.gguf`） |
| out | info | JSON | - | - |

## 4. 执行与缓存
- `run` 为纯头部读取，无随机性；相同文件头部产生相同输出。
- 头部字节参与 ComfyUI 缓存键（输入路径变化即重算）；权重负载不读取、不参与。

## 5. 资源
- 仅读 24 字节（`file.read(24)`），与文件大小、张量规模无关；不分配权重内存。

## 6. 副作用与安全
- **路径包含**：`safe_join` 拒绝空路径、绝对路径与 `..` 越界，任何读取均限于 `folder_paths.models_dir` 之内。
- 只读打开（`"rb"`），不写入、不修改被读文件。
- 不执行模型代码，不反序列化张量。

## 7. 错误行为
- 空 / 绝对 / 越界 `path` → `ValueError`（`safe_join`）。
- 文件不存在或不可读 → `FileNotFoundError` / `OSError`。
- 前 4 字节非 `b"GGUF"`（含不足 4 字节）→ `ValueError("not a GGUF file")`。
- 魔数正确但头部不足 24 字节 → `ValueError("truncated GGUF header")`。
- 版本非 2/3 不做额外限制：仍按 v2/v3 布局解析（本节点只解析公共头部）。

## 8. 对抗性反例
1. 合法 v3 头 → 返回 `version=3` 与正确的 `tensor_count`/`metadata_kv_count`；
2. 合法 v2 头 → 返回 `version=2`；
3. 魔数为 `b"NOPE"` → `ValueError("not a GGUF file")`；
4. 魔数正确但仅 8 字节 → `ValueError("truncated GGUF header")`；
5. `path="../evil.gguf"` → `ValueError`，不读取 models 目录之外；
6. `path` 为绝对路径 → `ValueError`；
7. 空文件（0 字节）→ 魔数校验失败 → `ValueError("not a GGUF file")`。

## 9. 验收
`tests/test_loaders_quant.py`。
