"""Florence-2 region refinement node (describe / categorize / OCR a box)."""

import re

from ....core.types import ensure_image
from .florence2 import FLORENCE2_TYPE, run_florence2

TASKS = {
    "region_to_description": "<REGION_TO_DESCRIPTION>",
    "region_to_category": "<REGION_TO_CATEGORY>",
    "region_to_ocr": "<REGION_TO_OCR>",
}

_LOC_TOKEN = re.compile(r"<loc_\d+>")


def strip_loc_tokens(text: str) -> str:
    """Drop echoed ``<loc_N>`` tokens; Florence-2 sometimes repeats them in its answer."""
    return _LOC_TOKEN.sub("", text).strip().strip(",").strip()


def quantize(value, size, bins=1000) -> int:
    """Map a pixel coordinate onto Florence-2's ``bins``-wide location grid."""
    if size <= 0:
        return 0
    return min(bins - 1, max(0, round(value / size * bins)))


def loc_string(x0, y0, x1, y1, width, height, bins=1000) -> str:
    """Encode a pixel box as four quantized ``<loc_N>`` tokens."""
    return (
        f"<loc_{quantize(x0, width, bins)}>"
        f"<loc_{quantize(y0, height, bins)}>"
        f"<loc_{quantize(x1, width, bins)}>"
        f"<loc_{quantize(y1, height, bins)}>"
    )


class CFXFlorence2Region:
    """Describe / categorize / OCR a specific box of an image with Florence-2."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "florence2": (FLORENCE2_TYPE,),
                "image": ("IMAGE",),
                "x0": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "y0": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "x1": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "y1": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "task": (list(TASKS), {"default": "region_to_description"}),
            },
            "optional": {
                "max_new_tokens": ("INT", {"default": 256, "min": 1, "max": 4096}),
                "num_beams": ("INT", {"default": 3, "min": 1, "max": 64}),
                "do_sample": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING", "JSON")
    RETURN_NAMES = ("text", "parsed")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Vision/Florence2"

    def run(self, florence2, image, x0=0, y0=0, x1=0, y1=0, task="region_to_description",
            max_new_tokens=256, num_beams=3, do_sample=False):
        token = TASKS.get(task)
        if token is None:
            raise ValueError(f"unknown Florence-2 region task {task!r}")

        frame = ensure_image(image)
        height, width = frame.shape[1], frame.shape[2]

        if x0 == 0 and y0 == 0 and x1 == 0 and y1 == 0:
            x0, y0, x1, y1 = 0, 0, width, height
        elif not (x1 > x0 and y1 > y0):
            raise ValueError(f"invalid region box ({x0}, {y0}, {x1}, {y1}); need x1 > x0 and y1 > y0")

        x0, x1 = min(max(x0, 0), width), min(max(x1, 0), width)
        y0, y1 = min(max(y0, 0), height), min(max(y1, 0), height)

        prompt = token + loc_string(x0, y0, x1, y1, width, height)
        text, parsed = run_florence2(florence2, image, prompt, token, max_new_tokens, num_beams, do_sample)
        if isinstance(parsed, str):
            parsed = strip_loc_tokens(parsed)
        return (strip_loc_tokens(text), parsed)


NODE_CLASS_MAPPINGS = {
    "comfyui_vision_florence2_region": CFXFlorence2Region,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_vision_florence2_region": "ComfyUI-Vision · Florence-2 Region",
}
