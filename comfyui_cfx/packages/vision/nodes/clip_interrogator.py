"""CLIP Interrogator node (lazy `clip_interrogator` backend)."""

from ....core.images import first_image_to_pil

CLIP_MODELS = (
    "ViT-L-14/openai",
    "ViT-H-14/laion2b_s32b_b79k",
)

MODE_METHODS = {
    "fast": "interrogate_fast",
    "classic": "interrogate_classic",
    "best": "interrogate",
    "negative": "interrogate_negative",
}

_CACHE = {}


def _load(clip_model: str):
    if clip_model not in _CACHE:
        from clip_interrogator import Config, Interrogator

        _CACHE[clip_model] = Interrogator(Config(clip_model_name=clip_model))
    return _CACHE[clip_model]


class CFXClipInterrogator:
    """Interrogate an image into a prompt-style caption with CLIP Interrogator."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "clip_model": (list(CLIP_MODELS), {"default": CLIP_MODELS[0]}),
                "mode": (list(MODE_METHODS), {"default": "fast"}),
                "max_flavors": ("INT", {"default": 4, "min": 1, "max": 16}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Vision/Caption"

    def run(self, image, clip_model="ViT-L-14/openai", mode="fast", max_flavors=4):
        if mode not in MODE_METHODS:
            raise ValueError(f"unknown CLIP Interrogator mode {mode!r}")

        interrogator = _load(clip_model)
        pil = first_image_to_pil(image)
        method = getattr(interrogator, MODE_METHODS[mode])
        if mode == "negative":
            return (method(pil),)
        return (method(pil, max_flavors=max_flavors),)


NODE_CLASS_MAPPINGS = {
    "comfyui_vision_clip_interrogator": CFXClipInterrogator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_vision_clip_interrogator": "ComfyUI-Vision · CLIP Interrogator",
}
