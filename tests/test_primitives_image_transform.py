import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import transform as transform_node

node = transform_node.CFXImageTransform()


def test_rotate90_swaps_dimensions():
    out = node.apply(torch.rand(1, 8, 4, 3), "rotate90")[0]
    assert out.shape == (1, 4, 8, 3)


def test_four_rotations_restore_original():
    original = torch.rand(2, 5, 7, 3)
    out = original
    for _ in range(4):
        out = node.apply(out, "rotate90")[0]
    assert torch.equal(out, original)


def test_flip_axes_differ():
    original = torch.rand(1, 4, 6, 3)
    assert torch.equal(node.apply(original, "flip_h")[0], torch.flip(original, dims=(2,)))
    assert torch.equal(node.apply(original, "flip_v")[0], torch.flip(original, dims=(1,)))


def test_transpose_swaps_wh():
    out = node.apply(torch.rand(1, 4, 6, 3), "transpose")[0]
    assert out.shape == (1, 6, 4, 3)


def test_unknown_operation_raises():
    with pytest.raises(ValueError):
        node.apply(torch.rand(1, 4, 4, 3), "spin")
