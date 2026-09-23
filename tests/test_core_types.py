import pytest
import torch

from comfyui_cfx.core import types


def test_ensure_image_from_hwc():
    out = types.ensure_image(torch.rand(8, 8, 3))
    assert out.shape == (1, 8, 8, 3)
    assert out.dtype == torch.float32


def test_ensure_image_from_bchw():
    out = types.ensure_image(torch.rand(2, 3, 8, 8))
    assert out.shape == (2, 8, 8, 3)


def test_ensure_image_rejects_bad_shape():
    with pytest.raises(ValueError):
        types.ensure_image(torch.rand(2, 2))


def test_make_and_read_latent():
    latent = types.make_latent(torch.randn(1, 4, 8, 8))
    assert types.latent_samples(latent).shape == (1, 4, 8, 8)


def test_latent_requires_dict():
    with pytest.raises(ValueError):
        types.latent_samples(torch.randn(1, 4, 8, 8))
