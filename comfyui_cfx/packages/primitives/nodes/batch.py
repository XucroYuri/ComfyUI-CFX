"""Batch and list primitives.

``batch_list`` from the plan is split into two nodes because ComfyUI decides
``OUTPUT_IS_LIST`` at class definition time: ``CFXImageBatch`` concatenates up to
eight images into one batch, ``CFXImageSplit`` turns a batch into a list.
"""

import torch

from ....core.types import ensure_image

INPUTS = tuple(f"image{i}" for i in range(1, 9))


class CFXImageBatch:
    """Concatenate up to eight same-sized images into a single batch."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {name: ("IMAGE",) for name in INPUTS},
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "batch"
    CATEGORY = "ComfyUI-Primitives/Batch"

    def batch(self, **kwargs):
        images = [ensure_image(kwargs[name]) for name in INPUTS if kwargs.get(name) is not None]
        if not images:
            raise ValueError("batch: no connected image")
        if len(images) == 1:
            return (images[0],)
        shape = images[0].shape[1:]
        if any(image.shape[1:] != shape for image in images):
            raise ValueError("batch: image sizes or channel counts differ")
        return (torch.cat(images, dim=0).contiguous(),)


class CFXImageSplit:
    """Split a batch into a list of single-image batches."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"image": ("IMAGE",)}}

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "split"
    CATEGORY = "ComfyUI-Primitives/Batch"

    def split(self, image):
        img = ensure_image(image)
        return ([img[index:index + 1].contiguous() for index in range(img.shape[0])],)


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_image_batch": CFXImageBatch,
    "comfyui_primitives_image_split": CFXImageSplit,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_image_batch": "ComfyUI-Primitives · Image Batch",
    "comfyui_primitives_image_split": "ComfyUI-Primitives · Image Split",
}
