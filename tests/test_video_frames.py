import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.video.nodes import frames as frames_node

node = frames_node.CFXFrameRange()


def make_batch(batch=8, height=4, width=5, channels=3):
    index = torch.arange(batch, dtype=torch.float32).reshape(batch, 1, 1, 1)
    return index.expand(batch, height, width, channels).contiguous()


def frame_ids(image):
    return image[:, 0, 0, 0].tolist()


def test_middle_slice():
    out = node.run(make_batch(), 2, 6, 1)[0]
    assert frame_ids(out) == [2, 3, 4, 5]


def test_stop_minus_one_selects_to_end():
    out = node.run(make_batch(), 5, -1, 1)[0]
    assert frame_ids(out) == [5, 6, 7]


def test_step_two():
    out = node.run(make_batch(), 0, 8, 2)[0]
    assert frame_ids(out) == [0, 2, 4, 6]


def test_stop_beyond_batch_clamps():
    out = node.run(make_batch(), 1, 100, 1)[0]
    assert frame_ids(out) == [1, 2, 3, 4, 5, 6, 7]


def test_empty_range_raises():
    with pytest.raises(ValueError, match="empty range"):
        node.run(make_batch(), 5, 3, 1)
    with pytest.raises(ValueError, match="empty range"):
        node.run(make_batch(), 4, 4, 1)


def test_output_shape_bhwc():
    out = node.run(make_batch(), 0, 6, 2)[0]
    assert out.shape == (3, 4, 5, 3)
    assert out.dim() == 4
