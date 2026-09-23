"""Constrain an image to a maximum size (behaviour reimplementation of ConstrainImage|pysssss)."""

import comfy.utils

from ....core.types import ensure_image


class CFXConstrainImage:
    """Fit an image inside a maximum box, optionally cropping to cover it exactly."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "max_width": ("INT", {"default": 1024, "min": 1, "max": 16384}),
                "max_height": ("INT", {"default": 1024, "min": 1, "max": 16384}),
                "crop_if_required": ("BOOLEAN", {"default": False}),
                "upscale_method": (["bicubic", "bilinear", "area", "nearest-exact", "lanczos"], {"default": "bicubic"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Flow/Image"

    def run(self, image, max_width, max_height, crop_if_required=False, upscale_method="bicubic"):
        img = ensure_image(image)
        _, height, width, _ = img.shape
        source = img.permute(0, 3, 1, 2)

        if crop_if_required:
            scale = max(max_width / width, max_height / height)
            scaled_w = max(1, int(round(width * scale)))
            scaled_h = max(1, int(round(height * scale)))
            resized = comfy.utils.common_upscale(source, scaled_w, scaled_h, upscale_method, "disabled")
            x0 = (scaled_w - max_width) // 2
            y0 = (scaled_h - max_height) // 2
            out = resized[:, :, y0:y0 + max_height, x0:x0 + max_width]
            out_w, out_h = max_width, max_height
        else:
            scale = min(1.0, max_width / width, max_height / height)
            out_w = max(1, int(round(width * scale)))
            out_h = max(1, int(round(height * scale)))
            if (out_w, out_h) == (width, height):
                out = source
            else:
                out = comfy.utils.common_upscale(source, out_w, out_h, upscale_method, "disabled")

        return (out.permute(0, 2, 3, 1).contiguous(), out_w, out_h)


NODE_CLASS_MAPPINGS = {
    "comfyui_flow_constrain_image": CFXConstrainImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_flow_constrain_image": "ComfyUI-Flow · Constrain Image",
}
