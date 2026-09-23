---
id: comfyui_segment_sam2_loader
display_name: "ComfyUI-Segment · SAM2 Loader"
category: "ComfyUI-Segment/Loaders"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "DownloadAndLoadSAM2Model (ComfyUI-segment-anything-2，作为后端复用而非替代)"
  - "SAM2ModelLoader (comfyui-sam2，重复实现)"
---

## 1. 目的
统一的 SAM2 加载入口，**复用** `ComfyUI-segment-anything-2`（Apache-2.0）的自带实现，
避免再 vendor 一份。

## 2. 语义
- 模型 8 个 checkpoint（2.0/2.1 × tiny/small/base+/large）；
- `segmentor ∈ {single_image, video}`；
- 设备由 `model_management.get_torch_device()` 推导；CPU 上强制 fp32（一次性告警）；
- 通过上游 `DownloadAndLoadSAM2Model().loadmodel(...)` 返回句柄 dict（类型 `CFX_SAM2`）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | model | COMBO | 是 | sam2.1_hiera_large.safetensors |
| in | segmentor | COMBO | 是 | single_image |
| in | precision | COMBO | 是 | fp16 |
| out | sam2 | CFX_SAM2 | - | - |

## 4. 执行与缓存
模型由上游加载/管理；句柄在图中传递，`keep_model_loaded` 在掩码节点控制。

## 5. 资源
按 precision 载入；CPU 强制 fp32。

## 6. 副作用与安全
首次使用下载 checkpoint（用户触发）。

## 7. 错误行为
后端缺失 → `FileNotFoundError`（含期望目录）；未知精度 → 枚举约束。

## 8. 对抗性反例
1. CPU + fp16 → 自动降为 fp32 并告警；
2. `CFX_SAM2_DIR` 覆盖路径；
3. 后端不存在 → 清晰报错。

## 9. 验收
`tests/test_segment_sam2.py`（后端定位/接口）；真实推理人工 VERIFY。
