import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment import backend, geometry
from comfyui_cfx.packages.segment.nodes import sam2 as sam2_node


def test_annotations_to_box_batch_shape():
    batch = geometry.annotations_to_box_batch({"bboxes": [[1, 2, 3, 4], [5, 6, 7, 8]]})
    assert batch == [[[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]]]


def test_annotations_to_box_batch_requires_bboxes():
    with pytest.raises(ValueError):
        geometry.annotations_to_box_batch({"polygons": []})
    with pytest.raises(ValueError):
        geometry.annotations_to_box_batch("nope")


def test_backend_dir_points_at_sam2_node():
    assert backend.backend_dir().endswith("ComfyUI-segment-anything-2")


def test_backend_env_override(monkeypatch):
    monkeypatch.setenv("CFX_SAM2_DIR", "X:/nodes")
    assert backend.backend_dir().replace("\\", "/") == "X:/nodes/ComfyUI-segment-anything-2"


def test_missing_backend_raises(monkeypatch):
    monkeypatch.setenv("CFX_SAM2_DIR", "Z:/definitely/missing")
    with pytest.raises(FileNotFoundError):
        backend.load_sam2("m", "single_image", "fp32", "cpu")


def test_loader_input_types():
    required = sam2_node.CFXSAM2Loader.INPUT_TYPES()["required"]
    assert "sam2.1_hiera_large.safetensors" in required["model"][0]
    assert required["segmentor"][0] == ["single_image", "video"]


def test_mask_node_requires_annotations():
    required = sam2_node.CFXSAM2Mask.INPUT_TYPES()["required"]
    assert "annotations" in required
