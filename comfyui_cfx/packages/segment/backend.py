"""Adapter to the Apache-2.0 SAM2 backend shipped with ComfyUI-segment-anything-2.

Reusing one upstream implementation keeps a single SAM2 copy in the stack instead
of vendoring another one.
"""

import os
import sys
import types

import folder_paths

BACKEND_NODE = "ComfyUI-segment-anything-2"
BACKEND_PACKAGE = "cfx_sam2_backend"


def custom_nodes_dir() -> str:
    override = os.environ.get("CFX_SAM2_DIR")
    if override:
        return os.path.abspath(override)
    base = getattr(folder_paths, "base_path", None)
    if base:
        return os.path.join(base, "custom_nodes")
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))


def backend_dir() -> str:
    return os.path.join(custom_nodes_dir(), BACKEND_NODE)


def _nodes():
    node_dir = backend_dir()
    if not os.path.isdir(node_dir):
        raise FileNotFoundError(
            f"cfx-segment needs '{BACKEND_NODE}' installed under {custom_nodes_dir()}; not found: {node_dir}"
        )
    if BACKEND_PACKAGE not in sys.modules:
        package = types.ModuleType(BACKEND_PACKAGE)
        package.__path__ = [node_dir]
        sys.modules[BACKEND_PACKAGE] = package
    from cfx_sam2_backend import nodes

    return nodes


def load_sam2(model: str, segmentor: str, precision: str, device: str):
    return _nodes().DownloadAndLoadSAM2Model().loadmodel(
        model=model, segmentor=segmentor, precision=precision, device=device
    )


def segment(sam2_model: dict, image, bboxes=None, keep_model_loaded: bool = False):
    return _nodes().Sam2Segmentation().segment(
        image=image, sam2_model=sam2_model, keep_model_loaded=keep_model_loaded, bboxes=bboxes
    )


def segment_points(sam2_model: dict, image, positive: str, negative=None, keep_model_loaded: bool = False):
    return _nodes().Sam2Segmentation().segment(
        image=image,
        sam2_model=sam2_model,
        keep_model_loaded=keep_model_loaded,
        coordinates_positive=positive,
        coordinates_negative=negative,
    )
