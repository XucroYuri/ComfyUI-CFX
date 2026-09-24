"""Lineart preprocessor (OpenCV adaptive threshold, deterministic).

This is a non-neural approximation of ``AnimeLineArtPreprocessor``: it is
model-free and deterministic, not the neural AnimeLineArt model.
"""

import numpy as np
import torch

from ....core.types import ensure_image


class CFXLineartPreprocessor:
    """Extract dark line-art from an image via adaptive thresholding."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "block_size": ("INT", {"default": 9, "min": 3, "max": 255, "step": 2}),
                "strength": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "invert": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-ControlNet/Preprocessors"

    def run(self, image, block_size=9, strength=0.5, invert=True):
        import cv2

        if block_size < 3 or block_size % 2 == 0:
            raise ValueError(f"block_size must be odd and >= 3, got {block_size}")

        img = ensure_image(image)[0]
        arr = img.detach().cpu().numpy()
        channels = arr.shape[-1]
        if channels == 1:
            rgb = np.repeat(arr, 3, axis=-1)
        else:
            rgb = arr[..., :3]

        gray = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
        gray = np.clip(gray * 255.0, 0.0, 255.0).astype(np.uint8)

        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        c = max(1, round(strength * 50))
        lines = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY_INV,
            int(block_size),
            c,
        )
        if not invert:
            lines = cv2.bitwise_not(lines)

        lines = lines.astype(np.float32) / 255.0
        out_image = torch.from_numpy(lines).unsqueeze(0).unsqueeze(-1).repeat(1, 1, 1, 3)
        out_mask = torch.from_numpy(lines).unsqueeze(0)
        return (out_image, out_mask)


NODE_CLASS_MAPPINGS = {
    "comfyui_controlnet_lineart": CFXLineartPreprocessor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_controlnet_lineart": "ComfyUI-ControlNet · Lineart",
}
