"""Primitives node registry."""

from . import batch, boolean, crop, image, json_access, mask, math, resolution, save, seed, stitch, switch, text, transform

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for _module in (image, crop, transform, stitch, batch, switch, boolean, math, text, mask, resolution, seed, save, json_access):
    _duplicates = NODE_CLASS_MAPPINGS.keys() & _module.NODE_CLASS_MAPPINGS.keys()
    if _duplicates:
        raise RuntimeError(f"duplicate node ids in primitives: {sorted(_duplicates)}")
    NODE_CLASS_MAPPINGS.update(_module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(_module.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
