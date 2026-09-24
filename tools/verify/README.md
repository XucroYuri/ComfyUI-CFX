# Verification scripts

Reproducible end-to-end checks for the nodes that need real models. Run them from a
ComfyUI environment that has the required custom nodes installed.

```bat
set COMFYUI_PATH=D:\path\to\ComfyUI
python tools\verify\florence2.py
python tools\verify\wd14.py
python tools\verify\blip.py
python tools\verify\vlm.py
python tools\verify\grounding_dino.py
python tools\verify\matting.py
python tools\verify\sam2.py
python tools\verify\sam2_points.py
python tools\verify\text_to_mask.py
python tools\verify\vision_clip_interrogator.py
python tools\verify\facecrop.py
python tools\verify\resolve_upscale.py
```

| Script | Node(s) | Requires |
|---|---|---|
| `florence2.py` | `comfyui_vision_florence2_loader` / `_run` | `comfyui-florence2` + Florence-2 weights |
| `wd14.py` | `comfyui_vision_wd14_tagger` | auto-downloads `wd-v1-4-moat-tagger-v2` (~0.3 GB) |
| `grounding_dino.py` | `comfyui_segment_grounding_dino` | auto-downloads `grounding-dino-tiny` (~0.66 GB) |
| `matting.py` | `comfyui_segment_matting` | auto-downloads rembg `u2net` (~0.18 GB) |
| `sam2.py` | `comfyui_segment_sam2_loader` / `_mask` | `ComfyUI-segment-anything-2` + a SAM2 checkpoint |
| `sam2_points.py` | `comfyui_segment_sam2_points` | same as `sam2.py` |
| `text_to_mask.py` | `comfyui_segment_text_to_mask` | GroundingDINO + SAM2 (auto-downloads the tiny detector) |
| `vision_clip_interrogator.py` | `comfyui_vision_clip_interrogator` | downloads CLIP ViT-L-14/openai + BLIP |
| `facecrop.py` | `comfyui_segment_face_crop` | `ComfyUI-AutoCropFaces` (weights bundled) |
| `blip.py` | `comfyui_vision_blip_caption` | auto-downloads `blip-image-captioning-base` (~1 GB) |
| `vlm.py` | `comfyui_vision_vlm_caption` | auto-downloads `Qwen2.5-VL-3B-Instruct` (~7 GB) |
| `resolve_upscale.py` | `comfyui_resolve_upscale_tiled` | an upscale model in `models/upscale_models` |

Each script prints the observed result and exits non-zero on assertion failure.

**Do not** force CPU with an empty `CUDA_VISIBLE_DEVICES=` — on this ComfyUI/torch build it
makes `comfy_kitchen`'s device probe raise during ComfyUI import, before any node runs.
Leave the GPU visible (onnxruntime here is CPU-only anyway) or use ComfyUI's `--cpu`.

See `docs/verification-matrix.md` for the full node-by-node verification ledger.
