"""BLIP-2 caption / VQA node (native transformers, loaded lazily)."""

from ....core.device import compute_device, resolve_dtype
from ....core.images import first_image_to_pil

BLIP2_MODELS = (
    "Salesforce/blip2-opt-2.7b",
    "Salesforce/blip2-flan-t5-xl",
    "Salesforce/blip2-opt-6.7b",
)

_CACHE = {}


def _load(model: str, precision: str):
    dtype = resolve_dtype(precision)
    key = (model, precision)
    if key not in _CACHE:
        from transformers import Blip2ForConditionalGeneration, Blip2Processor

        processor = Blip2Processor.from_pretrained(model)
        network = Blip2ForConditionalGeneration.from_pretrained(model, dtype=dtype)
        _CACHE[key] = (processor, network.to(compute_device()))
    return _CACHE[key]


class CFXBlip2Caption:
    """Caption or question-answer an image with BLIP-2."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (list(BLIP2_MODELS), {"default": BLIP2_MODELS[0]}),
                "mode": (["caption", "vqa"], {"default": "caption"}),
                "question": ("STRING", {"default": "What is in the image?"}),
                "max_new_tokens": ("INT", {"default": 64, "min": 1, "max": 512}),
                "precision": (["bf16", "fp16", "fp32"], {"default": "bf16"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Vision/Caption"

    def run(self, image, model, mode="caption", question="What is in the image?",
            max_new_tokens=64, precision="bf16"):
        processor, network = _load(model, precision)
        dtype = network.dtype
        pil = first_image_to_pil(image)

        if mode == "vqa":
            inputs = processor(pil, question, return_tensors="pt")
        else:
            inputs = processor(pil, return_tensors="pt")
        inputs = inputs.to(network.device)
        for key, value in inputs.items():
            if value.dtype.is_floating_point:
                inputs[key] = value.to(dtype)

        output = network.generate(**inputs, max_new_tokens=max_new_tokens)
        return (processor.decode(output[0], skip_special_tokens=True).strip(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_vision_blip2_caption": CFXBlip2Caption,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_vision_blip2_caption": "ComfyUI-Vision · BLIP2 Caption",
}
