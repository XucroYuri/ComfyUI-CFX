import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import json_access as json_node

node = json_node.CFXJsonBBox()


def test_bbox_returns_expected_ints_and_json():
    assert node.run({"bboxes": [[10, 20, 30, 40], [1, 2, 3, 4]]}, 1) == (
        1,
        2,
        3,
        4,
        {"bbox": [1, 2, 3, 4], "index": 1},
    )


def test_default_index_is_zero():
    assert node.run({"bboxes": [[10, 20, 30, 40]]}) == (10, 20, 30, 40, {"bbox": [10, 20, 30, 40], "index": 0})


def test_polygon_returns_enclosing_box():
    annotations = {"polygons": [[[10, 20], [30, 5], [15, 40]]]}
    assert node.run(annotations) == (10, 5, 30, 40, {"bbox": [10, 5, 30, 40], "index": 0})


def test_unsorted_bbox_is_normalized():
    assert node.run({"bboxes": [[80, 60, 20, 10]]}) == (20, 10, 80, 60, {"bbox": [20, 10, 80, 60], "index": 0})


def test_float_coords_are_rounded():
    assert node.run({"bboxes": [[1.4, 2.6, 9.2, 4.4]]}) == (1, 3, 9, 4, {"bbox": [1, 3, 9, 4], "index": 0})


def test_out_of_range_index_raises():
    with pytest.raises(ValueError, match="1 entry available"):
        node.run({"bboxes": [[1, 2, 3, 4]]}, 1)


def test_negative_index_raises():
    with pytest.raises(ValueError, match="2 entries available"):
        node.run({"bboxes": [[1, 2, 3, 4], [5, 6, 7, 8]]}, -1)


def test_missing_keys_raise():
    with pytest.raises(ValueError, match="0 entries available"):
        node.run({})


def test_bboxes_take_precedence_over_polygons():
    annotations = {"bboxes": [[1, 2, 3, 4]], "polygons": [[[9, 9], [8, 8]]]}
    assert node.run(annotations) == (1, 2, 3, 4, {"bbox": [1, 2, 3, 4], "index": 0})
