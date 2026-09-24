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
| ComfyUI-Vision | 10 | ✅ | Florence-2 ✅ / Region ✅ / WD14 ✅ / BLIP ✅ / VLM ✅ / CLIP-IR ✅ | 1（BLIP2 下载中） |
| ComfyUI-Segment | 12 | ✅ | SAM2(框/点/自动) ✅ / FaceCrop ✅ / GDINO ✅ / Matting ✅ / Text→Mask ✅ | 0 |
| ComfyUI-Resolve | 2 | ✅ | 模型放大 ✅ | 0 |
| ComfyUI-ControlNet | 3 | ✅ | cv2 确定性（建议冒烟） | 0 |
| ComfyUI-Inpaint | 4 | ✅ | 不需要（纯几何） | 0 |
| ComfyUI-Depth3D | 2 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Sampling | 2 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Video | 2 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Flux | 2 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Audio | 2 | ✅ | 不需要（纯张量） | 0 |
| ComfyUI-Loaders | 2 | ✅ | 不需要（读文件头/元数据） | 0 |
| ComfyUI-Filter | 2 | ✅ | 不需要（纯张量） | 0 |
| **合计** | **65** | **✅** | **14 项已真实运行** | **1（BLIP2）** |

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
| `comfyui_segment_sam2_points` | SAM2 点位提示（复用已有 checkpoint） | 0（已有） | MASK `(1,H,W)`、非空 | ✅ 已通过 |
| `comfyui_segment_text_to_mask` | GroundingDINO-tiny + SAM2 | 0（已有） | 检测框 + 非空 MASK | ✅ 已通过（3 框，覆盖 0.299）|
| `comfyui_vision_clip_interrogator` | CLIP `ViT-L-14/openai` + BLIP | 已下载 ~2 GB | 非空英文描述 | ✅ 已通过 |
| `comfyui_vision_florence2_region` | Florence-2（本机已有） | 0 | 区域描述非空且**无 loc token 回显** | ✅ 已通过（修复 loc token 清理） |
| `comfyui_vision_blip2_caption` | `Salesforce/blip2-opt-2.7b` | ~15 GB | 非空英文描述 | ⏳ 下载中 |
| `comfyui_segment_sam2_auto_mask` | SAM2 自动分割（复用已有 checkpoint） | 0（已有） | MASK + 多个区域 | ✅ 已通过（23 个区域） |
| `comfyui_resolve_upscale_tiled` | 超分模型（已装 `RealESRGAN_x4plus.pth`） | 0.06 GB（已有） | 4x 尺寸、无接缝 | ✅ 已通过（修复 1 处 bug） |

**全部 L3 模型已就位**（WD14 + GDINO + u2net + BLIP + Qwen3B ≈ 9.9 GB；超分模型本机已有）；**剩余预算 0**。

## 画布实测（in-ComfyUI smoke）

通过真实 ComfyUI 引擎提交 API 工作流（等价于在画布上连好图点运行），脚本 `tools/verify/canvas_smoke.py`：

| 检查 | 结果 |
|---|---|
| 插件加载 | `custom_nodes\ComfyUI-CFX`（junction）0.1s 加载，无导入错误 |
| 节点注册 | `object_info` 4119 个节点类型；抽样 9 个 cfx 节点全部存在 |
| 工作流 A（primitives + IO） | LoadImage → Image Resize → Save Image(Metadata) + Text → Save Text 全部执行；产出 `cfx_smoke_00001_.png` 与内容精确匹配的 `cfx_smoke.txt` |
| 工作流 B（Florence-2 链路） | LoadImage → Florence-2 Loader/Run(tags) → Tags Filter → Save Text；产出 `1girl, solo, smile, blue eyes, blonde hair, dress, ...` |

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
| `comfyui_controlnet_normal_map_from_depth` | controlnet | ✅ | N/A | 纯张量 |
| `comfyui_inpaint_outpaint_to_ratio` | inpaint | ✅ | N/A | 纯几何 |
| `comfyui_filter_sharpen` | filter | ✅ | N/A | 纯张量 |
| `comfyui_audio_normalize` | audio | ✅ | N/A | 纯张量 |
| `comfyui_video_pad_frames` | video | ✅ | N/A | 纯张量 |
| `comfyui_loaders_safetensors_info` | loaders | ✅ | N/A | 读元数据 + 路径校验 |
| `comfyui_flux_conditioning_concat` | flux | ✅ | N/A | 纯列表 |
| `comfyui_depth3d_colormap` | depth3d | ✅ | N/A | 纯张量 + matplotlib |
| `comfyui_vision_clip_interrogator` | vision | ✅ | ✅ | CLIP + BLIP |
| `comfyui_segment_sam2_points` | segment | ✅ | ✅ | SAM2 点位 |
| `comfyui_segment_text_to_mask` | segment | ✅ | ✅ | GDINO + SAM2 |
| `comfyui_segment_mask_to_bbox` | segment | ✅ | N/A | 纯几何 |
| `comfyui_vision_blip2_caption` | vision | ✅ | ⏳ | 见上（模型清单已修正） |
| `comfyui_vision_florence2_region` | vision | ✅ | ✅ | 见上 |
| `comfyui_segment_sam2_auto_mask` | segment | ✅ | ✅ | 见上 |
| `comfyui_segment_mask_to_segs` | segment | ✅ | N/A | SEGS 结构兼容（纯数据） |
| `comfyui_segment_segs_to_mask` | segment | ✅ | N/A | SEGS 结构兼容（纯数据） |

## 收官执行清单（L3）

```bat
set COMFYUI_PATH=D:\path\to\ComfyUI
python tools\verify\florence2.py
python tools\verify\sam2.py
python tools\verify\facecrop.py
```

WD14 / BLIP / VLM / GroundingDINO / Matting 的脚本将在对应节点开发/复核时补入
`tools/verify/`（命名 `<node>.py`），并在此表把 ⏳ 改为 ✅ 或记录的失败原因。
