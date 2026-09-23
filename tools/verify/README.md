# Verification scripts

Reproducible end-to-end checks for the nodes that need real models. Run them from a
ComfyUI environment that has the required custom nodes installed.

```bat
set COMFYUI_PATH=D:\path\to\ComfyUI
python tools\verify\florence2.py
python tools\verify\sam2.py
python tools\verify\facecrop.py
```

| Script | Node(s) | Requires |
|---|---|---|
| `florence2.py` | `comfyui_vision_florence2_loader` / `_run` | `comfyui-florence2` + Florence-2 weights |
| `sam2.py` | `comfyui_segment_sam2_loader` / `_mask` | `ComfyUI-segment-anything-2` + a SAM2 checkpoint |
| `facecrop.py` | `comfyui_segment_face_crop` | `ComfyUI-AutoCropFaces` (weights bundled) |

Each script prints the observed result and exits non-zero on assertion failure.
See `docs/verification-matrix.md` for the full node-by-node verification ledger.
