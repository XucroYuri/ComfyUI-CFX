"""Verify SAM2 loader + box-prompted mask (needs ComfyUI-segment-anything-2 + weights)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.segment.nodes.sam2 import CFXSAM2Loader, CFXSAM2Mask

handle = CFXSAM2Loader().load("sam2.1_hiera_tiny.safetensors", "single_image", "fp16")[0]
print("segmentor:", handle["segmentor"], "version:", handle["version"])

image, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")
width, height = image.size
box = [width * 0.2, height * 0.1, width * 0.8, height * 0.95]

mask = CFXSAM2Mask().run(handle, tensor, {"bboxes": [box], "labels": ["subject"]})[0]
assert mask.ndim == 3 and mask.shape[0] == 1, f"unexpected mask shape {tuple(mask.shape)}"
assert float(mask.max()) > 0.0, "mask is empty"
print("mask shape:", tuple(mask.shape), "coverage: %.3f" % float(mask.mean()))
print("OK")
