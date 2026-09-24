"""High-pass (unsharp) filter built on a separable Gaussian blur."""

import torch
import torch.nn.functional as F

from ....core.types import ensure_image


def _blur(x: torch.Tensor, radius: int) -> torch.Tensor:
    size = 2 * radius + 1
    coords = torch.arange(size, dtype=x.dtype, device=x.device) - radius
    sigma = max(0.5, radius / 2.0)
    kernel = torch.exp(-(coords ** 2) / (2 * sigma * sigma))
    kernel = (kernel / kernel.sum()).view(1, 1, 1, size)
    x = F.pad(x, (radius, radius, radius, radius), mode="reflect")
    x = F.conv2d(x, kernel)
    x = F.conv2d(x, kernel.view(1, 1, size, 1))
    return x


class CFXHighPass:
    """Add a scaled high-pass band to sharpen an image."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "radius": ("INT", {"default": 4, "min": 1, "max": 256}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Filter/Image"

    def run(self, image, radius=4, strength=1.0):
        img = ensure_image(image)
        b, h, w, c = img.shape
        x = img.permute(0, 3, 1, 2).reshape(b * c, 1, h, w)
        blur = _blur(x, int(radius)).reshape(b, c, h, w).permute(0, 2, 3, 1)
        high = img - blur
        return (torch.clamp(img + high * strength, 0.0, 1.0).contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_filter_high_pass": CFXHighPass,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_filter_high_pass": "ComfyUI-Filter · High Pass",
}
