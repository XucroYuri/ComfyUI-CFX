import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.flow.nodes import constrain_image as constrain_node

node = constrain_node.CFXConstrainImage()


def test_small_image_is_not_upscaled():
    out, width, height = node.run(torch.rand(1, 64, 64, 3), 1024, 1024, False)
    assert (width, height) == (64, 64)
    assert out.shape == (1, 64, 64, 3)


def test_wide_image_fits_within_box():
    out, width, height = node.run(torch.rand(1, 512, 1024, 3), 512, 512, False)
    assert (width, height) == (512, 256)
    assert out.shape == (1, 256, 512, 3)


def test_crop_covers_target_box():
    out, width, height = node.run(torch.rand(1, 256, 512, 3), 256, 256, True)
    assert (width, height) == (256, 256)
    assert out.shape == (1, 256, 256, 3)


def test_crop_upscales_small_image_to_box():
    out, width, height = node.run(torch.rand(1, 64, 64, 3), 256, 256, True)
    assert (width, height) == (256, 256)
