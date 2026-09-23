"""SAM2 loader and box-prompted segmentation (via the shared Apache backend)."""

import comfy.model_management as mm

from ....core.logging import warn_once
from ..backend import load_sam2, segment
from ..geometry import annotations_to_box_batch

SAM2_TYPE = "CFX_SAM2"

SAM2_MODELS = (
    "sam2.1_hiera_large.safetensors",
    "sam2.1_hiera_base_plus.safetensors",
    "sam2.1_hiera_small.safetensors",
    "sam2.1_hiera_tiny.safetensors",
    "sam2_hiera_large.safetensors",
    "sam2_hiera_base_plus.safetensors",
    "sam2_hiera_small.safetensors",
    "sam2_hiera_tiny.safetensors",
)


def resolve_device() -> str:
    device = mm.get_torch_device()
    return "cuda" if device.type == "cuda" else ("mps" if device.type == "mps" else "cpu")


class CFXSAM2Loader:
    """Load a SAM2 checkpoint through the shared backend."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (list(SAM2_MODELS), {"default": SAM2_MODELS[0]}),
                "segmentor": (["single_image", "video"], {"default": "single_image"}),
                "precision": (["fp16", "bf16", "fp32"], {"default": "fp16"}),
            },
        }

    RETURN_TYPES = (SAM2_TYPE,)
    RETURN_NAMES = ("sam2",)
    FUNCTION = "load"
    CATEGORY = "ComfyUI-Segment/Loaders"

    def load(self, model, segmentor="single_image", precision="fp16"):
        device = resolve_device()
        if device == "cpu" and precision != "fp32":
            warn_once("sam2-cpu-fp32", "SAM2 on CPU requires fp32; using fp32")
            precision = "fp32"
        (sam2_model,) = load_sam2(model, segmentor, precision, device)
        return (sam2_model,)


class CFXSAM2Mask:
    """Segment boxes (from annotations) into a mask with SAM2."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sam2": (SAM2_TYPE,),
                "image": ("IMAGE",),
                "annotations": ("JSON",),
            },
            "optional": {
                "keep_model_loaded": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/SAM2"

    def run(self, sam2, image, annotations, keep_model_loaded=False):
        bboxes = annotations_to_box_batch(annotations)
        (mask,) = segment(sam2, image, bboxes=bboxes, keep_model_loaded=keep_model_loaded)
        return (mask,)


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_sam2_loader": CFXSAM2Loader,
    "comfyui_segment_sam2_mask": CFXSAM2Mask,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_sam2_loader": "ComfyUI-Segment · SAM2 Loader",
    "comfyui_segment_sam2_mask": "ComfyUI-Segment · SAM2 Mask",
}
