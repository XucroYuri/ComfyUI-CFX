"""Verify SAM2 automatic mask generation (needs a SAM2 checkpoint loaded with segmentor=automaskgenerator)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.segment.nodes.sam2 import CFXSAM2Loader
from comfyui_cfx.packages.segment.nodes.sam2_auto import CFXSam2AutoMask

handle = CFXSAM2Loader().load("sam2.1_hiera_tiny.safetensors", "automaskgenerator", "fp16")[0]
_, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")

mask, bboxes = CFXSam2AutoMask().run(handle, tensor, points_per_side=8)
print("mask shape:", tuple(mask.shape), "mask count:", mask.shape[0], "bboxes:", len(bboxes))
assert mask.ndim == 3 and mask.shape[0] >= 1, f"unexpected mask shape {tuple(mask.shape)}"
assert float(mask.max()) > 0.0, "auto mask is empty"
print("OK")
