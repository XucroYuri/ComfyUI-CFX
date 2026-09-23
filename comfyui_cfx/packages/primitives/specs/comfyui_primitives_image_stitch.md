---
id: comfyui_primitives_image_stitch
display_name: "ComfyUI-Primitives · Image Stitch"
category: "ComfyUI-Primitives/Image"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "Image Stitch (WAS)"
  - "easy imageConcat"
  - "AGSoft_Image_Stitch / AGSoft_Image_Concatenate"
---

## 1. 目的
唯一图像拼接（横向/纵向，含间距与背景填充）。

## 2. 语义
- 最多 8 路 `image1..image8`，按顺序拼接。
- 横向要求高度一致；纵向要求宽度一致。batch 与通道数必须一致。
- `spacing` 为像素间距，用 `background` 填充。
- 单路输入直接透传。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | direction | COMBO | 是 | horizontal |
| in | spacing | INT | 是 | 0 |
| in | background | FLOAT | 是 | 0.0 |
| in | image1..image8 | IMAGE | 否 | - |
| out | image | IMAGE | - | - |

## 4. 执行与缓存
确定性；无随机。

## 5. 资源
输出张量大小 = 各输入之和 + 间距。

## 6. 副作用与安全
无。

## 7. 错误行为
- 无输入 → `ValueError`；
- 横向高度不一致 / 纵向宽度不一致 → `ValueError`；
- batch / 通道不一致 → `ValueError`。

## 8. 对抗性反例
1. 未连接槽跳过，不产生空洞；
2. 单路透传；
3. 尺寸不匹配 → 明确报错而非静默裁剪；
4. `spacing>0` 时输出尺寸正确。

## 9. 验收
`tests/test_primitives_image_stitch.py`。
