"""Vision node registry."""

from . import blip, clip_interrogator, florence2, tags, text, vlm, wd14

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for _module in (florence2, wd14, blip, clip_interrogator, vlm, text, tags):
    _duplicates = NODE_CLASS_MAPPINGS.keys() & _module.NODE_CLASS_MAPPINGS.keys()
    if _duplicates:
        raise RuntimeError(f"duplicate node ids in vision: {sorted(_duplicates)}")
    NODE_CLASS_MAPPINGS.update(_module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(_module.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
