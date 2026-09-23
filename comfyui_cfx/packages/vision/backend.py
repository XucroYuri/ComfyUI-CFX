"""Adapter to the self-contained Florence-2 backend shipped with ComfyUI-Florence2.

The upstream backend implements Florence-2 on ``comfy.ops`` (no ``transformers``
remote code), which is why it is reused here instead of re-vendoring it.
"""

import os
import sys
import types

import folder_paths

BACKEND_NODE = "comfyui-florence2"
BACKEND_PACKAGE = "cfx_florence2_backend"


def custom_nodes_dir() -> str:
    override = os.environ.get("CFX_FLORENCE2_DIR")
    if override:
        return os.path.abspath(override)
    base = getattr(folder_paths, "base_path", None)
    if base:
        return os.path.join(base, "custom_nodes")
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))


def backend_dir() -> str:
    return os.path.join(custom_nodes_dir(), BACKEND_NODE)


def load_florence2(model_path: str, dtype):
    """Load a Florence-2 model through the upstream backend."""
    node_dir = backend_dir()
    if not os.path.isdir(node_dir):
        raise FileNotFoundError(
            f"cfx-vision needs '{BACKEND_NODE}' installed under {custom_nodes_dir()}; not found: {node_dir}"
        )
    if BACKEND_PACKAGE not in sys.modules:
        package = types.ModuleType(BACKEND_PACKAGE)
        package.__path__ = [node_dir]
        sys.modules[BACKEND_PACKAGE] = package
    from cfx_florence2_backend.nodes import load_florence2 as upstream_load

    return upstream_load(model_path, dtype)
