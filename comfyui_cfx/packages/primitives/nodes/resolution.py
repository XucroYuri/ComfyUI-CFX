"""Resolution / aspect-ratio primitive.

Only outputs width and height. Latent creation stays with ComfyUI's own empty
latent nodes so model-specific channel counts are never guessed here.
"""

RATIOS = {
    "1:1": (1, 1),
    "4:3": (4, 3),
    "3:2": (3, 2),
    "16:9": (16, 9),
    "21:9": (21, 9),
    "3:4": (3, 4),
    "2:3": (2, 3),
    "9:16": (9, 16),
    "custom": (1, 1),
}


def _align(value: float, multiple_of: int) -> int:
    return max(int(multiple_of), int(round(value / multiple_of)) * int(multiple_of))


class CFXResolution:
    """Resolve width/height from a preset ratio, megapixels, or explicit overrides."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "preset": (list(RATIOS), {"default": "1:1"}),
                "megapixels": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 64.0, "step": 0.01}),
                "orientation": (["landscape", "portrait"], {"default": "landscape"}),
                "multiple_of": ("INT", {"default": 8, "min": 1, "max": 256}),
            },
            "optional": {
                "width_override": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "height_override": ("INT", {"default": 0, "min": 0, "max": 16384}),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "compute"
    CATEGORY = "ComfyUI-Primitives/Resolution"

    def compute(self, preset, megapixels=1.0, orientation="landscape", multiple_of=8,
                width_override=0, height_override=0):
        ratio_w, ratio_h = RATIOS[preset]
        if orientation == "portrait":
            ratio_w, ratio_h = ratio_h, ratio_w

        if width_override > 0 and height_override > 0:
            width, height = float(width_override), float(height_override)
        elif width_override > 0:
            width = float(width_override)
            height = width * ratio_h / ratio_w
        elif height_override > 0:
            height = float(height_override)
            width = height * ratio_w / ratio_h
        else:
            area = megapixels * 1_000_000.0
            width = (area * ratio_w / ratio_h) ** 0.5
            height = (area * ratio_h / ratio_w) ** 0.5

        return (_align(width, multiple_of), _align(height, multiple_of))


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_resolution": CFXResolution,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_resolution": "ComfyUI-Primitives · Resolution",
}
