"""Show text in the UI (behaviour reimplementation of ShowText|pysssss)."""


class CFXShowText:
    """Display text in the node and pass it through."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True, "forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "show"
    CATEGORY = "ComfyUI-Flow/Text"

    def show(self, text):
        return {"ui": {"text": [text]}, "result": (text,)}


NODE_CLASS_MAPPINGS = {
    "comfyui_flow_show_text": CFXShowText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_flow_show_text": "ComfyUI-Flow · Show Text",
}
