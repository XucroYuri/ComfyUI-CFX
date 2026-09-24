---
id: comfyui_controlnet_lineart
display_name: "ComfyUI-ControlNet · Lineart"
category: "ComfyUI-ControlNet/Preprocessors"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "AnimeLineArtPreprocessor (controlnet_aux)"
  - "LineArtPreprocessor (comfyui_controlnet_aux)"
---

## 1. 目的
提供确定性、无模型、无网络的线稿（lineart）预处理器，供 ControlNet 条件图使用。
同一节点同时输出三通道线稿图（`IMAGE`）与单通道线稿掩码（`MASK`），避免下游重复计算。

**诚实声明**：本节点是 `AnimeLineArtPreprocessor` 的**非神经、确定性近似**，
**不是**神经 AnimeLineArt 模型。它不加载任何权重，只用 OpenCV 自适应阈值提取暗线，
对照片、阴影和纹理的鲁棒性弱于神经模型；对干净线稿/卡通/二值图更稳定。

## 2. 语义
- 输入 `IMAGE` 经 `core.types.ensure_image` 归一为 `[B,H,W,C]` float32。
- 仅取 batch 第一项 `[H,W,C]` 参与计算（batch>1 时其余丢弃）。
- 灰度（亮度）加权：`0.299R + 0.587G + 0.114B`；单通道输入直接复制为三通道。
  灰度按 `*255` 后 clamp 到 `[0,255]` 并量化为 `uint8`。
- 高斯平滑：`cv2.GaussianBlur(gray, (3,3), 0)`。
- 线提取：`cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
  cv2.THRESH_BINARY_INV, block_size, C)`，其中 `C = max(1, round(strength * 50))`。
- `invert=True`（默认）：线为 `255`（亮线黑底），即输出中 `1 = line`。
- `invert=False`：对结果取反，线为暗线白底（`0 = line`，`1 = 背景`）。
- 输出 `image`：线稿值 `/255` 后复制到 3 通道，形状 `[1,H,W,3]`，值域 `[0,1]`。
- 输出 `mask`：同一份线稿，形状 `[1,H,W]`，值域 `[0,1]`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | image | IMAGE | 是 | - | BHWC float32；取 batch 第一项 |
| in | block_size | INT | 是 | 9 | 自适应阈值窗口，奇数且 ≥3，步长 2，[3,255] |
| in | strength | FLOAT | 是 | 0.5 | 映射为阈值常数 `C=max(1,round(strength*50))`，[0,1] |
| in | invert | BOOLEAN | 是 | True | True=亮线黑底；False=暗线白底 |
| out | image | IMAGE | - | - | 线稿图 [1,H,W,3] |
| out | mask | MASK | - | - | 线稿掩码 [1,H,W] |

## 4. 执行与缓存
- 确定性：同输入逐元素可复现；无随机性。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。
- 无模型、无全局状态，重复执行结果一致。

## 5. 资源
- 纯 CPU numpy/OpenCV 运算；峰值内存 ≈ 灰度图 + 平滑图 + 阈值图。
- `cv2` **运行时惰性导入**，模块导入本身不要求 OpenCV 可用。
- 输出张量 float32。

## 6. 副作用与安全
- 无文件、无网络、无全局状态修改。
- 不写入 shared/temp 目录。

## 7. 错误行为
- `block_size` 为偶数或 `< 3` → `ValueError`（不静默修正）。
- 非张量 / 非法 shape → 由 `core.types.ensure_image` 抛出清晰异常。
- 运行时缺少 OpenCV → `import cv2` 抛 `ImportError`（不静默降级）。

## 8. 对抗性反例
1. `block_size` 偶数（如 10）→ 必须报错，不得向上取奇；
2. `block_size < 3`（如 1）→ 必须报错；
3. 全黑/全白图 → 输出形状不变（自适应阈值在平坦区不产生线）；
4. 白底黑矩形 → 产生非零线像素；
5. `invert=False` 的输出必须与 `invert=True` 不同（互补）；
6. batch>1 → 只处理第一张，输出 batch 恒为 1。

## 9. 验收
- `tests/test_controlnet_lineart.py`：形状、合成线像素、`invert` 差异、异常、值域；
- CPU 上 fp32 断言；`cv2`/`comfy.utils` 缺失时 skip；
- `tools/spec_lint.py` 与 `tools/license_gate.py` 通过；
- SPEC 明确声明为确定性非神经近似。
