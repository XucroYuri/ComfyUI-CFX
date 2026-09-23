"""Crop image and mask to the mask bounding box."""

import torch

from ....core.types import ensure_image


class CFXCropByMask:
    """Crop image/mask to the mask bbox, padded and aligned to a multiple."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "padding": ("INT", {"default": 32, "min": 0, "max": 4096}),
                "multiple_of": ("INT", {"default": 8, "min": 1, "max": 256}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "JSON")
    RETURN_NAMES = ("image", "mask", "crop_data")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Inpaint/Crop"

    def run(self, image, mask, padding=32, multiple_of=8):
        img = ensure_image(image)
        _, height, width, _ = img.shape

        m = mask.float()
        if m.dim() == 3:
            m = m[0]
        elif m.dim() != 2:
            raise ValueError(f"crop_by_mask: mask must be 2D or 3D, got shape {tuple(mask.shape)}")

        rows = torch.any(m > 0.5, dim=1)
        cols = torch.any(m > 0.5, dim=0)
        if not bool(rows.any()):
            raise ValueError("crop_by_mask: mask is empty")

        ys = torch.nonzero(rows, as_tuple=False).flatten()
        xs = torch.nonzero(cols, as_tuple=False).flatten()
        x0 = int(xs[0].item()) - padding
        y0 = int(ys[0].item()) - padding
        x1 = int(xs[-1].item()) + 1 + padding
        y1 = int(ys[-1].item()) + 1 + padding

        x0 = (x0 // multiple_of) * multiple_of
        y0 = (y0 // multiple_of) * multiple_of
        x1 = -(-x1 // multiple_of) * multiple_of
        y1 = -(-y1 // multiple_of) * multiple_of

        x0 = max(0, min(x0, width - 1))
        y0 = max(0, min(y0, height - 1))
        x1 = max(x0 + 1, min(x1, width))
        y1 = max(y0 + 1, min(y1, height))

        crop_data = {
            "x": x0,
            "y": y0,
            "width": x1 - x0,
            "height": y1 - y0,
            "original_width": width,
            "original_height": height,
        }
        cropped_image = img[:1, y0:y1, x0:x1, :].contiguous()
        cropped_mask = m[y0:y1, x0:x1].unsqueeze(0).contiguous()
        return (cropped_image, cropped_mask, crop_data)


NODE_CLASS_MAPPINGS = {
    "comfyui_inpaint_crop_by_mask": CFXCropByMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_inpaint_crop_by_mask": "ComfyUI-Inpaint · Crop by Mask",
}
