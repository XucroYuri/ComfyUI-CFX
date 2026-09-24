import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.inpaint.nodes import ratio as ratio_node

node = ratio_node.CFXOutpaintToRatio()

H, W, C = 32, 32, 3


def _inputs():
    return torch.rand(1, H, W, C), torch.rand(1, H, W)


def test_wide_ratio_grows_width_only():
    image, mask = _inputs()
    out_image, out_mask = node.run(image, mask, ratio="16:9")
    assert out_image.shape[0] == 1
    assert out_image.shape[1] == H
    assert out_image.shape[2] > W
    assert out_image.shape[3] == C
    assert out_mask.shape == (1, out_image.shape[1], out_image.shape[2])


def test_tall_ratio_grows_height_only():
    image, mask = _inputs()
    out_image, out_mask = node.run(image, mask, ratio="9:16")
    assert out_image.shape[1] > H
    assert out_image.shape[2] == W
    assert out_mask.shape == (1, out_image.shape[1], out_image.shape[2])


def test_output_shape_matches_returned_mask_shape():
    image, mask = _inputs()
    out_image, out_mask = node.run(image, mask, ratio="3:2")
    assert out_image.shape[1:3] == out_mask.shape[1:3]


def test_border_mask_is_one_and_centre_matches_input():
    image, mask = _inputs()
    out_image, out_mask = node.run(image, mask, ratio="16:9", anchor="center")
    new_h, new_w = out_image.shape[1], out_image.shape[2]
    offset_y = (new_h - H) // 2
    offset_x = (new_w - W) // 2

    assert torch.all(out_mask[:, :offset_y, :] == 1.0)
    assert torch.all(out_mask[:, offset_y + H:, :] == 1.0)
    assert torch.all(out_mask[:, offset_y:offset_y + H, :offset_x] == 1.0)
    assert torch.all(out_mask[:, offset_y:offset_y + H, offset_x + W:] == 1.0)
    assert torch.allclose(out_mask[:, offset_y:offset_y + H, offset_x:offset_x + W], mask.clamp(0.0, 1.0))


def test_start_anchor_places_image_top_left():
    image, mask = _inputs()
    out_image, out_mask = node.run(image, mask, ratio="16:9", anchor="start", fill=0.25)
    new_w = out_image.shape[2]

    assert torch.equal(out_image[:, :H, :W, :], image)
    assert torch.all(out_image[:, :, W:, :] == 0.25)
    assert torch.all(out_mask[:, :, W:] == 1.0)
    assert new_w > W


def test_end_anchor_places_image_bottom_right():
    image, mask = _inputs()
    out_image, out_mask = node.run(image, mask, ratio="16:9", anchor="end", fill=0.25)
    new_w = out_image.shape[2]

    assert torch.equal(out_image[:, :, new_w - W:, :], image)
    assert torch.all(out_image[:, :, :new_w - W, :] == 0.25)
    assert torch.all(out_mask[:, :, :new_w - W] == 1.0)


def test_exact_match_ratio_returns_unchanged():
    image, mask = _inputs()
    out_image, out_mask = node.run(image, mask, ratio="1:1")
    assert torch.equal(out_image, image)
    assert torch.equal(out_mask, mask)
