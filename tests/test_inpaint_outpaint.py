import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.inpaint.nodes import outpaint as outpaint_node

node = outpaint_node.CFXOutpaintCanvas()

# Canvas geometry used across the tests: original 8x6 pasted at (left=2, top=1).
H, W, C = 8, 6, 3
LEFT, RIGHT, TOP, BOTTOM = 2, 3, 1, 4
NEW_H, NEW_W = H + TOP + BOTTOM, W + LEFT + RIGHT


def _inputs():
    return torch.rand(1, H, W, C), torch.rand(1, H, W)


def test_canvas_shape():
    image, mask = _inputs()
    out_image, out_mask = node.run(image, mask, left=LEFT, right=RIGHT, top=TOP, bottom=BOTTOM, fill=0.5)
    assert out_image.shape == (1, NEW_H, NEW_W, C)
    assert out_mask.shape == (1, NEW_H, NEW_W)


def test_border_pixels_equal_fill():
    image, mask = _inputs()
    fill = 0.25
    out_image, _ = node.run(image, mask, left=LEFT, right=RIGHT, top=TOP, bottom=BOTTOM, fill=fill)

    assert torch.all(out_image[:, :TOP, :, :] == fill)
    assert torch.all(out_image[:, TOP + H:, :, :] == fill)
    assert torch.all(out_image[:, TOP:TOP + H, :LEFT, :] == fill)
    assert torch.all(out_image[:, TOP:TOP + H, LEFT + W:, :] == fill)


def test_original_region_equals_input_image():
    image, mask = _inputs()
    out_image, _ = node.run(image, mask, left=LEFT, right=RIGHT, top=TOP, bottom=BOTTOM, fill=0.5)
    assert torch.equal(out_image[:, TOP:TOP + H, LEFT:LEFT + W, :], image)


def test_output_mask_border_is_one_and_interior_matches_input():
    image, mask = _inputs()
    _, out_mask = node.run(image, mask, left=LEFT, right=RIGHT, top=TOP, bottom=BOTTOM, fill=0.5)

    assert torch.all(out_mask[:, :TOP, :] == 1.0)
    assert torch.all(out_mask[:, TOP + H:, :] == 1.0)
    assert torch.all(out_mask[:, TOP:TOP + H, :LEFT] == 1.0)
    assert torch.all(out_mask[:, TOP:TOP + H, LEFT + W:] == 1.0)
    assert torch.allclose(out_mask[:, TOP:TOP + H, LEFT:LEFT + W], mask.clamp(0.0, 1.0))


def test_zero_margins_returns_inputs_unchanged():
    image, mask = _inputs()
    out_image, out_mask = node.run(image, mask)
    assert torch.equal(out_image, image)
    assert torch.equal(out_mask, mask)
    assert out_image.shape == (1, H, W, C)
    assert out_mask.shape == (1, H, W)


def test_mask_hw_shape_works():
    image, mask = _inputs()
    flat_mask = mask[0]
    out_image, out_mask = node.run(image, flat_mask, left=LEFT, right=RIGHT, top=TOP, bottom=BOTTOM, fill=0.5)
    assert out_image.shape == (1, NEW_H, NEW_W, C)
    assert out_mask.shape == (1, NEW_H, NEW_W)
    assert torch.allclose(out_mask[:, TOP:TOP + H, LEFT:LEFT + W], flat_mask.clamp(0.0, 1.0))
