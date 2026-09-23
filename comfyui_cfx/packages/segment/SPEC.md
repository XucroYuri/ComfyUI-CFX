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

## 依赖约束与范围（已定）
- 文本检测统一走 `transformers.AutoModelForZeroShotObjectDetection`，弃 `groundingdino-py` 与 vendored fork（三套→一套）。
- 抠图使用 `rembg`（MIT）；FaceCrop 复用 `ComfyUI-AutoCropFaces`（MIT）；SAM2 复用 `ComfyUI-segment-anything-2`（Apache-2.0）。
- **GPL 只重写行为**：`rmbg`、`impact-pack` 的对应节点不得复制代码。
- SAM2：保留**一份** Apache 实现（后续 M2）；不再 vendor 第二份。
- 删除计划：neverbiasu `comfyui-sam2`（与 kijai SAM2 100% 冗余）、`AGSoft/Pytorch_Retinaface`（与 AutoCropFaces 同源副本）、
  rmbg `AILab_Florence2*`、rmbg vendored `models/sam2`、rmbg `SegmentV1+V2` 与重复 Segformer 文件。

## 节点 ID 前缀
`comfyui_segment_<verb>_<noun>` · 分类 `ComfyUI-Segment/<Sub>`
