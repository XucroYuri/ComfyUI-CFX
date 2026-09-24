"""Text-conditioned object detection with GroundingDINO (native transformers)."""

import torch
from PIL import Image

from ....core.device import compute_device
from ....core.types import ensure_image
from ..geometry import boxes_to_mask

DETECT_MODELS = (
    "IDEA-Research/grounding-dino-tiny",
    "IDEA-Research/grounding-dino-base",
)

_CACHE = {}


def _load(model: str):
    if model not in _CACHE:
        from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

        processor = AutoProcessor.from_pretrained(model)
        network = AutoModelForZeroShotObjectDetection.from_pretrained(model, dtype=torch.float32)
        _CACHE[model] = (processor, network.to(compute_device()))
    return _CACHE[model]


class CFXGroundingDinoDetect:
    """Detect boxes for a text prompt and return both JSON and a filled MASK."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"default": "person. dog."}),
                "model": (list(DETECT_MODELS), {"default": DETECT_MODELS[0]}),
                "box_threshold": ("FLOAT", {"default": 0.30, "min": 0.0, "max": 1.0, "step": 0.01}),
                "text_threshold": ("FLOAT", {"default": 0.25, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("JSON", "MASK")
    RETURN_NAMES = ("detections", "mask")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/Detect"

    def run(self, image, prompt, model, box_threshold=0.30, text_threshold=0.25):
        processor, network = _load(model)
        device = network.device

        first = ensure_image(image)[0].clamp(0, 1).cpu().numpy()
        pil = Image.fromarray((first * 255.0).round().astype("uint8"))

        inputs = processor(images=pil, text=prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = network(**inputs)
        result = processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=box_threshold,
            text_threshold=text_threshold,
            target_sizes=[pil.size[::-1]],
        )[0]

        boxes = [[float(v) for v in box] for box in result["boxes"].cpu().tolist()]
        labels = [str(label) for label in (result["text_labels"] if "text_labels" in result else result["labels"])]
        mask = boxes_to_mask(boxes, pil.height, pil.width)
        return ({"bboxes": boxes, "labels": labels}, torch.from_numpy(mask)[None, ...].contiguous())


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_grounding_dino": CFXGroundingDinoDetect,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_grounding_dino": "ComfyUI-Segment · GroundingDINO Detect",
}
