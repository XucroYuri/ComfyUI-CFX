import os

import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment import face_backend
from comfyui_cfx.packages.segment.nodes import face as face_node


def test_backend_dir_points_at_autocropfaces():
    assert face_backend.backend_dir().endswith("ComfyUI-AutoCropFaces")


def test_backend_env_override(monkeypatch):
    monkeypatch.setenv("CFX_FACECROP_DIR", "X:/nodes")
    assert face_backend.backend_dir().replace("\\", "/") == "X:/nodes/ComfyUI-AutoCropFaces"


def test_missing_backend_raises(monkeypatch):
    monkeypatch.setenv("CFX_FACECROP_DIR", "Z:/definitely/missing")
    with pytest.raises(FileNotFoundError):
        face_backend.backend_module()


def test_input_types_expose_aspect_ratios():
    required = face_node.CFXFaceCrop.INPUT_TYPES()["required"]
    assert required["aspect_ratio"][0][0] == "9:16"
    assert required["number_of_faces"][1]["default"] == 5


def test_real_backend_exposes_node():
    if not os.path.isdir(face_backend.backend_dir()):
        pytest.skip("AutoCropFaces not installed")
    module = face_backend.backend_module()
    assert "AutoCropFaces" in module.NODE_CLASS_MAPPINGS
