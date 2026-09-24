"""SEGS compatibility shim: MASK <-> Impact-Pack style SEGS (no GPL import)."""

import numpy as np
import torch

from ....core.types import ensure_image
from ..geometry import mask_to_bboxes


def _as_mask_batch(mask) -> np.ndarray:
    """Return ``mask`` as ``[B,H,W]`` float32 numpy, promoting 2D input."""
    if not isinstance(mask, torch.Tensor):
        raise TypeError(f"MASK must be a torch.Tensor, got {type(mask).__name__}")
    m = mask
    if m.dim() == 2:
        m = m.unsqueeze(0)
    elif m.dim() != 3:
        raise ValueError(f"MASK must be [H,W] or [B,H,W], got shape {tuple(mask.shape)}")
    return m.detach().float().cpu().numpy()


class CFXMaskToSegs:
    """Convert the non-empty items of a MASK into Impact-compatible SEGS."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "label": ("STRING", {"default": "segment"}),
                "confidence": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("SEGS",)
    RETURN_NAMES = ("segs",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/Compat"

    def run(self, image, mask, label="segment", confidence=1.0):
        image_np = ensure_image(image).detach().cpu().numpy()
        mask_np = _as_mask_batch(mask)

        height, width = image_np.shape[1:3]
        segs = []
        for index in range(mask_np.shape[0]):
            boxes = mask_to_bboxes(mask_np[index:index + 1], threshold=0.5)
            if not boxes:
                continue
            x0, y0, x1, y1 = boxes[0]["bbox"]
            source = image_np[0] if image_np.shape[0] == 1 else image_np[index]
            cropped_image = source[y0:y1, x0:x1, :]
            cropped_mask = mask_np[index, y0:y1, x0:x1]
            segs.append((
                (height, width),
                {
                    "cropped_image": torch.from_numpy(np.ascontiguousarray(cropped_image)),
                    "cropped_mask": torch.from_numpy(np.ascontiguousarray(cropped_mask)),
                    "confidence": float(confidence),
                    "crop_region": (x0, y0, x1, y1),
                    "bbox": (x0, y0, x1, y1),
                    "label": str(label),
                    "control_net_wrapper": None,
                },
            ))
        return (segs,)


class CFXSegsToMask:
    """Rasterize SEGS entries into one union MASK (``cropped_mask`` OR'd)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "segs": ("SEGS",),
            },
            "optional": {
                "width": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "height": ("INT", {"default": 0, "min": 0, "max": 16384}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/Compat"

    def run(self, segs, width=0, height=0):
        if not segs:
            raise ValueError("segs_to_mask: empty SEGS")
        (full_height, full_width), _ = segs[0]
        out_height = int(height) if height else int(full_height)
        out_width = int(width) if width else int(full_width)

        canvas = np.zeros((out_height, out_width), dtype=np.float32)
        for _, meta in segs:
            x0, y0, x1, y1 = (int(value) for value in meta["crop_region"])
            crop = np.asarray(meta["cropped_mask"], dtype=np.float32)
            region = canvas[y0:y1, x0:x1]
            rows = min(region.shape[0], crop.shape[0])
            cols = min(region.shape[1], crop.shape[1])
            region[:rows, :cols] = np.maximum(region[:rows, :cols], crop[:rows, :cols])
        return (torch.from_numpy(canvas)[None, ...].contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_mask_to_segs": CFXMaskToSegs,
    "comfyui_segment_segs_to_mask": CFXSegsToMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_mask_to_segs": "ComfyUI-Segment · Mask to SEGS",
    "comfyui_segment_segs_to_mask": "ComfyUI-Segment · SEGS to Mask",
}
