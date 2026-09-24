"""Verify SAM2 point-prompt segmentation (needs ComfyUI-segment-anything-2 + a checkpoint)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.segment.nodes.sam2 import CFXSAM2Loader
from comfyui_cfx.packages.segment.nodes.sam2_points import CFXSam2Points

handle = CFXSAM2Loader().load("sam2.1_hiera_tiny.safetensors", "single_image", "fp16")[0]
image, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")
width, height = image.size

positive = f"[[{int(width * 0.5)}, {int(height * 0.62)}]]"
negative = f"[[{int(width * 0.05)}, {int(height * 0.05)}]]"
mask = CFXSam2Points().run(handle, tensor, positive, negative_points=negative)[0]
assert mask.ndim == 3 and mask.shape[0] == 1, f"unexpected mask shape {tuple(mask.shape)}"
assert float(mask.max()) > 0.0, "mask is empty"
print("mask shape:", tuple(mask.shape), "coverage: %.3f" % float(mask.mean()))
print("OK")
