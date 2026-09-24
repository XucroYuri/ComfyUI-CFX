# 验证台账（Verification Matrix）

> 日期：2026-09-24
> 目的：把「真实推理验证」从探索变成**机械执行清单**，并让模型下载预算提前可见。
> 三层验证：**L1** = SPEC + 对抗性审查 + 纯逻辑单测；**L2** = 新模式冒烟（真实运行，每类模式一次）；
> **L3** = 收官逐节点真实验证（本表 `L3` 列）。

## 汇总

| 包 | 节点数 | L1 | L2（已冒烟） | L3 待做 |
|---|---|---|---|---|
| ComfyUI-Primitives | 14 | ✅ | 不需要（纯运算） | 0 |
| ComfyUI-Flow | 6 | ✅ | 不需要（纯运算/文本） | 0 |
| ComfyUI-Vision | 7 | ✅ | Florence-2 ✅ / WD14 ✅ / BLIP ✅ / VLM ✅ | 0 |
| ComfyUI-Segment | 6 | ✅ | SAM2 ✅ / FaceCrop ✅ / GDINO ✅ / Matting ✅ | 0 |
| ComfyUI-Resolve | 2 | ✅ | 模型放大 ✅ | 0 |
| ComfyUI-ControlNet | 2 | ✅ | cv2 确定性（建议冒烟） | 0 |
| ComfyUI-Inpaint | 3 | ✅ | 不需要（纯几何） | 0 |
| ComfyUI-Depth3D | 1 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Sampling | 2 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Video | 1 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Flux | 1 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Audio | 1 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Loaders | 1 | ✅ | 不需要（读文件头） | 0 |
| ComfyUI-Filter | 1 | ✅ | 不需要（纯张量） | 0 |
| **合计** | **48** | **✅** | **9 项已真实运行** | **0** |

## L3 明细（需要模型的节点）

| 节点 | 需要的模型/后端 | 体积 | 期望输出 | 状态 |
|---|---|---|---|---|
| `comfyui_vision_florence2_loader` / `_run` | comfyui-florence2 + PromptGen v2.0 | 已在本地 | tags 非空；检测任务返回 dict | ✅ 已通过 |
| `comfyui_segment_sam2_loader` / `_mask` | ComfyUI-segment-anything-2 + sam2.1_hiera_tiny-fp16 | 已在本地 | MASK `(1,H,W)`、二值、非空 | ✅ 已通过 |
| `comfyui_segment_face_crop` | ComfyUI-AutoCropFaces（权重随插件 1.7MB） | 0 | 无人脸返回原图；有脸返回裁剪 | ✅ 已通过 |
| `comfyui_vision_wd14_tagger` | SmilingWolf `wd-v1-4-moat-tagger-v2` | 已下载 ~0.31 GB | 非空标签串、含 general 标签 | ✅ 已通过（修复 3 处 bug） |
| `comfyui_vision_blip_caption` | `Salesforce/blip-image-captioning-base` | 已下载 ~1 GB | 非空英文描述 | ✅ 已通过（修复 1 处 bug） |
| `comfyui_vision_vlm_caption` | `Qwen/Qwen2.5-VL-3B-Instruct` | 已下载 ~8.8 GB | 非空描述 | ✅ 已通过（修复 1 处 bug；首次下载遇网络中断，续传成功） |
| `comfyui_segment_grounding_dino` | `IDEA-Research/grounding-dino-tiny` | 已下载 ~0.66 GB | boxes + MASK | ✅ 已通过（修复 2 处 bug，含 transformers 5 `threshold` 改名） |
| `comfyui_segment_matting` | rembg `u2net` | 已下载 ~0.18 GB | alpha MASK + RGBA | ✅ 已通过（修复 1 处 bug） |
| `comfyui_resolve_upscale_tiled` | 超分模型（已装 `RealESRGAN_x4plus.pth`） | 0.06 GB（已有） | 4x 尺寸、无接缝 | ✅ 已通过（修复 1 处 bug） |

**全部 L3 模型已就位**（WD14 + GDINO + u2net + BLIP + Qwen3B ≈ 9.9 GB；超分模型本机已有）；**剩余预算 0**。

## 全节点清单

