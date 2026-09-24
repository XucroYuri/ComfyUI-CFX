"""Generic VLM caption helpers (native transformers, no trust_remote_code).

The node surface and implementation here are original. The copyleft-licensed
``ComfyUI-QwenVL`` plugin is deliberately not used or copied; users who want its
extra features install it separately.
"""

VLM_MODELS = (
    "Qwen/Qwen2.5-VL-3B-Instruct",
    "Qwen/Qwen2.5-VL-7B-Instruct",
    "Qwen/Qwen3-VL-4B-Instruct",
    "Qwen/Qwen3-VL-8B-Instruct",
)

_CACHE = {}


def build_messages(prompt: str) -> list:
    """Chat messages with one image followed by the instruction."""
    return [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt},
            ],
        }
    ]


def load(model: str, dtype):
    """Load (and cache) a processor + model for ``model``."""
    key = model
    if key not in _CACHE:
        from transformers import AutoModelForImageTextToText, AutoProcessor

        from ...core.device import compute_device

        processor = AutoProcessor.from_pretrained(model)
        network = AutoModelForImageTextToText.from_pretrained(model, dtype=dtype)
        _CACHE[key] = (processor, network.to(compute_device()))
    return _CACHE[key]
