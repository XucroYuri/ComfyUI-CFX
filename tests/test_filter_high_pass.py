import pytest
import torch

from comfyui_cfx.packages.filter.nodes import high_pass as high_pass_node

node = high_pass_node.CFXHighPass


def test_shape_preserved():
    image = torch.rand(2, 16, 24, 3)
    (out,) = node().run(image, radius=4, strength=1.0)
    assert out.shape == image.shape
    assert out.dtype == torch.float32


def test_zero_strength_is_identity():
    image = torch.rand(1, 16, 16, 3)
    (out,) = node().run(image, radius=4, strength=0.0)
    assert torch.allclose(out, image)


def test_constant_image_unchanged():
    image = torch.full((1, 16, 16, 3), 0.5)
    (out,) = node().run(image, radius=4, strength=2.0)
    assert torch.allclose(out, image)


def test_output_stays_in_unit_interval():
    image = torch.rand(1, 16, 16, 3)
    (out,) = node().run(image, radius=8, strength=10.0)
    assert float(out.min()) >= 0.0
    assert float(out.max()) <= 1.0


def test_step_edge_gains_contrast():
    image = torch.full((1, 64, 64, 1), 0.4)
    image[:, :, 32:, :] = 0.6
    (out,) = node().run(image, radius=4, strength=1.0)
    assert float(out.std()) > float(image.std())


def test_oversized_radius_raises():
    image = torch.rand(1, 4, 4, 3)
    with pytest.raises((RuntimeError, ValueError)):
        node().run(image, radius=8, strength=1.0)
