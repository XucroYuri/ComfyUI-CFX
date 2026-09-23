---
id: comfyui_primitives_image_batch
display_name: "ComfyUI-Primitives · Image Batch"
category: "ComfyUI-Primitives/Batch"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Image Batch (WAS)"
  - "easy joinImageBatch"
  - "ImageBatchMultiple+ (essentials)"
---

## 1. 目的
把最多 8 路 IMAGE 合并为一个 batch（沿 batch 维拼接）。

## 2. 语义
按 `image1..image8` 顺序沿 dim=0 拼接；要求 H/W/C 完全一致，否则明确报错。
单路输入直接透传。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 |
|---|---|---|---|
| in | image1..image8 | IMAGE | 否 |
| out | images | IMAGE | - |

## 4. 执行与缓存
确定性。

## 5. 资源
输出显存/内存 = 各输入之和（`torch.cat` 复制）。

## 6. 副作用与安全
无。

## 7. 错误行为
无输入 / 尺寸或通道不一致 → `ValueError`。

## 8. 对抗性反例
1. 无输入 → 报错；
2. 尺寸不一致 → 报错而非静默裁剪；
3. 单路 → 透传；
4. batch=1 的多个输入 → 合并后 batch=N。

## 9. 验收
`tests/test_primitives_batch.py`。
