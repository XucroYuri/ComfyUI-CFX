"""Text -> mask: GroundingDINO detection fused with SAM2 (classic full chain)."""

import torch

from ....core.types import ensure_image
from ..backend import segment
from ..geometry import annotations_to_box_batch, boxes_to_mask
from .detect import DETECT_MODELS, CFXGroundingDinoDetect


class CFXTextToMask:
    """Detect boxes from a text prompt, then segment them into a MASK."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"default": "person. dog."}),
                "detect_model": (list(DETECT_MODELS), {"default": DETECT_MODELS[0]}),
                "box_threshold": ("FLOAT", {"default": 0.30, "min": 0.0, "max": 1.0, "step": 0.01}),
                "text_threshold": ("FLOAT", {"default": 0.25, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "sam2": ("CFX_SAM2",),
                "keep_model_loaded": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("MASK", "JSON")
    RETURN_NAMES = ("mask", "detections")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/Detect"

    def run(self, image, prompt, detect_model, box_threshold=0.30, text_threshold=0.25,
            sam2=None, keep_model_loaded=False):
        detections = CFXGroundingDinoDetect().run(
            image, prompt, detect_model, box_threshold, text_threshold
        )[0]
        boxes = detections.get("bboxes", [])

        if not boxes:
            height, width = ensure_image(image).shape[1:3]
            mask = torch.zeros((1, height, width), dtype=torch.float32)
        elif sam2 is not None:
            (mask,) = segment(
                sam2, image, bboxes=annotations_to_box_batch(detections), keep_model_loaded=keep_model_loaded
            )
        else:
            height, width = ensure_image(image).shape[1:3]
            mask = torch.from_numpy(boxes_to_mask(boxes, height, width))[None, ...].contiguous()

        return (mask, detections)


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_text_to_mask": CFXTextToMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_text_to_mask": "ComfyUI-Segment · Text to Mask",
}
