import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.inpaint.nodes import crop as crop_node
from comfyui_cfx.packages.inpaint.nodes import stitch as stitch_node

crop = crop_node.CFXCropByMask()
stitch = stitch_node.CFXStitchCrop()


def _rect_mask(height=64, width=64, y0=20, y1=30, x0=10, x1=25):
    mask = torch.zeros(1, height, width)
    mask[:, y0:y1, x0:x1] = 1.0
    return mask


def _crop(image, padding=0, multiple_of=1):
    _, _, data = crop.run(image, _rect_mask(), padding=padding, multiple_of=multiple_of)
    return data


def test_round_trip_restores_outside_and_applies_inside():
    image = torch.rand(1, 64, 64, 3)
    data = _crop(image)
    cropped, _, _ = crop.run(image, _rect_mask(), padding=0, multiple_of=1)
    patch = torch.rand_like(cropped)
    out = stitch.run(image, patch, data)[0]

    keep = torch.ones(1, 64, 64, 1, dtype=torch.bool)
    keep[:, 20:30, 10:25, :] = False
    assert torch.equal(out[keep.expand_as(out)], image[keep.expand_as(image)])
    assert torch.equal(out[0, 20:30, 10:25, :], patch[0])
    assert out.shape == image.shape


def test_stitch_does_not_mutate_base():
    image = torch.rand(1, 64, 64, 3)
    original = image.clone()
    data = _crop(image)
    patch = torch.ones(1, data["height"], data["width"], 3)
    stitch.run(image, patch, data)
    assert torch.equal(image, original)


def test_mask_weights_blend_patch_and_base():
    image = torch.rand(1, 64, 64, 3)
    data = _crop(image)
    cropped, crop_mask, _ = crop.run(image, _rect_mask(), padding=0, multiple_of=1)
    patch = torch.rand_like(cropped)
    weights = crop_mask * 0.25
    out = stitch.run(image, patch, data, mask=weights)[0]

    expected = image[0, 20:30, 10:25, :] * 0.75 + patch[0] * 0.25
    assert torch.allclose(out[0, 20:30, 10:25, :], expected, atol=1e-6)


def test_full_size_mask_also_blends():
    image = torch.rand(1, 64, 64, 3)
    data = _crop(image)
    cropped, _, _ = crop.run(image, _rect_mask(), padding=0, multiple_of=1)
    patch = torch.rand_like(cropped)
    full = torch.full((1, 64, 64), 0.5)
    out = stitch.run(image, patch, data, mask=full)[0]

    expected = image[0, 20:30, 10:25, :] * 0.5 + patch[0] * 0.5
    assert torch.allclose(out[0, 20:30, 10:25, :], expected, atol=1e-6)


def test_patch_size_mismatch_raises():
    image = torch.rand(1, 64, 64, 3)
    data = _crop(image)
    with pytest.raises(ValueError, match="does not match crop_data"):
        stitch.run(image, torch.rand(1, 5, 5, 3), data)


def test_missing_key_raises():
    image = torch.rand(1, 64, 64, 3)
    data = _crop(image)
    del data["x"]
    with pytest.raises(ValueError, match="missing 'x'"):
        stitch.run(image, torch.rand(1, 10, 15, 3), data)


def test_original_size_mismatch_raises():
    image = torch.rand(1, 64, 64, 3)
    data = _crop(image)
    data["original_width"] = 32
    with pytest.raises(ValueError, match="does not match base image"):
        stitch.run(image, torch.rand(1, 10, 15, 3), data)