| 节点 ID | 包 | L1 | L3 | 备注 |
|---|---|---|---|---|
| `comfyui_primitives_image_resize` | primitives | ✅ | N/A | 纯张量 |
| `comfyui_primitives_image_crop` | primitives | ✅ | N/A | 纯张量 |
| `comfyui_primitives_image_transform` | primitives | ✅ | N/A | 纯张量 |
| `comfyui_primitives_image_stitch` | primitives | ✅ | N/A | 纯张量 |
| `comfyui_primitives_image_batch` | primitives | ✅ | N/A | 纯张量 |
| `comfyui_primitives_image_split` | primitives | ✅ | N/A | 列表语义 |
| `comfyui_primitives_switch` | primitives | ✅ | N/A | any 路由 |
| `comfyui_primitives_boolean` | primitives | ✅ | N/A | 纯逻辑 |
| `comfyui_primitives_math` | primitives | ✅ | N/A | AST 白名单 |
| `comfyui_primitives_text` | primitives | ✅ | N/A | 纯文本 |
| `comfyui_primitives_mask_ops` | primitives | ✅ | N/A | scipy 填洞 |
| `comfyui_primitives_resolution` | primitives | ✅ | N/A | 纯计算 |
| `comfyui_primitives_seed` | primitives | ✅ | N/A | 纯逻辑 |
| `comfyui_primitives_save_image_metadata` | primitives | ✅ | 建议一次 | 建议跑一次确认写盘/元数据 |
| `comfyui_flow_string_function` | flow | ✅ | N/A | 纯文本 |
| `comfyui_flow_show_text` | flow | ✅ | N/A | UI 输出 |
| `comfyui_flow_constrain_image` | flow | ✅ | N/A | 纯张量 |
| `comfyui_flow_repeater` | flow | ✅ | N/A | 列表语义 |
| `comfyui_flow_load_text` | flow | ✅ | 建议一次 | 需配置 `CFX_TEXT_DIRS` |
| `comfyui_flow_save_text` | flow | ✅ | 建议一次 | 同上 |
| `comfyui_vision_florence2_loader` | vision | ✅ | ✅ | 见上 |
| `comfyui_vision_florence2_run` | vision | ✅ | ✅ | 见上 |
| `comfyui_vision_wd14_tagger` | vision | ✅ | ✅ | 见上（修复 3 处 bug） |
| `comfyui_vision_blip_caption` | vision | ✅ | ✅ | 见上（修复 1 处 bug） |
| `comfyui_vision_vlm_caption` | vision | ✅ | ✅ | 见上（修复 1 处 bug） |
| `comfyui_vision_caption_clean` | vision | ✅ | N/A | 纯文本 |
| `comfyui_vision_tags_filter` | vision | ✅ | N/A | 纯文本 |
| `comfyui_segment_annotations_to_mask` | segment | ✅ | N/A | 纯几何 |
| `comfyui_segment_grounding_dino` | segment | ✅ | ✅ | 见上（修复 2 处 bug） |
| `comfyui_segment_sam2_loader` | segment | ✅ | ✅ | 见上 |
| `comfyui_segment_sam2_mask` | segment | ✅ | ✅ | 见上 |
| `comfyui_segment_matting` | segment | ✅ | ✅ | 见上（修复 1 处 bug） |
| `comfyui_segment_face_crop` | segment | ✅ | ✅ | 见上 |
| `comfyui_resolve_scale_to_megapixels` | resolve | ✅ | N/A | 纯张量 |
| `comfyui_resolve_upscale_tiled` | resolve | ✅ | ✅ | 见上（修复 1 处 bug） |
| `comfyui_controlnet_canny` | controlnet | ✅ | 建议一次 | cv2，确定性 |
| `comfyui_controlnet_lineart` | controlnet | ✅ | 建议一次 | cv2，确定性（非神经近似） |
| `comfyui_inpaint_crop_by_mask` | inpaint | ✅ | N/A | 纯几何 |
| `comfyui_inpaint_stitch` | inpaint | ✅ | N/A | 纯几何 |
| `comfyui_inpaint_outpaint_canvas` | inpaint | ✅ | N/A | 纯几何 |
| `comfyui_depth3d_normalize_depth` | depth3d | ✅ | N/A | 纯张量 |
| `comfyui_sampling_split_sigmas` | sampling | ✅ | N/A | 纯张量 |
| `comfyui_sampling_sigma_shift` | sampling | ✅ | N/A | 纯张量 |
| `comfyui_video_frame_range` | video | ✅ | N/A | 纯张量 |
| `comfyui_flux_conditioning_blend` | flux | ✅ | N/A | 纯张量 |
| `comfyui_audio_trim_silence` | audio | ✅ | N/A | 纯张量 |
| `comfyui_loaders_gguf_header` | loaders | ✅ | N/A | 读文件头 + 路径校验 |
| `comfyui_filter_high_pass` | filter | ✅ | N/A | 纯张量 |

## 收官执行清单（L3）

```bat
set COMFYUI_PATH=D:\path\to\ComfyUI
python tools\verify\florence2.py
python tools\verify\sam2.py
python tools\verify\facecrop.py
```

WD14 / BLIP / VLM / GroundingDINO / Matting 的脚本将在对应节点开发/复核时补入
`tools/verify/`（命名 `<node>.py`），并在此表把 ⏳ 改为 ✅ 或记录的失败原因。
