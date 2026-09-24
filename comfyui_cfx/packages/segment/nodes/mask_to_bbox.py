"""Mask -> bounding boxes node."""

from ..geometry import mask_to_bboxes


class CFXMaskToBBox:
    """Convert a MASK into per-item ``[x0, y0, x1, y1]`` bounding boxes."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "threshold": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "multiple_of": ("INT", {"default": 1, "min": 1, "max": 256}),
            },
        }

    RETURN_TYPES = ("JSON", "STRING")
    RETURN_NAMES = ("bboxes", "summary")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/Geometry"

    def run(self, mask, threshold=0.5, multiple_of=1):
        m = mask.float()
        if m.dim() == 2:
            m = m.unsqueeze(0)
        elif m.dim() != 3:
            raise ValueError(f"mask must be [H,W] or [B,H,W], got shape {tuple(mask.shape)}")
        bboxes = mask_to_bboxes(m.detach().cpu().numpy(), threshold, multiple_of)
        if bboxes:
            summary = f"{len(bboxes)} box(es); first: {bboxes[0]['bbox']}"
        else:
            summary = "0 box(es)"
        return (bboxes, summary)


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_mask_to_bbox": CFXMaskToBBox,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_mask_to_bbox": "ComfyUI-Segment · Mask to BBox",
}
