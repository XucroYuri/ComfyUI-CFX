"""Adapter to the MIT-licensed RetinaFace backend shipped with ComfyUI-AutoCropFaces."""

import importlib.util
import os
import sys

import folder_paths

BACKEND_NODE = "ComfyUI-AutoCropFaces"
BACKEND_PACKAGE = "cfx_autocropfaces_backend"


def custom_nodes_dir() -> str:
    override = os.environ.get("CFX_FACECROP_DIR")
    if override:
        return os.path.abspath(override)
    base = getattr(folder_paths, "base_path", None)
    if base:
        return os.path.join(base, "custom_nodes")
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))


def backend_dir() -> str:
    return os.path.join(custom_nodes_dir(), BACKEND_NODE)


def backend_module():
    init_path = os.path.join(backend_dir(), "__init__.py")
    if not os.path.isfile(init_path):
        raise FileNotFoundError(
            f"cfx-segment needs '{BACKEND_NODE}' installed under {custom_nodes_dir()}; not found: {init_path}"
        )
    if BACKEND_PACKAGE not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            BACKEND_PACKAGE, init_path, submodule_search_locations=[backend_dir()]
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[BACKEND_PACKAGE] = module
        spec.loader.exec_module(module)
    return sys.modules[BACKEND_PACKAGE]


def auto_crop_faces(**kwargs):
    return backend_module().AutoCropFaces().auto_crop_faces(**kwargs)
