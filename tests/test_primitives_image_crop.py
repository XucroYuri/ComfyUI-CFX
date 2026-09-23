import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import crop as crop_node

node = crop_node.CFXImageCrop()


def test_pixel_crop_shape_and_size():
    out, width, height = node.crop(torch.rand(1, 64, 64, 3), "pixel", x=10, y=20, width=30, height=40)
    assert (width, height) == (30, 40)
    assert out.shape == (1, 40, 30, 3)


def test_zero_size_goes_to_edge():
    _, width, height = node.crop(torch.rand(1, 64, 48, 3), "pixel", x=8, y=8)
    assert (width, height) == (40, 56)


def test_out_of_range_is_clamped():
    _, width, height = node.crop(torch.rand(1, 64, 64, 3), "pixel", x=1000, y=1000)
    assert (width, height) == (1, 1)


def test_inset_pixels():
    _, width, height = node.crop(torch.rand(1, 64, 64, 3), "inset", left=10, right=10, top=5, bottom=5)
    assert (width, height) == (44, 54)


def test_inset_percent():
    _, width, height = node.crop(
        torch.rand(1, 100, 200, 3), "inset", left=10, right=10, top=25, bottom=25, inset_unit="percent"
    )
    assert (width, height) == (160, 50)


def test_inset_larger_than_image_keeps_one_pixel():
    _, width, height = node.crop(torch.rand(1, 32, 32, 3), "inset", left=100, right=100, top=100, bottom=100)
    assert width >= 1 and height >= 1
