"""Mask operations."""

import numpy as np
import torch
import torch.nn.functional as F
from scipy import ndimage


def as_bhw(mask: torch.Tensor) -> torch.Tensor:
    m = mask.float()
    if m.dim() == 2:
        m = m.unsqueeze(0)
    if m.dim() != 3:
        raise ValueError(f"mask must be [H,W] or [B,H,W], got {tuple(mask.shape)}")
    return m


def _grow(mask: torch.Tensor, pixels: int) -> torch.Tensor:
    if pixels <= 0:
        return mask
    kernel = 2 * pixels + 1
    return F.max_pool2d(mask.unsqueeze(1), kernel_size=kernel, stride=1, padding=pixels).squeeze(1)


def _shrink(mask: torch.Tensor, pixels: int) -> torch.Tensor:
    return 1.0 - _grow(1.0 - mask, pixels)


def _blur(mask: torch.Tensor, radius: int) -> torch.Tensor:
    if radius <= 0:
        return mask
    size = 2 * radius + 1
    coords = torch.arange(size, dtype=mask.dtype, device=mask.device) - radius
    sigma = max(0.5, radius / 2.0)
    kernel = torch.exp(-(coords ** 2) / (2 * sigma * sigma))
    kernel = (kernel / kernel.sum()).view(1, 1, 1, size)
    x = F.pad(mask.unsqueeze(1), (radius, radius, radius, radius), mode="reflect")
    x = F.conv2d(x, kernel)
    x = F.conv2d(x, kernel.view(1, 1, size, 1))
    return x.squeeze(1)


def _fill_holes(mask: torch.Tensor) -> torch.Tensor:
    array = mask.detach().cpu().numpy()
    filled = np.empty_like(array)
    for index in range(array.shape[0]):
        filled[index] = ndimage.binary_fill_holes(array[index] > 0.5).astype(array.dtype)
    return torch.from_numpy(filled).to(mask.device, mask.dtype)


class CFXMaskOps:
    """One mask node: threshold, invert, fill holes, blur, grow, shrink."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
            },
            "optional": {
                "threshold": ("FLOAT", {"default": -1.0, "min": -1.0, "max": 1.0, "step": 0.01}),
                "invert": ("BOOLEAN", {"default": False}),
                "fill_holes": ("BOOLEAN", {"default": False}),
                "blur": ("INT", {"default": 0, "min": 0, "max": 256}),
                "grow": ("INT", {"default": 0, "min": 0, "max": 256}),
                "shrink": ("INT", {"default": 0, "min": 0, "max": 256}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Primitives/Mask"

    def run(self, mask, threshold=-1.0, invert=False, fill_holes=False,
            blur=0, grow=0, shrink=0):
        result = as_bhw(mask)
        if threshold >= 0:
            result = (result > threshold).to(result.dtype)
        if invert:
            result = 1.0 - result
        if fill_holes:
            result = _fill_holes(result)
        if blur > 0:
            result = _blur(result, blur)
        if grow > 0:
            result = _grow(result, grow)
        if shrink > 0:
            result = _shrink(result, shrink)
        return (result.clamp(0.0, 1.0).contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_mask_ops": CFXMaskOps,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_mask_ops": "ComfyUI-Primitives · Mask Ops",
}
