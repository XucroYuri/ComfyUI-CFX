"""Seed primitive."""

import random

MAX_SEED = 0xFFFFFFFFFFFFFFFF


class CFXSeed:
    """Produce an integer seed under explicit control."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": MAX_SEED}),
                "control": (["fixed", "randomize", "increment", "decrement"], {"default": "fixed"}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Primitives/Seed"

    def run(self, seed, control):
        if control == "randomize":
            return (random.randint(0, MAX_SEED),)
        if control == "increment":
            return ((int(seed) + 1) % (MAX_SEED + 1),)
        if control == "decrement":
            return ((int(seed) - 1) % (MAX_SEED + 1),)
        return (int(seed),)

    @classmethod
    def IS_CHANGED(cls, seed, control):
        # Force re-execution whenever the seed is not fixed.
        return float("NaN") if control != "fixed" else seed


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_seed": CFXSeed,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_seed": "ComfyUI-Primitives · Seed",
}
