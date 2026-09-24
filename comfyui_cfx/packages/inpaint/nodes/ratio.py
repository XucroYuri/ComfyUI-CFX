"""Outpaint to a target aspect ratio by extending only the shorter dimension."""

import torch

from ....core.types import ensure_image

_RATIOS = {
    "1:1": (1, 1),
    "4:3": (4, 3),
    "3:2": (3, 2),
    "16:9": (16, 9),
    "9:16": (9, 16),
    "2:3": (2, 3),
    "3:4": (3, 4),
}

_ANCHORS = ("center", "start", "end")


class CFXOutpaintToRatio:
    """Extend the canvas to a target ratio, marking the new border as outpaint."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "ratio": (list(_RATIOS), {"default": "16:9"}),
                "anchor": (list(_ANCHORS), {"default": "center"}),
                "fill": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Inpaint/Crop"

    def run(self, image, mask, ratio="16:9", anchor="center", fill=0.0):
        img = ensure_image(image)

        m = mask.float()
        if m.dim() == 3:
            m = m[0]
        elif m.dim() != 2:
            raise ValueError(f"outpaint_to_ratio: mask must be 2D or 3D, got shape {tuple(mask.shape)}")
        m = m.clamp(0.0, 1.0).unsqueeze(0)

        if ratio not in _RATIOS:
            raise ValueError(f"outpaint_to_ratio: unknown ratio {ratio!r}")
        if anchor not in _ANCHORS:
            raise ValueError(f"outpaint_to_ratio: unknown anchor {anchor!r}")

        batch, height, width, channels = img.shape
        target_w, target_h = _RATIOS[ratio]

        if width * target_h == height * target_w:
            return (img, m)

        if m.shape[-2:] != (height, width):
            raise ValueError(f"outpaint_to_ratio: mask {tuple(m.shape[-2:])} does not match image {height}x{width}")

        if width * target_h < height * target_w:
            new_h = height
            new_w = round(height * target_w / target_h)
        else:
            new_w = width
            new_h = round(width * target_h / target_w)

        if anchor == "start":
            offset_x = 0
            offset_y = 0
        elif anchor == "end":
            offset_x = new_w - width
            offset_y = new_h - height
        else:
            offset_x = (new_w - width) // 2
            offset_y = (new_h - height) // 2

        canvas = torch.full(
            (batch, new_h, new_w, channels),
            float(fill),
            dtype=img.dtype,
            device=img.device,
        )
        canvas[:, offset_y:offset_y + height, offset_x:offset_x + width, :] = img

        out_mask = torch.ones((1, new_h, new_w), dtype=m.dtype, device=m.device)
        out_mask[:, offset_y:offset_y + height, offset_x:offset_x + width] = m
        return (canvas, out_mask)


NODE_CLASS_MAPPINGS = {
    "comfyui_inpaint_outpaint_to_ratio": CFXOutpaintToRatio,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_inpaint_outpaint_to_ratio": "ComfyUI-Inpaint · Outpaint to Ratio",
}
