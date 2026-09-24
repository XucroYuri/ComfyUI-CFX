"""Scale a SIGMAS tensor by a constant factor."""


class CFXSigmaShift:
    """Multiply a 1-D SIGMAS tensor by ``factor``."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sigmas": ("SIGMAS",),
                "factor": ("FLOAT", {"default": 1.0, "min": 0.001, "max": 10.0, "step": 0.001}),
            },
        }

    RETURN_TYPES = ("SIGMAS",)
    RETURN_NAMES = ("sigmas",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Sampling/Sigmas"

    def run(self, sigmas, factor):
        if sigmas.dim() != 1:
            raise ValueError(f"sigma_shift: expected 1-D SIGMAS, got shape {tuple(sigmas.shape)}")
        return ((sigmas * factor).contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_sampling_sigma_shift": CFXSigmaShift,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_sampling_sigma_shift": "ComfyUI-Sampling · Sigma Shift",
}
