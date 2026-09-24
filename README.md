# ComfyUI-CFX

Consolidated ComfyUI custom-node suite. One monorepo, **14 domain packages**, a single type
lattice, SPEC-driven development, MIT.

Replaces a pile of overlapping plugins with one dependency-clean suite: every node has a
contract (`specs/<id>.md`), an adversarial review (`specs/<id>.review.md`), unit tests, and an
append-only development record (`DEVLOG.md`).

## Status

| Metric | Value |
|---|---|
| Packages | 14 |
| Nodes | 56 |
| Unit tests | 347 passing |
| Real end-to-end verified | 9 nodes (models: Florence-2, WD14, BLIP, Qwen2.5-VL, GroundingDINO, rembg, SAM2, RetinaFace, RealESRGAN) |
| License | MIT (`packages/**` enforced MIT by `tools/license_gate.py`) |

See `docs/verification-matrix.md` for the node-by-node verification ledger.

## Packages

| Package | Nodes | Notes |
|---|---|---|
| `ComfyUI-Primitives` | 14 | text / number / logic / image / mask / resolution / seed / save |
| `ComfyUI-Flow` | 6 | string function, show text, constrain image, repeater, load/save text |
| `ComfyUI-Vision` | 7 | Florence-2 load/run, WD14 tagger, BLIP, Qwen2.5/3-VL, caption clean, tags filter |
| `ComfyUI-Segment` | 6 | annotations→mask, GroundingDINO, SAM2 load/mask, matting, face crop |
| `ComfyUI-Inpaint` | 4 | crop-by-mask, stitch, outpaint canvas, outpaint to ratio |
| `ComfyUI-ControlNet` | 3 | canny, lineart, normal-from-depth |
| `ComfyUI-Resolve` | 2 | scale to megapixels, tiled model upscale |
| `ComfyUI-Depth3D` | 2 | normalize depth, colormap |
| `ComfyUI-Sampling` | 2 | split sigmas, sigma shift |
| `ComfyUI-Video` | 2 | frame range, pad frames |
| `ComfyUI-Flux` | 2 | conditioning blend, conditioning concat |
| `ComfyUI-Audio` | 2 | trim silence, normalize |
| `ComfyUI-Loaders` | 2 | GGUF header, safetensors info |
| `ComfyUI-Filter` | 2 | high pass, sharpen |

## Install

```bat
git clone https://github.com/XucroYuri/ComfyUI-CFX ComfyUI\custom_nodes\ComfyUI-CFX
pip install -r ComfyUI\custom_nodes\ComfyUI-CFX\requirements.txt
```

Or, to keep the repo outside `custom_nodes`, create a directory junction:

```bat
mklink /J "ComfyUI\custom_nodes\ComfyUI-CFX" "D:\path\to\ComfyUI-CFX"
```

Runtime dependency: `rembg` (used by `ComfyUI-Segment · Matting`).

### Optional backends (only if you use those nodes)

| Package | Needs |
|---|---|
| `ComfyUI-Vision` | [`comfyui-florence2`](https://github.com/kijai/ComfyUI-Florence2) for Florence-2 (path overridable with `CFX_FLORENCE2_DIR`) |
| `ComfyUI-Segment` | `ComfyUI-segment-anything-2` for SAM2 (`CFX_SAM2_DIR`), `ComfyUI-AutoCropFaces` for face crop (`CFX_FACECROP_DIR`) |
| `ComfyUI-Resolve` | any upscale model in `models/upscale_models` |

Model weights download on first use to the standard ComfyUI / HuggingFace cache locations.

## Conventions

- Node ids: `comfyui_<domain>_<verb>_<noun>`; display names `ComfyUI-<Domain> · <Name>`; categories `ComfyUI-<Domain>/<Sub>`.
- Types: the `core.types` lattice — `IMAGE` BHWC float32, `MASK` BHW, `LATENT` dict, real `BOOLEAN`.
- No `transformers` remote code. GPL-licensed plugins are **never copied**; they may only be
  used as behaviour references (see `AGENTS.md`).

## Develop

```bat
pip install -r requirements-dev.txt
pytest
python tools\spec_lint.py       # every node needs a spec + a review with verdict: PASS
python tools\license_gate.py    # packages/** must stay MIT
ruff check .
```

## Verify against real models

```bat
set COMFYUI_PATH=D:\path\to\ComfyUI
python tools\verify\florence2.py
python tools\verify\wd14.py
python tools\verify\blip.py
python tools\verify\vlm.py
python tools\verify\grounding_dino.py
python tools\verify\matting.py
python tools\verify\sam2.py
python tools\verify\facecrop.py
python tools\verify\resolve_upscale.py
python tools\verify\canvas_smoke.py   # requires a running ComfyUI on --port
```

## Migrate existing workflows

```bat
python tools\migrate.py my_workflow.json -o migrated.json
```

## License

MIT. See `LICENSE`. Third-party backends keep their own licenses (Apache-2.0 for SAM2 /
controlnet_aux, MIT for comfyui-florence2 / AutoCropFaces / rgthree).
