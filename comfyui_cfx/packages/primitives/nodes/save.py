"""Save image with embedded metadata."""

import json
import os

import folder_paths
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from ....core.paths import output_dir


def validate_prefix(prefix: str) -> str:
    prefix = prefix or "ComfyUI-CFX"
    if os.path.isabs(prefix):
        raise ValueError(f"save image: filename_prefix must be relative, got {prefix!r}")
    if any(part == ".." for part in prefix.replace("\\", "/").split("/")):
        raise ValueError("save image: filename_prefix must not contain '..'")
    return prefix


class CFXSaveImageMetadata:
    """Save images to the output folder with prompt metadata and workflow embedding."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI-CFX"}),
                "positive": ("STRING", {"default": "", "multiline": True}),
                "negative": ("STRING", {"default": "", "multiline": True}),
                "format": (["png", "jpg", "webp"], {"default": "png"}),
                "quality": ("INT", {"default": 95, "min": 1, "max": 100}),
                "embed_workflow": ("BOOLEAN", {"default": True}),
                "save_metadata_txt": ("BOOLEAN", {"default": False}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "save"
    CATEGORY = "ComfyUI-Primitives/IO"

    def save(self, images, filename_prefix, positive="", negative="", format="png", quality=95,
             embed_workflow=True, save_metadata_txt=False, prompt=None, extra_pnginfo=None):
        prefix = validate_prefix(filename_prefix)
        front, _, height, width = images.shape
        folder, filename, counter, subfolder, _ = folder_paths.get_save_image_path(
            prefix, output_dir(), width, height
        )

        results = []
        for index in range(front):
            array = (images[index].clamp(0, 1).cpu().numpy() * 255.0).round().astype(np.uint8)
            image = Image.fromarray(array)
            name = f"{filename}_{counter:05}_.{format}"
            path = os.path.join(folder, name)
            parameters = f"{positive}\nNegative prompt: {negative}\nSize: {width}x{height}"

            if format == "png":
                info = PngInfo()
                info.add_text("parameters", parameters)
                if embed_workflow and prompt is not None:
                    info.add_text("prompt", json.dumps(prompt))
                if embed_workflow and extra_pnginfo is not None:
                    for key, value in extra_pnginfo.items():
                        info.add_text(key, json.dumps(value))
                image.save(path, pnginfo=info)
            else:
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image.save(path, quality=int(quality))

            if save_metadata_txt:
                with open(os.path.join(folder, f"{filename}_{counter:05}_.txt"), "w", encoding="utf-8") as handle:
                    handle.write(parameters)

            results.append({"filename": name, "subfolder": subfolder, "type": "output"})
            counter += 1

        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_save_image_metadata": CFXSaveImageMetadata,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_save_image_metadata": "ComfyUI-Primitives · Save Image (Metadata)",
}
