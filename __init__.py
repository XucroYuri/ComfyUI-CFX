"""ComfyUI plugin entry point.

Keeps ComfyUI's custom-node contract (``__init__.py`` at the repo root) while all
real code lives in the importable ``comfyui_cfx`` package.
"""

import os
import sys

_REPO = os.path.dirname(os.path.abspath(__file__))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from comfyui_cfx import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS  # noqa: E402

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
