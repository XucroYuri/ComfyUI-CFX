import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.inpaint.nodes import crop as crop_node

node = crop_node.CFXCropByMask()


def _rect_mask(height=64, width=64, y0=20, y1=30, x0=10, x1=25):
    mask = torch.zeros(1, height, width)
    mask[:, y0:y1, x0:x1] = 1.0
    return mask


def test_known_rectangle_box():
    image = torch.rand(1, 64, 64, 3)
    out_image, out_mask, data = node.run(image, _rect_mask(), padding=0, multiple_of=1)
    assert data["x"] == 10 and data["y"] == 20
    assert data["width"] == 15 and data["height"] == 10
    assert out_image.shape == (1, 10, 15, 3)
    assert out_mask.shape == (1, 10, 15)
    assert out_mask.sum().item() == 150


def test_padding_expands_box():
    image = torch.rand(1, 64, 64, 3)
    _, _, data = node.run(image, _rect_mask(), padding=4, multiple_of=1)
    assert (data["x"], data["y"]) == (6, 16)
    assert (data["width"], data["height"]) == (23, 18)


def test_multiple_of_alignment_outward():
    image = torch.rand(1, 64, 64, 3)
    _, _, data = node.run(image, _rect_mask(), padding=0, multiple_of=8)
    assert (data["x"], data["y"]) == (8, 16)
    assert (data["width"], data["height"]) == (24, 16)


def test_clamped_at_image_border():
    image = torch.rand(1, 32, 32, 3)
    mask = _rect_mask(height=32, width=32, y0=28, y1=32, x0=28, x1=32)
    _, _, data = node.run(image, mask, padding=8, multiple_of=1)
    assert (data["x"], data["y"]) == (20, 20)
    assert (data["width"], data["height"]) == (12, 12)


def test_padding_beyond_border_clamps_to_image():
    image = torch.rand(1, 32, 32, 3)
    mask = _rect_mask(height=32, width=32, y0=0, y1=4, x0=0, x1=4)
    _, _, data = node.run(image, mask, padding=64, multiple_of=8)
    assert (data["x"], data["y"]) == (0, 0)
    assert (data["width"], data["height"]) == (32, 32)


def test_empty_mask_raises():
    image = torch.rand(1, 64, 64, 3)
    with pytest.raises(ValueError, match="mask is empty"):
        node.run(image, torch.zeros(1, 64, 64), padding=8, multiple_of=8)


def test_crop_data_matches_tensor_shapes():
    image = torch.rand(1, 64, 64, 3)
    out_image, out_mask, data = node.run(image, _rect_mask(), padding=4, multiple_of=8)
    assert set(data) == {
        "x", "y", "width", "height", "original_width", "original_height",
    }
    assert data["original_width"] == 64 and data["original_height"] == 64
    assert out_image.shape == (1, data["height"], data["width"], 3)
    assert out_mask.shape == (1, data["height"], data["width"])


def test_mask_returns_batch_of_one():
    image = torch.rand(1, 64, 64, 3)
    _, out_mask, _ = node.run(image, _rect_mask(), padding=0, multiple_of=1)
    assert out_mask.dim() == 3 and out_mask.shape[0] == 1

    stacked = _rect_mask().repeat(3, 1, 1)
    _, out_mask_batched, _ = node.run(image, stacked, padding=0, multiple_of=1)
    assert out_mask_batched.dim() == 3 and out_mask_batched.shape[0] == 1
