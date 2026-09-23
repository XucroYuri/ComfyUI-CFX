"""Pytest bootstrap.

Expose the repo as the importable package ``comfyui_cfx`` without executing
``comfyui_cfx/__init__.py`` — that aggregator imports every node package (and thus
ComfyUI), which would make even the pure ``core`` tests depend on ComfyUI.
"""

import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "comfyui_cfx"

if "comfyui_cfx" not in sys.modules:
    package = types.ModuleType("comfyui_cfx")
    package.__path__ = [str(PACKAGE)]
    # The repo-root shim does ``from comfyui_cfx import NODE_CLASS_MAPPINGS`` when
    # pytest imports it during Package collection; satisfy that without loading the
    # heavy aggregator (which would pull in ComfyUI).
    package.NODE_CLASS_MAPPINGS = {}
    package.NODE_DISPLAY_NAME_MAPPINGS = {}
    sys.modules["comfyui_cfx"] = package
