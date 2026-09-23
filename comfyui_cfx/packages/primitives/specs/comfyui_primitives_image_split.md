---
id: comfyui_primitives_image_split
display_name: "ComfyUI-Primitives · Image Split"
category: "ComfyUI-Primitives/Batch"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "ImageBatchToImageList"
  - "ImageBatchSplitter //Inspire"
---

## 1. 目的
把 batch 拆成 `LIST[IMAGE]`（每项 batch=1），供列表语义的下游按项执行。

## 2. 语义
`OUTPUT_IS_LIST=(True,)`；返回 `[img[i:i+1] for i in range(B)]`，保持设备与 dtype。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 |
|---|---|---|---|
| in | image | IMAGE | 是 |
| out | images | LIST[IMAGE] | - |

## 4. 执行与缓存
确定性。

## 5. 资源
列表项为切片后 `contiguous` 拷贝。

## 6. 副作用与安全
无。

## 7. 错误行为
非法 shape → `ValueError`（来自 `ensure_image`）。

## 8. 对抗性反例
1. batch=1 → 单项列表；
2. batch=N → 顺序与输入一致；
3. 每项 shape 为 `[1,H,W,C]`。

## 9. 验收
`tests/test_primitives_batch.py`。
