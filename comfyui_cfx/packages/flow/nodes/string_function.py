"""String manipulation node (behaviour reimplementation of StringFunction|pysssss)."""

import re

TIDY_DELIMITER = ", "


def _join(left: str, right: str, delimiter: str) -> str:
    if not left:
        return right
    if not right:
        return left
    return left + delimiter + right


def _tidy(value: str) -> str:
    parts = [part.strip() for part in value.split(",")]
    return TIDY_DELIMITER.join(part for part in parts if part)


class CFXStringFunction:
    """Append / prepend / replace / regex-replace on text, with optional tag tidy."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "action": (["append", "prepend", "replace", "regex_replace"], {"default": "append"}),
                "text": ("STRING", {"default": "", "multiline": False}),
                "other": ("STRING", {"default": "", "multiline": False}),
                "replacement": ("STRING", {"default": "", "multiline": False}),
                "delimiter": ("STRING", {"default": ", "}),
                "tidy": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Flow/Text"

    def run(self, action, text="", other="", replacement="", delimiter=", ", tidy=False):
        if action == "append":
            result = _join(text, other, delimiter)
        elif action == "prepend":
            result = _join(other, text, delimiter)
        elif action == "replace":
            result = text.replace(other, replacement) if other else text
        elif action == "regex_replace":
            if not other:
                result = text
            else:
                try:
                    result = re.sub(other, replacement, text)
                except re.error as exc:
                    raise ValueError(f"string_function: invalid regex ({exc})") from exc
        else:
            raise ValueError(f"string_function: unknown action {action!r}")

        if tidy:
            result = _tidy(result)
        return (result,)


NODE_CLASS_MAPPINGS = {
    "comfyui_flow_string_function": CFXStringFunction,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_flow_string_function": "ComfyUI-Flow · String Function",
}
