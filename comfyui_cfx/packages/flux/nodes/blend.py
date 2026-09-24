"""Blend two CONDITIONING lists with a linear factor (behaviour reimplementation of ConditioningKrea2Rebalance)."""


class CFXConditioningBlend:
    """Linearly interpolate two CONDITIONING lists, keeping ``a``'s metadata and dtype."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "conditioning_a": ("CONDITIONING",),
                "conditioning_b": ("CONDITIONING",),
                "factor": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("conditioning",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Flux/Conditioning"

    def run(self, conditioning_a, conditioning_b, factor=0.5):
        if not isinstance(conditioning_a, list) or not isinstance(conditioning_b, list):
            raise ValueError("conditioning_a and conditioning_b must be lists")
        if not conditioning_a or not conditioning_b:
            raise ValueError("conditioning_a and conditioning_b must be non-empty")
        if len(conditioning_a) != len(conditioning_b):
            raise ValueError(
                f"conditioning_a and conditioning_b must have the same length, got {len(conditioning_a)} and {len(conditioning_b)}"
            )

        blended = []
        for entry_a, entry_b in zip(conditioning_a, conditioning_b):
            tensor_a, meta_a = entry_a[0], entry_a[1]
            tensor_b = entry_b[0]
            tensor_b = tensor_b.to(dtype=tensor_a.dtype, device=tensor_a.device)
            blended.append([tensor_a * (1.0 - factor) + tensor_b * factor, dict(meta_a)])
        return (blended,)


NODE_CLASS_MAPPINGS = {
    "comfyui_flux_conditioning_blend": CFXConditioningBlend,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_flux_conditioning_blend": "ComfyUI-Flux · Conditioning Blend",
}
