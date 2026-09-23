"""Any-typed routing primitives."""

from ....core.anytype import any_type

INPUTS = tuple(f"input{i}" for i in range(1, 9))


class CFXSwitch:
    """Route one of eight any-typed inputs by index or by first connection."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["index", "first_connected"], {"default": "index"}),
                "index": ("INT", {"default": 0, "min": 0, "max": 7}),
            },
            "optional": {name: (any_type,) for name in INPUTS},
        }

    RETURN_TYPES = (any_type, "INT")
    RETURN_NAMES = ("value", "selected_index")
    FUNCTION = "switch"
    CATEGORY = "ComfyUI-Primitives/Logic"

    def switch(self, mode, index=0, **kwargs):
        if mode == "first_connected":
            for position, name in enumerate(INPUTS):
                value = kwargs.get(name)
                if value is not None:
                    return (value, position)
            raise ValueError("switch: no connected input")

        position = min(max(int(index), 0), len(INPUTS) - 1)
        value = kwargs.get(INPUTS[position])
        if value is None:
            raise ValueError(f"switch: {INPUTS[position]} is not connected")
        return (value, position)


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_switch": CFXSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_switch": "ComfyUI-Primitives · Switch",
}
