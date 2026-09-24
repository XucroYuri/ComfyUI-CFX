"""Verify CFXUpscaleTiled (comfyui_resolve_upscale_tiled) with a real 4x upscale model."""

import os

import torch
import torchvision.transforms.functional as F
from _common import bootstrap
from PIL import Image

bootstrap()

from comfy_extras.nodes_upscale_model import UpscaleModelLoader
from utils.extra_config import load_extra_path_config

from comfyui_cfx.packages.resolve.nodes.upscale import CFXUpscaleTiled

MODEL = "RealESRGAN_x4plus.pth"
COMFY = os.environ["COMFYUI_PATH"]

# main.py loads this before ComfyUI resolves model names; the shared model dir lives here.
extra_paths = os.path.join(COMFY, "extra_model_paths.yaml")
if os.path.isfile(extra_paths):
    load_extra_path_config(extra_paths)

image = Image.open(os.path.join(COMFY, "input", "example.png")).convert("RGB")
image = F.resize(image, [256, 256])
tensor = F.to_tensor(image).unsqueeze(0).permute(0, 2, 3, 1).contiguous().float()

model = UpscaleModelLoader.execute(MODEL).result[0]
out = CFXUpscaleTiled().run(model, tensor, tile_size=128, overlap=32)[0]

h, w, c = tensor.shape[1:]
expected = (1, h * 4, w * 4, c)
assert tuple(out.shape) == expected, f"shape {tuple(out.shape)} != {expected}"
assert torch.isfinite(out).all(), "output contains NaN/Inf"
lo, hi = out.min().item(), out.max().item()
assert lo >= -1e-4 and hi <= 1.0 + 1e-4, f"output range [{lo}, {hi}] outside [0, 1]"
assert out.std().item() > 0, "output is constant"

print(
    f"model={MODEL} input={tuple(tensor.shape)} output={tuple(out.shape)} "
    f"min={lo:.4f} max={hi:.4f} std={out.std().item():.4f}"
)
print("OK")
