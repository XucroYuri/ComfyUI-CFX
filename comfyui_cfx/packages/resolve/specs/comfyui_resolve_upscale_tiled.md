---
id: comfyui_resolve_upscale_tiled
display_name: "ComfyUI-Resolve · Upscale (Tiled)"
category: "ComfyUI-Resolve/Upscale"
version: 1.0.0
license: MIT
since: 2026-09-24
requires:
  - UPSCALE_MODEL
replaces:
  - "UltimateSDUpscale (tiled model upscale)"
---

## 1. 目的
用放大模型对图像做分块（tile）放大，降低单块显存占用，并把分块结果羽化拼接为无缝整图。
面向大图超分、显存受限场景；放大算法本身复用 ComfyUI 核心的 `ImageUpscaleWithModel`。

## 2. 语义
- 输入归一：`core.types.ensure_image`（HWC/BHWC/BCHW → BHWC float32）。
- **仅处理 batch 的第 0 张**（`ensure_image(image)[0]`），输出 batch 恒为 1。
- 分块：对 H/W 分别调用 `tile_ranges(length, tile, overlap)` 得到半开区间 `[start, end)`。
  - `tile >= length` → 单窗口 `[(0, length)]`。
  - 否则步长 `step = max(1, tile - overlap)`，逐窗口推进；末窗口若越界则回退起点，
    使其在可能时仍保持 `tile` 宽，并保证末端恰好到达 `length`。
- 放大：每个窗口 `upscaled = ImageUpscaleWithModel().upscale(upscale_model, tile_bhwc)`；
  输出缩放系数由**首个**窗口推导 `scale = out_w / tile_w`（模型尺度恒定）。
- 输出画布：`[1, round(H*scale), round(W*scale), C]`。
- 拼接：对每块构造可分离羽化权重（每轴 `_axis_weights`）：
  - 内部边沿在 `overlap*scale` 像素内 0→1 线性渐变；
  - 画布边界（无邻块一侧）权重恒为 1，保证每个像素至少被一个块覆盖。
  - 累积 `canvas += tile * weight`、`acc += weight`，最后 `canvas / acc`（`acc` 下限 `1e-8`）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| in | upscale_model | UPSCALE_MODEL | 是 | - | 运行时需提供放大模型 |
| in | image | IMAGE | 是 | - | BHWC float32，仅取第 0 张 |
| in | tile_size | INT | 是 | 512 | min 64 max 4096 |
| in | overlap | INT | 是 | 32 | min 0 max 512，须 `< tile_size` |
| out | image | IMAGE | - | - | `[1, H*scale, W*scale, C]` |

## 4. 执行与缓存
- 确定性：给定模型与输入逐元素可复现；无随机性。
- 不定义 `IS_CHANGED`（沿用输入哈希缓存）。
- 放大模型在运行时经 `UPSCALE_MODEL` 传入；本节点不加载、不缓存模型。

## 5. 资源
- 显存 ≈ 单个 tile 的输入/输出 + 输出画布 + 权重累加器；峰值随 `tile_size` 而非原图线性增长。
- 画布与累加器为 float32；权重逐块生成后即释放。

## 6. 副作用与安全
无文件/网络访问；无全局状态；不修改传入模型。

## 7. 错误行为
- `overlap >= tile_size` → `ValueError`（分块无重叠意义且权重退化）。
- 放大结果为空张量 → `ValueError("upscale model returned an empty tile")`。
- 非张量/非法 shape → 由 `core.types.ensure_image` 抛出 `TypeError`/`ValueError`。
- 模型执行失败 → 由 `ImageUpscaleWithModel.upscale` 向上抛出。

## 8. 对抗性反例
1. `tile_size >= 边长` → 单窗口，输出等于整图一次放大；
2. `overlap = 0` → 无羽化，块间无缝但不重叠；
3. `overlap >= tile_size` → 抛 `ValueError`；
4. 非整除尺寸 → 末窗口回退且保持 `tile` 宽，`tile_ranges` 完整覆盖 `[0,length)`；
5. batch=N>1 → 仅处理第 0 张，输出 batch=1；
6. 画布四边权重为 1 → 不存在零权重像素（`acc > 0`）。

## 9. 验收
- `tests/test_resolve_upscale.py`：以 2x nearest 桩替换 `ImageUpscaleWithModel`，
  断言输出形状 `[1, H*2, W*2, C]` 且与整图 2x nearest 参考在容差内一致；
- 覆盖 `tile_ranges` 的单窗口、精确切分、逐索引覆盖、末窗口终止于 `length`；
- 覆盖 `overlap >= tile_size` 抛错；无需真实模型文件。
