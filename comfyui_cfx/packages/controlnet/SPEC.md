# ComfyUI-ControlNet · SPEC

## 使命
ControlNet / IPAdapter / 预处理器的统一契约；高可靠上游保留设计。

## 不负责
语义分割模型本体（归 Segment）、深度后处理（归 Depth3D）。

## 来源（可包装）
controlnet_aux（**Apache-2.0**，高可靠）、advanced-controlnet、ipadapter_plus。

## 许可
MIT；包装宽松上游保留署名/NOTICE。

## 节点 ID 前缀
`comfyui_controlnet_<verb>_<noun>` · 分类 `ComfyUI-ControlNet/<Sub>`
