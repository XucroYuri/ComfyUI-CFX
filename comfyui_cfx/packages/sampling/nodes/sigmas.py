"""Split a SIGMAS tensor at a step index."""


class CFXSplitSigmas:
    """Split a 1-D SIGMAS tensor into high (prefix) and low (suffix) parts."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sigmas": ("SIGMAS",),
                "step": ("INT", {"default": 0, "min": 0, "max": 10000}),
            },
        }

    RETURN_TYPES = ("SIGMAS", "SIGMAS")
    RETURN_NAMES = ("sigmas_high", "sigmas_low")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Sampling/Sigmas"

    def run(self, sigmas, step):
        if sigmas.dim() != 1:
            raise ValueError(f"split_sigmas: expected 1-D SIGMAS, got shape {tuple(sigmas.shape)}")
        if step > len(sigmas):
            raise ValueError(f"split_sigmas: step {step} exceeds sigmas length {len(sigmas)}")
        return (sigmas[:step].contiguous(), sigmas[step:].contiguous())


NODE_CLASS_MAPPINGS = {
    "comfyui_sampling_split_sigmas": CFXSplitSigmas,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_sampling_split_sigmas": "ComfyUI-Sampling · Split Sigmas",
}
