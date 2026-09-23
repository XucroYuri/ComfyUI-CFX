"""Annotation -> mask node."""

import torch

from ....core.types import ensure_image
from ..geometry import annotations_to_mask


class CFXAnnotationsToMask:
    """Rasterize Florence-2 style boxes or polygons into a MASK."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "annotations": ("JSON",),
            },
            "optional": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 1024, "min": 1, "max": 16384}),
                "height": ("INT", {"default": 1024, "min": 1, "max": 16384}),
                "line_width": ("INT", {"default": 0, "min": 0, "max": 256}),
                "invert": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/Geometry"

    def run(self, annotations, image=None, width=1024, height=1024, line_width=0, invert=False):
        if image is not None:
            _, height, width, _ = ensure_image(image).shape
        mask = annotations_to_mask(annotations, height, width, line_width)
        if invert:
            mask = 1.0 - mask
        return (torch.from_numpy(mask)[None, ...].contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_annotations_to_mask": CFXAnnotationsToMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_annotations_to_mask": "ComfyUI-Segment · Annotations to Mask",
}
