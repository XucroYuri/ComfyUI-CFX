"""Concatenate two CONDITIONING lists, keeping both sets of entries (e.g. regional conditioning)."""


class CFXConditioningConcat:
    """Return a new CONDITIONING list: ``a``'s entries followed by ``b``'s entries."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning_a": ("CONDITIONING",),
                "conditioning_b": ("CONDITIONING",),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("conditioning",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Flux/Conditioning"

    def run(self, conditioning_a, conditioning_b):
        if not isinstance(conditioning_a, list) or not isinstance(conditioning_b, list):
            raise ValueError("conditioning_a and conditioning_b must be lists")
        if not conditioning_a or not conditioning_b:
            raise ValueError("conditioning_a and conditioning_b must be non-empty")

        return (list(conditioning_a) + list(conditioning_b),)


NODE_CLASS_MAPPINGS = {
    "comfyui_flux_conditioning_concat": CFXConditioningConcat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_flux_conditioning_concat": "ComfyUI-Flux · Conditioning Concat",
}
