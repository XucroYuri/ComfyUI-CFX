"""Outpaint by padding the canvas; the new border is marked as the outpaint region."""

import torch

from ....core.types import ensure_image


class CFXOutpaintCanvas:
    """Expand image/mask onto a larger fill-colored canvas."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "left": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "right": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "top": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "bottom": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "fill": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Inpaint/Crop"

    def run(self, image, mask, left=0, right=0, top=0, bottom=0, fill=0.0):
        img = ensure_image(image)

        m = mask.float()
        if m.dim() == 3:
            m = m[0]
        elif m.dim() != 2:
            raise ValueError(f"outpaint: mask must be 2D or 3D, got shape {tuple(mask.shape)}")
        m = m.clamp(0.0, 1.0).unsqueeze(0)

        if (left, right, top, bottom) == (0, 0, 0, 0):
            return (img, m)

        batch, height, width, channels = img.shape
        if m.shape[-2:] != (height, width):
            raise ValueError(f"outpaint: mask {tuple(m.shape[-2:])} does not match image {height}x{width}")

        new_h = height + top + bottom
        new_w = width + left + right

        canvas = torch.full(
            (batch, new_h, new_w, channels),
            float(fill),
            dtype=img.dtype,
            device=img.device,
        )
        canvas[:, top:top + height, left:left + width, :] = img

        out_mask = torch.ones((1, new_h, new_w), dtype=m.dtype, device=m.device)
        out_mask[:, top:top + height, left:left + width] = m
        return (canvas, out_mask)


NODE_CLASS_MAPPINGS = {
    "comfyui_inpaint_outpaint_canvas": CFXOutpaintCanvas,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_inpaint_outpaint_canvas": "ComfyUI-Inpaint · Outpaint Canvas",
}
