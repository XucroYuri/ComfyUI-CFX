"""Vision node registry."""

from . import florence2, tags, text

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for _module in (florence2, text, tags):
    _duplicates = NODE_CLASS_MAPPINGS.keys() & _module.NODE_CLASS_MAPPINGS.keys()
    if _duplicates:
        raise RuntimeError(f"duplicate node ids in vision: {sorted(_duplicates)}")
    NODE_CLASS_MAPPINGS.update(_module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(_module.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
