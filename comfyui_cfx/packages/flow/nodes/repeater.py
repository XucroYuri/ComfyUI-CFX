"""Repeat a value into a list (behaviour reimplementation of Repeater|pysssss)."""

from ....core.anytype import any_type


class CFXRepeater:
    """Emit the same value N times as a list."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (any_type,),
                "repeats": ("INT", {"default": 2, "min": 1, "max": 64}),
            },
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("values",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "repeat"
    CATEGORY = "ComfyUI-Flow/Util"

    def repeat(self, value, repeats):
        return ([value] * int(repeats),)


NODE_CLASS_MAPPINGS = {
    "comfyui_flow_repeater": CFXRepeater,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_flow_repeater": "ComfyUI-Flow · Repeater",
}
