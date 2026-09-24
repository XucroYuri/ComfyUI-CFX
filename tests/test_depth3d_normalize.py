import pytest
import torch

from comfyui_cfx.packages.depth3d.nodes import normalize as normalize_node

node = normalize_node.CFXNormalizeDepth()


def test_output_shapes_and_dtype():
    out_image, out_mask = node.run(torch.rand(2, 8, 8, 3))
    assert out_image.shape == (2, 8, 8, 3)
    assert out_mask.shape == (2, 8, 8)
    assert out_image.dtype == torch.float32
    assert out_mask.dtype == torch.float32


def test_minmax_reaches_both_bounds():
    image = torch.linspace(0.1, 0.9, steps=16).reshape(1, 4, 4, 1)
    _, out_mask = node.run(image, "minmax")
    assert float(out_mask.min()) == pytest.approx(0.0)
    assert float(out_mask.max()) == pytest.approx(1.0)


def test_invert_flips_normalized_output():
    image = torch.linspace(0.1, 0.9, steps=16).reshape(1, 4, 4, 1)
    _, base = node.run(image, "minmax", invert=False)
    _, inverted = node.run(image, "minmax", invert=True)
    assert torch.allclose(inverted, 1.0 - base)


def test_constant_image_is_zero_and_finite():
    image = torch.full((1, 4, 4, 3), 0.5)
    out_image, out_mask = node.run(image, "minmax")
    assert torch.isfinite(out_image).all()
    assert float(out_image.abs().max()) == 0.0
    assert float(out_mask.abs().max()) == 0.0


def test_clamp_mode_keeps_range():
    image = torch.tensor([-0.5, 0.25, 1.5]).reshape(1, 1, 3, 1)
    _, out_mask = node.run(image, "clamp")
    assert float(out_mask.min()) >= 0.0
    assert float(out_mask.max()) <= 1.0
    assert float(out_mask.min()) == pytest.approx(0.0)
    assert float(out_mask.max()) == pytest.approx(1.0)


def test_batch_items_normalize_independently():
    small = torch.tensor([[[10.0], [20.0]]])
    large = torch.tensor([[[1.0], [4.0]]])
    image = torch.cat([small, large], dim=0).unsqueeze(-1)
    _, out_mask = node.run(image, "minmax")
    assert float(out_mask[0].min()) == pytest.approx(0.0)
    assert float(out_mask[0].max()) == pytest.approx(1.0)
    assert float(out_mask[1].min()) == pytest.approx(0.0)
    assert float(out_mask[1].max()) == pytest.approx(1.0)
