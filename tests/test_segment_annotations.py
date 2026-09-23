import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment.nodes import annotations as annotations_node

node = annotations_node.CFXAnnotationsToMask()


def test_mask_from_bboxes_uses_given_size():
    mask = node.run({"bboxes": [[1, 1, 3, 3]]}, width=5, height=5)[0]
    assert mask.shape == (1, 5, 5)
    assert float(mask[0, 2, 2]) == 1.0


def test_image_overrides_size():
    mask = node.run({"bboxes": [[0, 0, 8, 8]]}, image=torch.rand(1, 8, 6, 3))[0]
    assert mask.shape == (1, 8, 6)


def test_polygons_take_precedence():
    mask = node.run({"polygons": [[[0, 0], [2, 0], [2, 2], [0, 2]]], "bboxes": [[4, 4, 5, 5]]},
                    width=5, height=5)[0]
    assert float(mask[0, 1, 1]) == 1.0
    assert float(mask[0, 4, 4]) == 0.0


def test_invert():
    mask = node.run({"bboxes": [[0, 0, 2, 2]]}, width=4, height=4, invert=True)[0]
    assert float(mask[0, 3, 3]) == 1.0
    assert float(mask[0, 0, 0]) == 0.0


def test_missing_geometry_raises():
    with pytest.raises(ValueError):
        node.run({"labels": ["x"]}, width=4, height=4)
