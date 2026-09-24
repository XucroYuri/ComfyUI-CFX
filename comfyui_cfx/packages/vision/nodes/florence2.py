"""Florence-2 loader and task runner (uses the ComfyUI-Florence2 backend)."""

import os

import comfy.model_management as mm
import folder_paths

from ....core.device import resolve_dtype
from ....core.types import ensure_image
from ..backend import load_florence2
from ..registry import FLORENCE2_MODELS, FLORENCE2_TASKS, task_token

FLORENCE2_TYPE = "CFX_FLORENCE2"


class CFXFlorence2Loader:
    """Download (if needed) and load a Florence-2 model via the shared backend."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (list(FLORENCE2_MODELS), {"default": FLORENCE2_MODELS[0]}),
                "precision": (["fp16", "bf16", "fp32"], {"default": "fp16"}),
            },
        }

    RETURN_TYPES = (FLORENCE2_TYPE,)
    RETURN_NAMES = ("florence2",)
    FUNCTION = "load"
    CATEGORY = "ComfyUI-Vision/Loaders"

    def load(self, model, precision="fp16"):
        dtype = resolve_dtype(precision)
        name = model.rsplit("/", 1)[-1]
        path = os.path.join(folder_paths.models_dir, "LLM", name)
        if not os.path.isdir(path):
            from huggingface_hub import snapshot_download

            snapshot_download(repo_id=model, local_dir=path)

        patcher, processor = load_florence2(path, dtype)
        mm.load_model_gpu(patcher)
        return ({"patcher": patcher, "processor": processor, "dtype": dtype, "path": path},)


class CFXFlorence2Run:
    """Run one Florence-2 task on an image."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "florence2": (FLORENCE2_TYPE,),
                "image": ("IMAGE",),
                "task": (list(FLORENCE2_TASKS), {"default": "more_detailed_caption"}),
            },
            "optional": {
                "max_new_tokens": ("INT", {"default": 1024, "min": 1, "max": 4096}),
                "num_beams": ("INT", {"default": 3, "min": 1, "max": 64}),
                "do_sample": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING", "JSON")
    RETURN_NAMES = ("text", "parsed")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Vision/Florence2"

    def run(self, florence2, image, task, max_new_tokens=1024, num_beams=3, do_sample=False):
        token = task_token(task)
        patcher = florence2["patcher"]
        processor = florence2["processor"]
        dtype = florence2["dtype"]
        device = patcher.load_device
        model = patcher.model

        first = ensure_image(image)[0].permute(2, 0, 1).contiguous()
        inputs = processor(text=token, images=first)
        generated_ids = model.generate(
            input_ids=inputs["input_ids"].to(device),
            pixel_values=inputs["pixel_values"].to(dtype=dtype, device=device),
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            num_beams=num_beams,
        )
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        parsed = processor.post_process_generation(
            generated_text, task=token, image_size=(first.shape[2], first.shape[1])
        )[token]

        text = parsed if isinstance(parsed, str) else ""
        return (text, parsed)


NODE_CLASS_MAPPINGS = {
    "comfyui_vision_florence2_loader": CFXFlorence2Loader,
    "comfyui_vision_florence2_run": CFXFlorence2Run,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_vision_florence2_loader": "ComfyUI-Vision · Florence-2 Loader",
    "comfyui_vision_florence2_run": "ComfyUI-Vision · Florence-2 Run",
}
