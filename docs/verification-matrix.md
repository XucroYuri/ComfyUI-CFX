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
| ComfyUI-Vision | 7 | ✅ | Florence-2 ✅ | 3（WD14 / BLIP / VLM） |
| ComfyUI-Segment | 6 | ✅ | SAM2 ✅ / FaceCrop ✅ | 2（GroundingDINO / Matting） |
| **合计** | **33** | **✅** | **3 模式** | **5 节点** |

## L3 明细（需要模型的节点）

| 节点 | 需要的模型/后端 | 体积 | 期望输出 | 状态 |
|---|---|---|---|---|
| `comfyui_vision_florence2_loader` / `_run` | comfyui-florence2 + PromptGen v2.0 | 已在本地 | tags 非空；检测任务返回 dict | ✅ 已通过 |
| `comfyui_segment_sam2_loader` / `_mask` | ComfyUI-segment-anything-2 + sam2.1_hiera_tiny-fp16 | 已在本地 | MASK `(1,H,W)`、二值、非空 | ✅ 已通过 |
| `comfyui_segment_face_crop` | ComfyUI-AutoCropFaces（权重随插件 1.7MB） | 0 | 无人脸返回原图；有脸返回裁剪 | ✅ 已通过 |
| `comfyui_vision_wd14_tagger` | SmilingWolf `wd-v1-4-moat-tagger-v2` | ~0.3 GB | 非空标签串、含 general 标签 | ⏳ 待做 |
| `comfyui_vision_blip_caption` | `Salesforce/blip-image-captioning-base` | ~1 GB | 非空英文描述 | ⏳ 待做 |
| `comfyui_vision_vlm_caption` | `Qwen/Qwen2.5-VL-3B-Instruct` | ~7 GB | 非空描述 | ⏳ 待做 |
| `comfyui_segment_grounding_dino` | `IDEA-Research/grounding-dino-tiny` | ~0.7 GB | boxes + 非空 MASK | ⏳ 待做 |
| `comfyui_segment_matting` | rembg `birefnet-general`（或 `u2net`） | ~0.9 GB (u2net ~0.18) | alpha MASK + RGBA | ⏳ 待做 |

**L3 模型下载总预算：约 9.9 GB**（可用 `u2net` 把抠图降到 ~0.18 GB，总计约 9.2 GB）。

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
| `comfyui_vision_wd14_tagger` | vision | ✅ | ⏳ | 见上 |
| `comfyui_vision_blip_caption` | vision | ✅ | ⏳ | 见上 |
| `comfyui_vision_vlm_caption` | vision | ✅ | ⏳ | 见上 |
| `comfyui_vision_caption_clean` | vision | ✅ | N/A | 纯文本 |
| `comfyui_vision_tags_filter` | vision | ✅ | N/A | 纯文本 |
| `comfyui_segment_annotations_to_mask` | segment | ✅ | N/A | 纯几何 |
| `comfyui_segment_grounding_dino` | segment | ✅ | ⏳ | 见上 |
| `comfyui_segment_sam2_loader` | segment | ✅ | ✅ | 见上 |
| `comfyui_segment_sam2_mask` | segment | ✅ | ✅ | 见上 |
| `comfyui_segment_matting` | segment | ✅ | ⏳ | 见上 |
| `comfyui_segment_face_crop` | segment | ✅ | ✅ | 见上 |

## 收官执行清单（L3）

```bat
set COMFYUI_PATH=D:\path\to\ComfyUI
python tools\verify\florence2.py
python tools\verify\sam2.py
python tools\verify\facecrop.py
```

WD14 / BLIP / VLM / GroundingDINO / Matting 的脚本将在对应节点开发/复核时补入
`tools/verify/`（命名 `<node>.py`），并在此表把 ⏳ 改为 ✅ 或记录的失败原因。
