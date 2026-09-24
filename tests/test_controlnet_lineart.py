import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("cv2")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.controlnet.nodes import lineart as lineart_node

node = lineart_node.CFXLineartPreprocessor()


def _rectangle_image(size=64, square=16):
    """White background with a centered black filled rectangle."""
    image = torch.ones(1, size, size, 3)
    start = (size - square) // 2
    image[:, start:start + square, start:start + square, :] = 0.0
    return image


def test_output_shapes():
    out_image, out_mask = node.run(_rectangle_image())
    assert out_image.shape == (1, 64, 64, 3)
    assert out_mask.shape == (1, 64, 64)


def test_rectangle_has_line_pixels():
    _, out_mask = node.run(_rectangle_image())
    assert float(out_mask.sum()) > 0.0


def test_invert_changes_output():
    _, lines = node.run(_rectangle_image(), invert=True)
    _, dark = node.run(_rectangle_image(), invert=False)
    assert not torch.equal(lines, dark)
    assert torch.allclose(lines + dark, torch.ones_like(lines))


def test_even_block_size_raises():
    with pytest.raises(ValueError):
        node.run(_rectangle_image(), block_size=10)


def test_block_size_below_three_raises():
    with pytest.raises(ValueError):
        node.run(_rectangle_image(), block_size=1)


def test_output_range_within_unit_interval():
    out_image, out_mask = node.run(_rectangle_image())
    assert float(out_image.min()) >= 0.0
    assert float(out_image.max()) <= 1.0
    assert float(out_mask.min()) >= 0.0
    assert float(out_mask.max()) <= 1.0
