---
id: comfyui_loaders_safetensors_info
display_name: "ComfyUI-Loaders · Safetensors Info"
category: "ComfyUI-Loaders/Quant"
version: 1.0.0
license: MIT
since: 2026-09-24
---

## 1. 目的
在不加载权重的前提下，读取 `.safetensors` 文件的张量计数、dtype 直方图与元数据键，供工作流做模型格式自检与分支决策。

## 2. 语义
- `path` 为**相对 ComfyUI models 目录**的路径；用 `core.paths.safe_join(folder_paths.models_dir, path)` 解析并做包含性校验。
- 以 `safetensors.safe_open(path, framework="pt")` 打开（仅解析头部/偏移，不读取权重负载）：
  - `keys = list(handle.keys())`；
  - 每个键的 dtype 取自 `handle.get_slice(key).get_dtype()`（如 `"F32"`、`"I8"`），累加成直方图；
  - 元数据键取自 `handle.metadata()`；无元数据时视为空。
- 返回单个 JSON 值：`{"tensor_count": len(keys), "dtypes": {dtype: count, ...}, "metadata_keys": sorted(metadata_keys)}`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | path | STRING | 是 | ""（相对 models 目录的 `.safetensors`） |
| out | info | JSON | - | - |

## 4. 执行与缓存
- `run` 为纯头部/元数据读取，无随机性；相同文件产生相同输出。
- 输入路径变化即重算；权重负载不读取、不参与。

## 5. 资源
- 仅按需读取头部与各张量 slice 的 dtype 元信息，不实例化张量；不分配权重内存。

## 6. 副作用与安全
- **路径包含**：`safe_join` 拒绝空路径、绝对路径与 `..` 越界，任何读取均限于 `folder_paths.models_dir` 之内。
- 只读打开，不写入、不修改被读文件。
- 不执行模型代码。

## 7. 错误行为
- 空 / 绝对 / 越界 `path` → `ValueError`（`safe_join`）。
- 文件不存在或不可读 → `FileNotFoundError` / `OSError`。
- 无法作为 safetensors 打开（头部损坏等 `safetensors.SafetensorError`）→ `ValueError("not a safetensors file: ...")`。

## 8. 对抗性反例
1. 含 `float32` 与 `int8` 两张量、单个元数据键的文件 → `tensor_count == 2`，dtypes 为 `{"F32": 1, "I8": 1}`，`metadata_keys == ["x"]`；
2. 无元数据文件 → `metadata_keys == []`；
3. `path="../evil.safetensors"` → `ValueError`，不读取 models 目录之外；
4. 非 safetensors 字节内容 → `ValueError`；
5. `path` 为绝对路径 → `ValueError`。

## 9. 验收
`tests/test_loaders_safetensors.py`。
