"""Scale an image to a target megapixel count, preserving aspect ratio."""

import comfy.utils

from ....core.types import ensure_image

UPSCALE_METHODS = ("bicubic", "bilinear", "area", "nearest-exact", "lanczos")


class CFXScaleToMegapixels:
    """Resize BHWC image so its pixel count approximates ``megapixels``."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "megapixels": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 64.0, "step": 0.01}),
                "multiple_of": ("INT", {"default": 8, "min": 1, "max": 256}),
                "upscale_method": (UPSCALE_METHODS, {"default": "bicubic"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height")
    FUNCTION = "scale"
    CATEGORY = "ComfyUI-Resolve/Scale"

    def scale(self, image, megapixels=1.0, multiple_of=8, upscale_method="bicubic"):
        img = ensure_image(image)
        in_h, in_w = img.shape[1], img.shape[2]
        factor = (megapixels * 1_000_000.0 / (in_w * in_h)) ** 0.5
        out_w = max(int(multiple_of), int(round(in_w * factor / multiple_of)) * int(multiple_of))
        out_h = max(int(multiple_of), int(round(in_h * factor / multiple_of)) * int(multiple_of))
        source = img.permute(0, 3, 1, 2)
        resized = comfy.utils.common_upscale(source, out_w, out_h, upscale_method, "disabled")
        return (resized.permute(0, 2, 3, 1).contiguous(), out_w, out_h)


NODE_CLASS_MAPPINGS = {
    "comfyui_resolve_scale_to_megapixels": CFXScaleToMegapixels,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_resolve_scale_to_megapixels": "ComfyUI-Resolve · Scale to Megapixels",
}
