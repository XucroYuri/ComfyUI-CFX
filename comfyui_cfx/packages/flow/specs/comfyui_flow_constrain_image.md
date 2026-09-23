---
id: comfyui_flow_constrain_image
display_name: "ComfyUI-Flow · Constrain Image"
category: "ComfyUI-Flow/Image"
version: 1.0.0
license: MIT
since: 2026-09-23
replaces:
  - "ConstrainImage|pysssss"
  - "ConstrainImageforVideo|pysssss"
---

## 1. 目的
把图像约束到最大尺寸框内（contain），或裁切到恰好覆盖该框（cover）。

## 2. 语义
- `crop_if_required=false`（contain）：`scale = min(1, max_w/w, max_h/h)`，只缩不放。
- `crop_if_required=true`（cover）：`scale = max(max_w/w, max_h/h)` 放大/缩小以覆盖，
  再居中裁切到 `max_w × max_h`。
- 采样走 `comfy.utils.common_upscale`。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | max_width / max_height | INT | 是 | 1024 |
| in | crop_if_required | BOOLEAN | 是 | False |
| in | upscale_method | COMBO | 是 | bicubic |
| out | image | IMAGE | - | - |
| out | width / height | INT | - | - |

## 4. 执行与缓存
确定性。

## 5. 资源
纯张量。

## 6. 副作用与安全
无。

## 7. 错误行为
非法 shape → `ValueError`（`ensure_image`）。

## 8. 对抗性反例
1. 图像小于框且 `crop=false` → 原样（不放大）；
2. 超宽图 → 按宽约束；
3. `crop=true` 且图像小于框 → 放大后裁切到框；
4. 极端宽高比 → 至少 1px。

## 9. 验收
`tests/test_flow_constrain_image.py`。
