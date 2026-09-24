"""Normalize a depth map to [0, 1] per batch item, optionally inverting it."""

import torch

from ....core.types import ensure_image


class CFXNormalizeDepth:
    """Rescale a single-channel depth estimate and expose it as IMAGE + MASK."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mode": (["minmax", "clamp"], {"default": "minmax"}),
                "invert": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Depth3D/Process"

    def run(self, image, mode="minmax", invert=False):
        img = ensure_image(image)
        d = img.mean(dim=-1)

        if mode == "minmax":
            dmin = d.amin(dim=(1, 2), keepdim=True)
            dmax = d.amax(dim=(1, 2), keepdim=True)
            span = dmax - dmin
            scaled = (d - dmin) / span.clamp_min(torch.finfo(d.dtype).eps)
            d = torch.where(span > 0, scaled, torch.zeros_like(d))
        else:
            d = d.clamp(0.0, 1.0)

        if invert:
            d = 1.0 - d

        out_image = d.unsqueeze(-1).repeat(1, 1, 1, 3).contiguous()
        return (out_image, d.contiguous())


NODE_CLASS_MAPPINGS = {
    "comfyui_depth3d_normalize_depth": CFXNormalizeDepth,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_depth3d_normalize_depth": "ComfyUI-Depth3D · Normalize Depth",
}
