---
id: comfyui_controlnet_canny
display_name: "ComfyUI-ControlNet · Canny"
category: "ComfyUI-ControlNet/Preprocessors"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "CannyEdgePreprocessor (controlnet_aux)"
  - "Canny (comfyui_controlnet_aux)"
---

## 1. 目的
提供确定性、无模型、无网络的 Canny 边缘预处理器，供 ControlNet 条件图使用。
同一节点同时输出三通道边缘图（`IMAGE`）与单通道边缘掩码（`MASK`），避免下游重复计算。

## 2. 语义
- 输入 `IMAGE` 经 `core.types.ensure_image` 归一为 `[B,H,W,C]` float32。
- 仅取 batch 第一项 `[H,W,C]` 参与计算（batch>1 时其余丢弃）。
- 灰度（亮度）加权：`0.299R + 0.587G + 0.114B`；单通道输入直接复制为三通道。
  灰度按 `*255` 后 clamp 到 `[0,255]` 并量化为 `uint8`。
- 调用 `cv2.Canny(gray, low_threshold, high_threshold, apertureSize=aperture_size)`，
  输出二值 `uint8`（0/255）。
- 输出 `image`：边缘值 `/255` 后复制到 3 通道，形状 `[1,H,W,3]`，值域 `[0,1]`。
- 输出 `mask`：同一份边缘，形状 `[1,H,W]`，值域 `[0,1]`。
- `low_threshold`、`high_threshold` 为 `double` 传给 OpenCV；`aperture_size` 只允许 3/5/7。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | image | IMAGE | 是 | - | BHWC float32；取 batch 第一项 |
| in | low_threshold | FLOAT | 是 | 100 | 滞后低阈值，[0,255] |
| in | high_threshold | FLOAT | 是 | 200 | 滞后高阈值，[0,255] |
| in | aperture_size | INT | 是 | 3 | Sobel 孔径，3/5/7，步长 2 |
| out | image | IMAGE | - | - | 边缘图 [1,H,W,3] |
| out | mask | MASK | - | - | 边缘掩码 [1,H,W] |

## 4. 执行与缓存
- 确定性：同输入逐元素可复现；无随机性。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。
- 无模型、无全局状态，重复执行结果一致。

## 5. 资源
- 纯 CPU numpy/OpenCV 运算；峰值内存 ≈ 灰度图 + 边缘图。
- `cv2` **运行时惰性导入**，模块导入本身不要求 OpenCV 可用。
- 输出张量 float32。

## 6. 副作用与安全
- 无文件、无网络、无全局状态修改。
- 不写入 shared/temp 目录。

## 7. 错误行为
- `high_threshold < low_threshold` → `ValueError`（不静默交换）。
- 非张量 / 非法 shape → 由 `core.types.ensure_image` 抛出清晰异常。
- 运行时缺少 OpenCV → `import cv2` 抛 `ImportError`（不静默降级）。

## 8. 对抗性反例
1. `high_threshold < low_threshold` → 必须报错，不得自动交换；
2. 全黑/全白图 → 边缘为 0，输出形状不变；
3. 黑底白方块 → 方块边界产生非零边缘；
4. 高阈值相对低阈值 → 边缘数量单调不增（`count(high) <= count(low)`）；
5. batch>1 → 只处理第一张，输出 batch 恒为 1。

## 9. 验收
- `tests/test_controlnet_canny.py`：形状、合成边缘、阈值单调性、异常、值域；
- CPU 上 fp32 断言；`cv2`/`comfy.utils` 缺失时 skip；
- `tools/spec_lint.py` 与 `tools/license_gate.py` 通过。
