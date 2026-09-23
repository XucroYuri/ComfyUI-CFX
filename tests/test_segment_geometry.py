import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment import geometry, registry


def test_boxes_to_mask_fills_region():
    mask = geometry.boxes_to_mask([[1, 1, 3, 3]], 5, 5)
    assert mask.shape == (5, 5)
    assert mask[2, 2] == 1.0
    assert mask[0, 0] == 0.0


def test_boxes_to_mask_normalizes_reversed_box():
    mask = geometry.boxes_to_mask([[3, 3, 1, 1]], 5, 5)
    assert mask[2, 2] == 1.0


def test_boxes_to_mask_outline_only():
    mask = geometry.boxes_to_mask([[1, 1, 3, 3]], 5, 5, line_width=1)
    assert mask[1, 1] == 1.0
    assert mask[2, 2] == 0.0


def test_polygons_to_mask_fills():
    mask = geometry.polygons_to_mask([[[1, 1], [4, 1], [4, 4], [1, 4]]], 5, 5)
    assert mask[2, 2] == 1.0
    assert mask[0, 0] == 0.0


def test_polygon_with_too_few_points_is_skipped():
    mask = geometry.polygons_to_mask([[[0, 0], [1, 1]]], 4, 4)
    assert mask.sum() == 0.0


def test_annotations_prefers_polygons():
    annotations = {"polygons": [[[0, 0], [3, 0], [3, 3], [0, 3]]], "bboxes": [[4, 4, 5, 5]]}
    mask = geometry.annotations_to_mask(annotations, 5, 5)
    assert mask[1, 1] == 1.0
    assert mask[4, 4] == 0.0


def test_annotations_requires_geometry():
    with pytest.raises(ValueError):
        geometry.annotations_to_mask({}, 5, 5)


def test_family_dir_is_under_project_root():
    assert registry.family_dir("sam2").replace("\\", "/").endswith("cfx-segment/sam2")


def test_unknown_family_raises():
    with pytest.raises(ValueError):
        registry.family_dir("nope")


def test_cache_key_defaults():
    assert registry.cache_key("sam2", "/models/x") == ("sam2", "/models/x", "fp16")
