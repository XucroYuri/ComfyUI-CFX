"""Flow node registry."""

from . import constrain_image, repeater, show_text, string_function, text_file

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for _module in (string_function, show_text, constrain_image, repeater, text_file):
    _duplicates = NODE_CLASS_MAPPINGS.keys() & _module.NODE_CLASS_MAPPINGS.keys()
    if _duplicates:
        raise RuntimeError(f"duplicate node ids in flow: {sorted(_duplicates)}")
    NODE_CLASS_MAPPINGS.update(_module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(_module.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
