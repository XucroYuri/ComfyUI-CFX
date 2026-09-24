"""Thresholded unsharp-mask sharpen filter."""

import torch

from ....core.types import ensure_image
from .high_pass import _blur


class CFXSharpen:
    """Sharpen an image with a thresholded unsharp mask."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "radius": ("INT", {"default": 2, "min": 1, "max": 64}),
                "amount": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01}),
                "threshold": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Filter/Image"

    def run(self, image, radius=2, amount=1.0, threshold=0.0):
        img = ensure_image(image)
        b, h, w, c = img.shape
        x = img.permute(0, 3, 1, 2).reshape(b * c, 1, h, w)
        blur = _blur(x, int(radius)).reshape(b, c, h, w).permute(0, 2, 3, 1)
        diff = img - blur
        diff = torch.where(diff.abs() <= threshold, torch.zeros_like(diff), diff)
        return (torch.clamp(img + diff * amount, 0.0, 1.0).contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_filter_sharpen": CFXSharpen,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_filter_sharpen": "ComfyUI-Filter · Sharpen",
}
