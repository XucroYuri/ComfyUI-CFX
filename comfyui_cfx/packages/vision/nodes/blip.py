"""BLIP caption / interrogate node (native transformers, loaded lazily)."""

from ....core.device import compute_device
from ....core.images import first_image_to_pil

BLIP_MODELS = (
    "Salesforce/blip-image-captioning-base",
    "Salesforce/blip-image-captioning-large",
    "Salesforce/blip-vqa-base",
)

_CACHE = {}


def _load(model: str):
    if model not in _CACHE:
        from transformers import BlipForConditionalGeneration, BlipForQuestionAnswering, BlipProcessor

        processor = BlipProcessor.from_pretrained(model)
        if "vqa" in model:
            network = BlipForQuestionAnswering.from_pretrained(model)
        else:
            network = BlipForConditionalGeneration.from_pretrained(model)
        device = compute_device()
        _CACHE[model] = (processor, network.to(device), device)
    return _CACHE[model]


class CFXBlipCaption:
    """Caption or interrogate an image with BLIP."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (list(BLIP_MODELS), {"default": BLIP_MODELS[0]}),
                "mode": (["caption", "interrogate"], {"default": "caption"}),
                "question": ("STRING", {"default": "What is in the image?"}),
                "max_new_tokens": ("INT", {"default": 64, "min": 1, "max": 512}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Vision/Caption"

    def run(self, image, model, mode="caption", question="What is in the image?", max_new_tokens=64):
        processor, network, device = _load(model)
        pil = first_image_to_pil(image)

        if mode == "interrogate":
            inputs = processor(pil, question, return_tensors="pt").to(device)
        else:
            inputs = processor(pil, return_tensors="pt").to(device)
        output = network.generate(**inputs, max_new_tokens=max_new_tokens)
        return (processor.decode(output[0], skip_special_tokens=True).strip(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_vision_blip_caption": CFXBlipCaption,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_vision_blip_caption": "ComfyUI-Vision · BLIP Caption",
}
