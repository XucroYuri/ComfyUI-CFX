"""Load / save text files inside an allow-listed set of directories.

Roots default to ``<output>/text`` and can be overridden with the ``CFX_TEXT_DIRS``
environment variable (``os.pathsep`` separated).
"""

import os

import folder_paths


def roots():
    configured = os.environ.get("CFX_TEXT_DIRS", "")
    if configured:
        return [os.path.abspath(path) for path in configured.split(os.pathsep) if path]
    return [os.path.join(folder_paths.get_output_directory(), "text")]


def resolve(name: str) -> str:
    if not name or os.path.isabs(name):
        raise ValueError(f"text file: path must be relative, got {name!r}")
    for root in roots():
        try:
            candidate = os.path.abspath(os.path.join(root, name))
            if os.path.commonpath([root, candidate]) == root:
                return candidate
        except ValueError:
            continue
    raise ValueError("text file: path is outside the configured text directories")


class CFXLoadText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": "prompt.txt"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "load"
    CATEGORY = "ComfyUI-Flow/Text"

    def load(self, path):
        with open(resolve(path), encoding="utf-8") as handle:
            return (handle.read(),)


class CFXSaveText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True}),
                "path": ("STRING", {"default": "prompt.txt"}),
                "mode": (["overwrite", "append"], {"default": "overwrite"}),
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "save"
    CATEGORY = "ComfyUI-Flow/Text"

    def save(self, text, path, mode="overwrite"):
        target = resolve(path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "a" if mode == "append" else "w", encoding="utf-8") as handle:
            handle.write(text)
        return {"ui": {"text": [text]}}


NODE_CLASS_MAPPINGS = {
    "comfyui_flow_load_text": CFXLoadText,
    "comfyui_flow_save_text": CFXSaveText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_flow_load_text": "ComfyUI-Flow · Load Text",
    "comfyui_flow_save_text": "ComfyUI-Flow · Save Text",
}
