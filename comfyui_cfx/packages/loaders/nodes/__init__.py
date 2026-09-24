"""Loaders node registry."""

from . import quant, safetensors_info

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for _module in (quant, safetensors_info):
    _duplicates = NODE_CLASS_MAPPINGS.keys() & _module.NODE_CLASS_MAPPINGS.keys()
    if _duplicates:
        raise RuntimeError(f"duplicate node ids in loaders: {sorted(_duplicates)}")
    NODE_CLASS_MAPPINGS.update(_module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(_module.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
