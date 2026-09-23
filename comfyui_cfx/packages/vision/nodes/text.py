"""Caption / tag text primitives."""


def _strip_control_tokens(text: str) -> str:
    out = text.replace("<s>", "").replace("</s>", "")
    while True:
        start = out.find("<")
        if start < 0:
            return out
        end = out.find(">", start)
        if end < 0:
            return out
        out = out[:start] + out[end + 1:]


class CFXCaptionClean:
    """Clean a generated caption: control tokens, whitespace, duplicate tags, length."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True}),
                "strip_tokens": ("BOOLEAN", {"default": True}),
                "collapse_whitespace": ("BOOLEAN", {"default": True}),
                "dedupe_tags": ("BOOLEAN", {"default": False}),
                "delimiter": ("STRING", {"default": ", "}),
                "max_chars": ("INT", {"default": 0, "min": 0, "max": 100000}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Vision/Text"

    def run(self, text, strip_tokens=True, collapse_whitespace=True, dedupe_tags=False,
            delimiter=", ", max_chars=0):
        result = text or ""
        if strip_tokens:
            result = _strip_control_tokens(result)
        if collapse_whitespace:
            result = " ".join(result.split())
        if dedupe_tags:
            seen = set()
            tags = []
            for part in result.split(delimiter.strip() or ","):
                tag = part.strip()
                if tag and tag not in seen:
                    seen.add(tag)
                    tags.append(tag)
            result = delimiter.join(tags)
        result = result.strip()
        if max_chars > 0 and len(result) > max_chars:
            cut = result[:max_chars]
            if delimiter in cut:
                cut = cut.rsplit(delimiter, 1)[0]
            result = cut
        return (result,)


NODE_CLASS_MAPPINGS = {
    "comfyui_vision_caption_clean": CFXCaptionClean,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_vision_caption_clean": "ComfyUI-Vision · Caption Clean",
}
