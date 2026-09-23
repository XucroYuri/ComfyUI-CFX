# ComfyUI-Segment · SPEC

## 使命
分割/抠图/检测/人脸的统一节点面与单一模型来源。

## 不负责
语义分割预处理器（归 ControlNet 域）、深度（归 Depth3D）。

## 来源
rmbg（**GPL-3.0**）、impact-pack（**GPL-3.0**）、segment-anything-2（Apache-2.0）、
sam2（Apache 声明）、AutoCropFaces（MIT）、florence2（MIT）、controlnet_aux（Apache-2.0）、
essentials（MIT）。

## 许可
本包 MIT。**GPL 只重写行为**；保留 Apache/MIT 资产。

## 依赖约束
- 文本检测统一走 `transformers.AutoModelForZeroShotObjectDetection`，弃 `groundingdino-py` 与 vendored fork。

## 节点 ID 前缀
`comfyui_segment_<verb>_<noun>` · 分类 `ComfyUI-Segment/<Sub>`
