"""WD14 ONNX tagger node."""

import numpy as np
from PIL import Image

from ....core.types import ensure_image
from ..wd14 import WD14_MODELS, format_tags, get_session, load_tag_rows, model_files, prepare_image, select_tags


class CFXWD14Tagger:
    """Tag an image with a WD14 ONNX model (SmilingWolf)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (list(WD14_MODELS), {"default": WD14_MODELS[0]}),
                "general_threshold": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
                "character_threshold": ("FLOAT", {"default": 0.85, "min": 0.0, "max": 1.0, "step": 0.01}),
                "replace_underscore": ("BOOLEAN", {"default": True}),
                "exclude_tags": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tags",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Vision/Tagging"

    def run(self, image, model, general_threshold=0.35, character_threshold=0.85,
            replace_underscore=True, exclude_tags=""):
        _, csv_path = model_files(model)
        rows = load_tag_rows(csv_path)
        session = get_session(model)

        input_name = session.get_inputs()[0].name
        shape = session.get_inputs()[0].shape
        size = shape[-1] if isinstance(shape[-1], int) else shape[-2]

        first = ensure_image(image)[0].cpu().numpy()
        pil = Image.fromarray((first.clamp(0, 1).numpy() * 255.0).round().astype(np.uint8))
        batch = prepare_image(pil, int(size))[None, ...]

        probs = session.run(None, {input_name: batch})[0][0]
        general, character = select_tags(rows, probs, general_threshold, character_threshold)
        return (format_tags(character + general, replace_underscore, exclude_tags),)


NODE_CLASS_MAPPINGS = {
    "comfyui_vision_wd14_tagger": CFXWD14Tagger,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_vision_wd14_tagger": "ComfyUI-Vision · WD14 Tagger",
}
