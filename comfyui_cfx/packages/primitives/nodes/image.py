"""Image geometry primitives.

Template node for the SPEC -> IMPL -> REVIEW -> VERIFY pipeline.
"""

import comfy.utils
import torch

from ....core.types import ensure_image

UPSCALE_METHODS = ("bicubic", "bilinear", "area", "nearest-exact", "lanczos")
CROP_POSITIONS = ("center", "top", "bottom", "left", "right")


def _align(value: float, multiple_of: int) -> int:
    return max(int(multiple_of), int(round(value / multiple_of)) * int(multiple_of))


def target_size(width, height, out_width, out_height, scale_by, target_megapixels, multiple_of):
    """Resolve the output size, then snap it to ``multiple_of``."""
    if scale_by > 0:
        w, h = width * scale_by, height * scale_by
    elif target_megapixels > 0:
        scale = (target_megapixels * 1_000_000.0 / (width * height)) ** 0.5
        w, h = width * scale, height * scale
    elif out_width > 0 and out_height > 0:
        w, h = out_width, out_height
    elif out_width > 0:
        w, h = out_width, height * out_width / width
    elif out_height > 0:
        w, h = width * out_height / height, out_height
    else:
        raise ValueError("image resize needs one of scale_by, target_megapixels, width or height")
    return _align(w, multiple_of), _align(h, multiple_of)


def aspect_crop(samples: torch.Tensor, out_width: int, out_height: int, position: str) -> torch.Tensor:
    """Crop BCHW ``samples`` to the target aspect ratio, anchored at ``position``."""
    in_h, in_w = samples.shape[-2], samples.shape[-1]
    target = out_width / out_height
    if in_w / in_h > target:
        new_w, new_h = max(1, int(round(in_h * target))), in_h
    else:
        new_w, new_h = in_w, max(1, int(round(in_w / target)))

    if position == "left":
        x0 = 0
    elif position == "right":
        x0 = in_w - new_w
    else:
        x0 = (in_w - new_w) // 2

    if position == "top":
        y0 = 0
    elif position == "bottom":
        y0 = in_h - new_h
    else:
        y0 = (in_h - new_h) // 2

    return samples[:, :, y0:y0 + new_h, x0:x0 + new_w]


class CFXImageResize:
    """Single resize node: stretch / crop / pad, from size, scale or megapixels."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mode": (["stretch", "crop", "pad"], {"default": "stretch"}),
            },
            "optional": {
                "width": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "height": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "scale_by": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 16.0, "step": 0.01}),
                "target_megapixels": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 256.0, "step": 0.01}),
                "multiple_of": ("INT", {"default": 8, "min": 1, "max": 256}),
                "upscale_method": (UPSCALE_METHODS, {"default": "bicubic"}),
                "crop_position": (CROP_POSITIONS, {"default": "center"}),
                "pad_color": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height")
    FUNCTION = "resize"
    CATEGORY = "ComfyUI-Primitives/Image"

    def resize(self, image, mode, width=0, height=0, scale_by=0.0, target_megapixels=0.0,
               multiple_of=8, upscale_method="bicubic", crop_position="center", pad_color=0.0):
        img = ensure_image(image)
        batch, in_h, in_w, channels = img.shape
        out_w, out_h = target_size(in_w, in_h, width, height, scale_by, target_megapixels, multiple_of)
        source = img.permute(0, 3, 1, 2)

        if mode == "pad":
            scale = min(out_w / in_w, out_h / in_h)
            inner_w = max(1, int(round(in_w * scale)))
            inner_h = max(1, int(round(in_h * scale)))
            resized = comfy.utils.common_upscale(source, inner_w, inner_h, upscale_method, "disabled")
            canvas = torch.full((batch, channels, out_h, out_w), pad_color, dtype=resized.dtype, device=resized.device)
            x0 = (out_w - inner_w) // 2
            y0 = (out_h - inner_h) // 2
            canvas[:, :, y0:y0 + inner_h, x0:x0 + inner_w] = resized
        elif mode == "crop":
            cropped = aspect_crop(source, out_w, out_h, crop_position)
            canvas = comfy.utils.common_upscale(cropped, out_w, out_h, upscale_method, "disabled")
        else:
            canvas = comfy.utils.common_upscale(source, out_w, out_h, upscale_method, "disabled")

        return (canvas.permute(0, 2, 3, 1).contiguous(), out_w, out_h)


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_image_resize": CFXImageResize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_image_resize": "ComfyUI-Primitives · Image Resize",
}
