import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("cv2")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.controlnet.nodes import canny as canny_node

node = canny_node.CFXCannyPreprocessor()


def _square_image(size=64, square=16):
    image = torch.zeros(1, size, size, 3)
    start = (size - square) // 2
    image[:, start:start + square, start:start + square, :] = 1.0
    return image


def test_output_shapes():
    out_image, out_mask = node.run(_square_image(), low_threshold=50.0, high_threshold=150.0)
    assert out_image.shape == (1, 64, 64, 3)
    assert out_mask.shape == (1, 64, 64)


def test_white_square_has_edges():
    _, out_mask = node.run(_square_image(), low_threshold=50.0, high_threshold=150.0)
    assert float(out_mask.sum()) > 0.0


def test_higher_thresholds_do_not_add_edges():
    _, low_mask = node.run(_square_image(), low_threshold=10.0, high_threshold=20.0)
    _, high_mask = node.run(_square_image(), low_threshold=100.0, high_threshold=200.0)
    assert int((high_mask > 0.0).sum()) <= int((low_mask > 0.0).sum())


def test_high_below_low_raises():
    with pytest.raises(ValueError):
        node.run(_square_image(), low_threshold=200.0, high_threshold=100.0)


def test_output_range_within_unit_interval():
    out_image, out_mask = node.run(_square_image(), low_threshold=50.0, high_threshold=150.0)
    assert float(out_image.min()) >= 0.0
    assert float(out_image.max()) <= 1.0
    assert float(out_mask.min()) >= 0.0
    assert float(out_mask.max()) <= 1.0
