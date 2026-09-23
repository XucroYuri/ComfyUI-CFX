"""Image stitching primitives."""

import torch

from ....core.types import ensure_image

INPUTS = tuple(f"image{i}" for i in range(1, 9))


class CFXImageStitch:
    """Stitch up to eight same-sized images horizontally or vertically."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "direction": (["horizontal", "vertical"], {"default": "horizontal"}),
                "spacing": ("INT", {"default": 0, "min": 0, "max": 512}),
                "background": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {name: ("IMAGE",) for name in INPUTS},
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "stitch"
    CATEGORY = "ComfyUI-Primitives/Image"

    def stitch(self, direction, spacing=0, background=0.0, **kwargs):
        images = [ensure_image(kwargs[name]) for name in INPUTS if kwargs.get(name) is not None]
        if not images:
            raise ValueError("stitch: no connected image")
        if len(images) == 1:
            return (images[0],)

        first = images[0]
        batch, _, _, channels = first.shape
        if any(image.shape[0] != batch for image in images):
            raise ValueError("stitch: batch sizes differ")
        if any(image.shape[3] != channels for image in images):
            raise ValueError("stitch: channel counts differ")

        if direction == "horizontal":
            if any(image.shape[1] != first.shape[1] for image in images):
                raise ValueError("stitch: heights differ for horizontal stitch")
            total = sum(image.shape[2] for image in images) + spacing * (len(images) - 1)
            out = torch.full((batch, first.shape[1], total, channels), background,
                             dtype=first.dtype, device=first.device)
            offset = 0
            for image in images:
                width = image.shape[2]
                out[:, :, offset:offset + width, :] = image
                offset += width + spacing
        else:
            if any(image.shape[2] != first.shape[2] for image in images):
                raise ValueError("stitch: widths differ for vertical stitch")
            total = sum(image.shape[1] for image in images) + spacing * (len(images) - 1)
            out = torch.full((batch, total, first.shape[2], channels), background,
                             dtype=first.dtype, device=first.device)
            offset = 0
            for image in images:
                height = image.shape[1]
                out[:, offset:offset + height, :, :] = image
                offset += height + spacing

        return (out.contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_image_stitch": CFXImageStitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_image_stitch": "ComfyUI-Primitives · Image Stitch",
}
