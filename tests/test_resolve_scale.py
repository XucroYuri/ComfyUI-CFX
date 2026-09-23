import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.resolve.nodes import scale as scale_node

node = scale_node.CFXScaleToMegapixels()


def test_one_megapixel_square():
    out, width, height = node.scale(torch.rand(1, 512, 512, 3), megapixels=1.0, multiple_of=8)
    assert (width, height) == (1000, 1000)
    assert out.shape == (1, 1000, 1000, 3)


def test_wide_image_keeps_aspect_ratio():
    out, width, height = node.scale(torch.rand(1, 400, 800, 3), megapixels=1.0, multiple_of=1)
    assert abs(width / height - 2.0) < 0.01
    assert out.shape == (1, height, width, 3)


def test_multiple_of_64_alignment():
    _, width, height = node.scale(torch.rand(1, 360, 640, 3), megapixels=1.0, multiple_of=64)
    assert width % 64 == 0 and height % 64 == 0


def test_shape_matches_returned_size():
    out, width, height = node.scale(torch.rand(2, 300, 500, 3), megapixels=0.5, multiple_of=16)
    assert out.shape == (2, height, width, 3)


def test_tiny_megapixels_never_zero():
    _, width, height = node.scale(torch.rand(1, 64, 64, 3), megapixels=0.0001, multiple_of=8)
    assert width >= 8 and height >= 8
