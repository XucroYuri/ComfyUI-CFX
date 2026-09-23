"""Tag filtering primitive."""


class CFXTagsFilter:
    """Filter a tag string by include/exclude substrings with dedupe and limit."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tags": ("STRING", {"default": "", "multiline": True}),
                "include": ("STRING", {"default": ""}),
                "exclude": ("STRING", {"default": ""}),
                "delimiter": ("STRING", {"default": ", "}),
                "case_sensitive": ("BOOLEAN", {"default": False}),
                "max_tags": ("INT", {"default": 0, "min": 0, "max": 4096}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tags",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Vision/Text"

    def run(self, tags, include="", exclude="", delimiter=", ", case_sensitive=False, max_tags=0):
        include_list = _split_list(include, case_sensitive)
        exclude_list = _split_list(exclude, case_sensitive)

        seen = set()
        kept = []
        for part in (tags or "").split(delimiter.strip() or ","):
            tag = part.strip()
            if not tag:
                continue
            key = tag if case_sensitive else tag.lower()
            if key in seen:
                continue
            if include_list and not any(item in key for item in include_list):
                continue
            if exclude_list and any(item in key for item in exclude_list):
                continue
            seen.add(key)
            kept.append(tag)

        if max_tags > 0:
            kept = kept[:max_tags]
        return (delimiter.join(kept),)


def _split_list(value: str, case_sensitive: bool) -> list:
    items = [item.strip() for item in (value or "").split(",") if item.strip()]
    return items if case_sensitive else [item.lower() for item in items]


NODE_CLASS_MAPPINGS = {
    "comfyui_vision_tags_filter": CFXTagsFilter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_vision_tags_filter": "ComfyUI-Vision · Tags Filter",
}
