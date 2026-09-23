"""Image transform primitives."""

import torch

from ....core.types import ensure_image

OPERATIONS = ("rotate90", "rotate180", "rotate270", "flip_h", "flip_v", "transpose")


class CFXImageTransform:
    """Rotate, flip or transpose an image without resampling."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "operation": (list(OPERATIONS), {"default": "rotate90"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "apply"
    CATEGORY = "ComfyUI-Primitives/Image"

    def apply(self, image, operation):
        img = ensure_image(image)
        if operation == "rotate90":
            out = torch.rot90(img, 1, dims=(1, 2))
        elif operation == "rotate180":
            out = torch.rot90(img, 2, dims=(1, 2))
        elif operation == "rotate270":
            out = torch.rot90(img, 3, dims=(1, 2))
        elif operation == "flip_h":
            out = torch.flip(img, dims=(2,))
        elif operation == "flip_v":
            out = torch.flip(img, dims=(1,))
        elif operation == "transpose":
            out = img.transpose(1, 2)
        else:
            raise ValueError(f"transform: unknown operation {operation!r}")
        return (out.contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_image_transform": CFXImageTransform,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_image_transform": "ComfyUI-Primitives · Image Transform",
}
