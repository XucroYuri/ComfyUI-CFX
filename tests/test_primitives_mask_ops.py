import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import mask as mask_node

node = mask_node.CFXMaskOps()


def test_threshold_binarizes():
    mask = torch.tensor([[[0.2, 0.8], [0.6, 0.1]]])
    out = node.run(mask, threshold=0.5)[0]
    assert out.tolist() == [[[0.0, 1.0], [1.0, 0.0]]]


def test_invert():
    mask = torch.tensor([[[0.2, 0.8], [0.6, 0.1]]])
    out = node.run(mask, invert=True)[0]
    assert torch.allclose(out, 1.0 - mask)


def test_grow_single_pixel():
    mask = torch.zeros(1, 7, 7)
    mask[0, 3, 3] = 1.0
    out = node.run(mask, grow=1)[0]
    assert float(out.sum()) == 9.0


def test_shrink_block():
    mask = torch.zeros(1, 7, 7)
    mask[:, 1:6, 1:6] = 1.0
    out = node.run(mask, shrink=1)[0]
    assert float(out.sum()) == 9.0


def test_fill_holes_on_ring():
    mask = torch.zeros(1, 9, 9)
    mask[:, 2, 2:7] = 1.0
    mask[:, 6, 2:7] = 1.0
    mask[:, 2:7, 2] = 1.0
    mask[:, 2:7, 6] = 1.0
    out = node.run(mask, fill_holes=True)[0]
    assert float(out[0, 4, 4]) == 1.0


def test_blur_preserves_mass_and_bounds():
    mask = torch.zeros(1, 9, 9)
    mask[0, 4, 4] = 1.0
    out = node.run(mask, blur=2)[0]
    assert abs(float(out.sum()) - 1.0) < 1e-3
    assert float(out.max()) < 1.0


def test_2d_input_is_promoted():
    out = node.run(torch.zeros(4, 4), invert=True)[0]
    assert out.shape == (1, 4, 4)
    assert float(out.sum()) == 16.0


def test_bad_shape_raises():
    with pytest.raises(ValueError):
        node.run(torch.zeros(1, 1, 4, 4))
