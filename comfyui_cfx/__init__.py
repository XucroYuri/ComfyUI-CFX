"""ComfyUI-CFX aggregated node mappings.

Every domain package under ``packages/`` exposes ``NODE_CLASS_MAPPINGS`` and
``NODE_DISPLAY_NAME_MAPPINGS``; this module merges them and fails loudly on
duplicate node ids.
"""

from .packages import (
    audio,
    controlnet,
    depth3d,
    filter,
    flow,
    flux,
    inpaint,
    loaders,
    primitives,
    resolve,
    sampling,
    segment,
    video,
    vision,
)

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for _package in (
    primitives,
    flow,
    vision,
    segment,
    resolve,
    controlnet,
    inpaint,
    depth3d,
    sampling,
    video,
    flux,
    audio,
    loaders,
    filter,
):
    _duplicates = NODE_CLASS_MAPPINGS.keys() & _package.NODE_CLASS_MAPPINGS.keys()
    if _duplicates:
        raise RuntimeError(f"duplicate node ids across packages: {sorted(_duplicates)}")
    NODE_CLASS_MAPPINGS.update(_package.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(_package.NODE_DISPLAY_NAME_MAPPINGS)

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
