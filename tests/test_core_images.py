import numpy as np
import torch

from comfyui_cfx.core.images import first_image_to_pil


def test_returns_uint8_rgb_pil():
    pil = first_image_to_pil(torch.rand(1, 8, 6, 3))
    assert pil.mode == "RGB"
    assert pil.size == (6, 8)


def test_clamps_out_of_range_values():
    image = torch.full((1, 2, 2, 3), 5.0)
    pil = first_image_to_pil(image)
    assert np.asarray(pil).max() == 255


def test_uses_first_batch_item():
    batch = torch.zeros(2, 2, 2, 3)
    batch[1] = 1.0
    pil = first_image_to_pil(batch)
    assert np.asarray(pil).max() == 0
