"""Text primitives."""

TEXTS = tuple(f"text{i}" for i in range(1, 9))

_ESCAPES = {"\\n": "\n", "\\t": "\t"}


def _unescape(value: str) -> str:
    return _ESCAPES.get(value, value)


class CFXText:
    """Concatenate or replace text with deterministic, whitespace-aware rules."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "operation": (["concat", "replace"], {"default": "concat"}),
                "delimiter": ("STRING", {"default": ", "}),
                "clean_whitespace": ("BOOLEAN", {"default": True}),
                "skip_empty": ("BOOLEAN", {"default": True}),
                "search": ("STRING", {"default": ""}),
                "replace": ("STRING", {"default": ""}),
            },
            "optional": {name: ("STRING", {"default": "", "multiline": False}) for name in TEXTS},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Primitives/Text"

    def run(self, operation, delimiter=", ", clean_whitespace=True, skip_empty=True,
            search="", replace="", **kwargs):
        if operation == "replace":
            source = kwargs.get(TEXTS[0]) or ""
            if search == "":
                return (source,)
            return (source.replace(search, replace),)

        parts = []
        for name in TEXTS:
            value = kwargs.get(name)
            if value is None:
                continue
            part = value.strip() if clean_whitespace else value
            if skip_empty and part == "":
                continue
            parts.append(part)
        return (_unescape(delimiter).join(parts),)


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_text": CFXText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_text": "ComfyUI-Primitives · Text",
}
