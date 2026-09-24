"""Read a GGUF v2/v3 header (header only, never the weight payload)."""

import struct

import folder_paths

from ....core.paths import safe_join

MAGIC = b"GGUF"
HEADER_SIZE = 4 + 4 + 8 + 8


class CFXGgufHeader:
    """Parse magic/version/tensor_count/metadata_kv_count from a GGUF file."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("JSON",)
    RETURN_NAMES = ("info",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Loaders/Quant"

    def run(self, path):
        target = safe_join(folder_paths.models_dir, path)
        with open(target, "rb") as handle:
            header = handle.read(HEADER_SIZE)

        if len(header) < 4 or header[:4] != MAGIC:
            raise ValueError("not a GGUF file")
        if len(header) < HEADER_SIZE:
            raise ValueError("truncated GGUF header")

        version = struct.unpack("<I", header[4:8])[0]
        tensor_count = struct.unpack("<Q", header[8:16])[0]
        metadata_kv_count = struct.unpack("<Q", header[16:24])[0]
        return (
            {
                "magic": "GGUF",
                "version": version,
                "tensor_count": tensor_count,
                "metadata_kv_count": metadata_kv_count,
            },
        )


NODE_CLASS_MAPPINGS = {
    "comfyui_loaders_gguf_header": CFXGgufHeader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_loaders_gguf_header": "ComfyUI-Loaders · GGUF Header",
}
