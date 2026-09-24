"""Verify GroundingDINO detection (native transformers; downloads IDEA-Research weights)."""

import os

import torch
from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.segment.nodes.detect import CFXGroundingDinoDetect

MODEL = "IDEA-Research/grounding-dino-tiny"

image, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")
detections, mask = CFXGroundingDinoDetect().run(
    tensor,
    prompt="girl. face. dress.",
    model=MODEL,
    box_threshold=0.25,
    text_threshold=0.20,
)

assert isinstance(detections, dict), f"detections must be a dict, got {type(detections).__name__}"
assert isinstance(detections.get("bboxes"), list), "detections['bboxes'] must be a list"
assert isinstance(detections.get("labels"), list), "detections['labels'] must be a list"
assert len(detections["bboxes"]) == len(detections["labels"]), "bboxes/labels length mismatch"
assert all(isinstance(label, str) for label in detections["labels"]), "labels must be strings"

assert isinstance(mask, torch.Tensor), f"mask must be a torch.Tensor, got {type(mask).__name__}"
assert mask.ndim == 3 and mask.shape[0] == 1, f"unexpected mask shape {tuple(mask.shape)}"
width, height = image.size
assert tuple(mask.shape[1:]) == (height, width), f"mask {tuple(mask.shape[1:])} != image {(height, width)}"
assert 0.0 <= float(mask.min()) and float(mask.max()) <= 1.0, "mask values must be within [0, 1]"

print("boxes:", len(detections["bboxes"]))
for box, label in zip(detections["bboxes"], detections["labels"]):
    print(f"  {label}: {[round(float(v), 1) for v in box]}")
print("labels:", detections["labels"])
print("mask shape:", tuple(mask.shape))
print("OK")
