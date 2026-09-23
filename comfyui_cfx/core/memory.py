"""GPU memory helpers.

Model lifetime is owned by ComfyUI's model management; these helpers only wrap the
standard release sequence so every cfx node frees the same way.
"""

import comfy.model_management as mm


def release(patcher):
    """Unload ``patcher`` and keep every other loaded model intact."""
    keep = [loaded for loaded in mm.current_loaded_models if loaded.model is not patcher]
    mm.free_memory(1e30, patcher.load_device, keep_loaded=keep)


def empty_cache():
    mm.soft_empty_cache()
