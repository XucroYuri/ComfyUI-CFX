"""Matting / background removal via rembg (MIT)."""

import numpy as np
import torch
from PIL import Image

from ....core.types import ensure_image

MATTING_MODELS = (
    "birefnet-general",
    "birefnet-general-lite",
    "birefnet-portrait",
    "isnet-general-use",
    "isnet-anime",
    "u2net",
    "u2net_human_seg",
)

_SESSIONS = {}


def get_session(model: str):
    """Return a cached rembg session for ``model``."""
    if model not in _SESSIONS:
        from rembg import new_session

        _SESSIONS[model] = new_session(model)
    return _SESSIONS[model]


def alpha_to_mask(rgba: np.ndarray) -> np.ndarray:
    """Extract the alpha channel of an ``HxWx4`` uint8 array as a float32 mask."""
    if rgba.ndim != 3 or rgba.shape[2] < 4:
        raise ValueError("matting: expected an HxWx4 RGBA array")
    return np.asarray(rgba, dtype=np.float32)[..., 3] / 255.0


class CFXMatting:
    """Remove the background, returning an alpha MASK and an RGBA cutout image."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (list(MATTING_MODELS), {"default": MATTING_MODELS[0]}),
            },
        }

    RETURN_TYPES = ("MASK", "IMAGE")
    RETURN_NAMES = ("mask", "image")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/Matting"

    def run(self, image, model):
        from rembg import remove

        session = get_session(model)
        first = ensure_image(image)[0].cpu().numpy()
        pil = Image.fromarray((first.clamp(0, 1).numpy() * 255.0).round().astype("uint8"))

        cutout = np.asarray(remove(pil, session=session))
        mask = alpha_to_mask(cutout)
        rgba = np.ascontiguousarray(cutout.astype(np.float32) / 255.0)
        mask_tensor = torch.from_numpy(mask)[None, ...].contiguous()
        image_tensor = torch.from_numpy(rgba)[None, ...].contiguous()
        return (mask_tensor, image_tensor)


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_matting": CFXMatting,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_matting": "ComfyUI-Segment · Matting",
}
