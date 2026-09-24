import numpy as np
import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment import geometry
from comfyui_cfx.packages.segment.nodes import mask_to_bbox as mask_to_bbox_node

node = mask_to_bbox_node.CFXMaskToBBox()


def _empty(batch=1, height=10, width=10):
    return np.zeros((batch, height, width), dtype=np.float32)


def test_known_rectangle_bbox_and_area():
    mask = _empty()
    mask[0, 2:5, 3:7] = 1.0
    assert geometry.mask_to_bboxes(mask) == [{"bbox": [3, 2, 7, 5], "area": 12}]


def test_multiple_of_aligns_outward():
    mask = _empty(height=16, width=16)
    mask[0, 2:4, 3:6] = 1.0
    boxes = geometry.mask_to_bboxes(mask, multiple_of=4)
    assert boxes[0]["bbox"] == [0, 0, 8, 4]


def test_border_touching_mask_clamps():
    mask = _empty()
    mask[0, 0, 0] = 1.0
    mask[0, 9, 9] = 1.0
    boxes = geometry.mask_to_bboxes(mask, multiple_of=16)
    assert boxes[0]["bbox"] == [0, 0, 10, 10]


def test_empty_mask_yields_no_entries_and_summary():
    mask = _empty()
    assert geometry.mask_to_bboxes(mask) == []
    bboxes, summary = node.run(torch.from_numpy(mask))
    assert bboxes == []
    assert summary == "0 box(es)"


def test_2d_mask_is_accepted():
    mask = torch.zeros(6, 6)
    mask[1:3, 2:5] = 1.0
    bboxes, summary = node.run(mask)
    assert bboxes == [{"bbox": [2, 1, 5, 3], "area": 6}]
    assert summary == "1 box(es); first: [2, 1, 5, 3]"


def test_threshold_filters_low_values():
    mask = _empty(height=4, width=4)
    mask[0, 1, 1] = 0.3
    mask[0, 2, 2] = 0.9
    assert geometry.mask_to_bboxes(mask, threshold=0.5) == [{"bbox": [2, 2, 3, 3], "area": 1}]
    assert geometry.mask_to_bboxes(mask, threshold=0.1) == [{"bbox": [1, 1, 3, 3], "area": 4}]


def test_two_batch_items_produce_two_entries():
    mask = _empty(batch=2)
    mask[0, 1:3, 1:3] = 1.0
    mask[1, 5:8, 6:9] = 1.0
    boxes = geometry.mask_to_bboxes(mask)
    assert len(boxes) == 2
    assert boxes[0]["bbox"] == [1, 1, 3, 3]
    assert boxes[1]["bbox"] == [6, 5, 9, 8]
