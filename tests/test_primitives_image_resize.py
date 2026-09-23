import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import image as image_node

node = image_node.CFXImageResize()


def test_scale_by_keeps_ratio():
    out, width, height = node.resize(torch.rand(1, 64, 32, 3), "stretch", scale_by=2.0, multiple_of=1)
    assert (width, height) == (64, 128)
    assert out.shape == (1, 128, 64, 3)


def test_stretch_to_exact_size():
    out, width, height = node.resize(torch.rand(1, 64, 32, 3), "stretch", width=100, height=50, multiple_of=1)
    assert (width, height) == (100, 50)
    assert out.shape == (1, 50, 100, 3)


def test_single_side_keeps_ratio():
    _, width, height = node.resize(torch.rand(1, 64, 32, 3), "stretch", height=128, multiple_of=1)
    assert (width, height) == (64, 128)


def test_multiple_of_alignment():
    _, width, height = node.resize(torch.rand(1, 64, 33, 3), "stretch", scale_by=1.1, multiple_of=8)
    assert width % 8 == 0 and height % 8 == 0


def test_target_megapixels():
    _, width, height = node.resize(torch.rand(1, 100, 100, 3), "stretch", target_megapixels=0.25, multiple_of=1)
    assert abs(width * height - 250_000) < 5_000


def test_crop_matches_target_and_keeps_batch():
    out, width, height = node.resize(torch.rand(2, 32, 64, 3), "crop", width=64, height=64, multiple_of=1)
    assert (width, height) == (64, 64)
    assert out.shape == (2, 64, 64, 3)


def test_pad_letterbox_uses_pad_color():
    out, width, height = node.resize(torch.ones(1, 32, 64, 3), "pad", width=64, height=64, multiple_of=1, pad_color=0.0)
    assert (width, height) == (64, 64)
    assert float(out[0, 0, 0, 0]) == 0.0
    assert float(out[0, 32, 32, 0]) == 1.0


def test_no_size_source_raises():
    with pytest.raises(ValueError):
        node.resize(torch.rand(1, 8, 8, 3), "stretch")


def test_tiny_megapixels_never_zero():
    _, width, height = node.resize(torch.rand(1, 64, 64, 3), "stretch", target_megapixels=1e-6, multiple_of=8)
    assert width >= 8 and height >= 8


def test_multiple_of_larger_than_image():
    _, width, height = node.resize(torch.rand(1, 4, 4, 3), "stretch", scale_by=1.0, multiple_of=64)
    assert width >= 64 and height >= 64
