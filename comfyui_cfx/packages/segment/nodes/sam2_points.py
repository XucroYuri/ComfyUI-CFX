"""SAM2 point-prompted segmentation (positive / negative clicks)."""

import json

from .. import backend
from .sam2 import SAM2_TYPE


def parse_points(text) -> list:
    """Normalize point text to ``[{"x": float, "y": float}, ...]``.

    Accepts a JSON list of ``[x, y]`` pairs or of ``{"x": x, "y": y}`` dicts.
    Empty/whitespace input yields ``[]``; anything else raises ``ValueError``.
    """
    if not text or not text.strip():
        return []
    try:
        data = json.loads(text)
        if not isinstance(data, list):
            raise TypeError
        return [
            {"x": float(point["x"]), "y": float(point["y"])} if isinstance(point, dict)
            else {"x": float(point[0]), "y": float(point[1])}
            for point in data
        ]
    except (KeyError, IndexError, TypeError, ValueError):
        raise ValueError(f"points must be [[x, y], ...] or [{{'x': x, 'y': y}}, ...]: {text!r}") from None


class CFXSam2Points:
    """Segment from click points (positive and optional negative) into a mask."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sam2": (SAM2_TYPE,),
                "image": ("IMAGE",),
                "positive_points": ("STRING", {"default": "[[128, 128]]"}),
            },
            "optional": {
                "negative_points": ("STRING", {"default": ""}),
                "keep_model_loaded": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/SAM2"

    def run(self, sam2, image, positive_points, negative_points="", keep_model_loaded=False):
        positive = parse_points(positive_points)
        if not positive:
            raise ValueError("positive_points must contain at least one point")
        negative = parse_points(negative_points)
        (mask,) = backend.segment_points(
            sam2,
            image,
            json.dumps(positive),
            negative=json.dumps(negative) if negative else None,
            keep_model_loaded=keep_model_loaded,
        )
        return (mask,)


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_sam2_points": CFXSam2Points,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_sam2_points": "ComfyUI-Segment · SAM2 Points",
}
