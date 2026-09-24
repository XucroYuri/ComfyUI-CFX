"""Summarize a safetensors file: tensor count, dtype histogram, metadata keys."""

import folder_paths
from safetensors import SafetensorError, safe_open

from ....core.paths import safe_join


class CFXSafetensorsInfo:
    """Report tensor count, dtype counts and metadata keys of a safetensors file."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("JSON",)
    RETURN_NAMES = ("info",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Loaders/Quant"

    def run(self, path):
        target = safe_join(folder_paths.models_dir, path)
        try:
            with safe_open(target, framework="pt") as handle:
                keys = list(handle.keys())
                dtypes = {}
                for key in keys:
                    dtype = handle.get_slice(key).get_dtype()
                    dtypes[dtype] = dtypes.get(dtype, 0) + 1
                metadata = handle.metadata() or {}
        except SafetensorError as exc:
            raise ValueError(f"not a safetensors file: {exc}") from exc

        return (
            {
                "tensor_count": len(keys),
                "dtypes": dtypes,
                "metadata_keys": sorted(metadata),
            },
        )


NODE_CLASS_MAPPINGS = {
    "comfyui_loaders_safetensors_info": CFXSafetensorsInfo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_loaders_safetensors_info": "ComfyUI-Loaders · Safetensors Info",
}
