import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import stitch as stitch_node

node = stitch_node.CFXImageStitch()


def test_horizontal_stitch():
    out = node.stitch("horizontal", image1=torch.rand(1, 8, 4, 3), image2=torch.rand(1, 8, 6, 3))[0]
    assert out.shape == (1, 8, 10, 3)


def test_vertical_stitch():
    out = node.stitch("vertical", image1=torch.rand(1, 4, 8, 3), image2=torch.rand(1, 6, 8, 3))[0]
    assert out.shape == (1, 10, 8, 3)


def test_spacing_adds_gap_and_background():
    out = node.stitch("horizontal", spacing=2, background=0.0,
                      image1=torch.ones(1, 8, 4, 3), image2=torch.ones(1, 8, 6, 3))[0]
    assert out.shape == (1, 8, 12, 3)
    assert float(out[0, 0, 4, 0]) == 0.0


def test_single_image_passthrough():
    only = torch.rand(1, 4, 4, 3)
    out = node.stitch("horizontal", image1=only)[0]
    assert torch.equal(out, only)


def test_no_input_raises():
    with pytest.raises(ValueError):
        node.stitch("horizontal")


def test_height_mismatch_raises():
    with pytest.raises(ValueError):
        node.stitch("horizontal", image1=torch.rand(1, 4, 4, 3), image2=torch.rand(1, 5, 4, 3))


def test_batch_mismatch_raises():
    with pytest.raises(ValueError):
        node.stitch("horizontal", image1=torch.rand(1, 4, 4, 3), image2=torch.rand(2, 4, 4, 3))
