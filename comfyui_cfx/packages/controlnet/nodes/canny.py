"""Canny edge preprocessor (OpenCV, deterministic)."""

import numpy as np
import torch

from ....core.types import ensure_image


class CFXCannyPreprocessor:
    """Extract Canny edges from an image, returning both edge image and mask."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "low_threshold": ("FLOAT", {"default": 100.0, "min": 0.0, "max": 255.0}),
                "high_threshold": ("FLOAT", {"default": 200.0, "min": 0.0, "max": 255.0}),
                "aperture_size": ("INT", {"default": 3, "min": 3, "max": 7, "step": 2}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-ControlNet/Preprocessors"

    def run(self, image, low_threshold=100.0, high_threshold=200.0, aperture_size=3):
        import cv2

        if high_threshold < low_threshold:
            raise ValueError(
                f"high_threshold ({high_threshold}) must be >= low_threshold ({low_threshold})"
            )

        img = ensure_image(image)[0]
        arr = img.detach().cpu().numpy()
        channels = arr.shape[-1]
        if channels == 1:
            rgb = np.repeat(arr, 3, axis=-1)
        else:
            rgb = arr[..., :3]

        gray = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
        gray = np.clip(gray * 255.0, 0.0, 255.0).astype(np.uint8)

        edges = cv2.Canny(
            gray,
            float(low_threshold),
            float(high_threshold),
            apertureSize=int(aperture_size),
        )
        edges = (edges.astype(np.float32) / 255.0)

        out_image = torch.from_numpy(edges).unsqueeze(0).unsqueeze(-1).repeat(1, 1, 1, 3)
        out_mask = torch.from_numpy(edges).unsqueeze(0)
        return (out_image, out_mask)


NODE_CLASS_MAPPINGS = {
    "comfyui_controlnet_canny": CFXCannyPreprocessor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_controlnet_canny": "ComfyUI-ControlNet · Canny",
}
