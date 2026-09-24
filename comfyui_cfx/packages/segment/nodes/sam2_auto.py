"""SAM2 automatic mask generation (no prompts).

The upstream preview image is intentionally dropped: this node exposes only the
combined mask plus the per-mask bboxes, so callers compose their own overlay.
"""

from ..backend import auto_mask
from .sam2 import SAM2_TYPE


class CFXSam2AutoMask:
    """Segment every object in an image with SAM2's automatic mask generator."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sam2": (SAM2_TYPE,),
                "image": ("IMAGE",),
            },
            "optional": {
                "keep_model_loaded": ("BOOLEAN", {"default": False}),
                "points_per_side": ("INT", {"default": 32, "min": 1}),
                "pred_iou_thresh": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.01}),
                "stability_score_thresh": ("FLOAT", {"default": 0.95, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("MASK", "JSON")
    RETURN_NAMES = ("mask", "bboxes")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/SAM2"

    def run(self, sam2, image, keep_model_loaded=False, points_per_side=32,
            pred_iou_thresh=0.8, stability_score_thresh=0.95):
        segmentor = sam2.get("segmentor")
        if segmentor != "automaskgenerator":
            raise ValueError(
                "SAM2 auto mask needs a handle loaded with segmentor='automaskgenerator', "
                f"but this handle used segmentor={segmentor!r}; set the SAM2 Loader 'segmentor' widget "
                "to 'automaskgenerator' and reload the model."
            )
        mask, _preview, bboxes = auto_mask(
            sam2,
            image,
            keep_model_loaded=keep_model_loaded,
            points_per_side=points_per_side,
            pred_iou_thresh=pred_iou_thresh,
            stability_score_thresh=stability_score_thresh,
        )
        return (mask, bboxes)


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_sam2_auto_mask": CFXSam2AutoMask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_sam2_auto_mask": "ComfyUI-Segment · SAM2 Auto Mask",
}
