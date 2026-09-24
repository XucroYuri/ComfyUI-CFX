"""Verify text -> mask (GroundingDINO + SAM2) end to end."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.segment.nodes.sam2 import CFXSAM2Loader
from comfyui_cfx.packages.segment.nodes.text_to_mask import CFXTextToMask

handle = CFXSAM2Loader().load("sam2.1_hiera_tiny.safetensors", "single_image", "fp16")[0]
_, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")

mask, detections = CFXTextToMask().run(
    tensor, "girl. dress.", "IDEA-Research/grounding-dino-tiny",
    box_threshold=0.25, text_threshold=0.20, sam2=handle,
)
print("boxes:", len(detections.get("bboxes", [])), "labels:", detections.get("labels"))
assert mask.ndim == 3 and mask.shape[0] == 1, f"unexpected mask shape {tuple(mask.shape)}"
assert detections.get("bboxes"), "no detections; try a different prompt"
print("mask shape:", tuple(mask.shape), "coverage: %.3f" % float(mask.mean()))
print("OK")
