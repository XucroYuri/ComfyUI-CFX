import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import resolution as resolution_node

node = resolution_node.CFXResolution()


def test_square_one_megapixel():
    assert node.compute("1:1", 1.0, "landscape", 8) == (1000, 1000)


def test_ratio_is_preserved():
    width, height = node.compute("16:9", 1.0, "landscape", 8)
    assert abs(width / height - 16 / 9) < 0.02


def test_portrait_swaps_sides():
    landscape = node.compute("16:9", 1.0, "landscape", 8)
    portrait = node.compute("16:9", 1.0, "portrait", 8)
    assert landscape[0] > landscape[1]
    assert portrait[0] < portrait[1]


def test_width_override_derives_height():
    width, height = node.compute("1:1", 1.0, "landscape", 8, width_override=512)
    assert (width, height) == (512, 512)


def test_multiple_of_alignment():
    width, height = node.compute("16:9", 1.0, "landscape", 64)
    assert width % 64 == 0 and height % 64 == 0


def test_tiny_megapixels_never_zero():
    width, height = node.compute("3:2", 0.000001, "landscape", 8)
    assert width >= 8 and height >= 8
