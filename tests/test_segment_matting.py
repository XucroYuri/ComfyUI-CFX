import numpy as np
import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment.nodes import matting as matting_node


def test_alpha_to_mask_extracts_alpha():
    rgba = np.zeros((4, 4, 4), dtype=np.uint8)
    rgba[..., 3] = 255
    mask = matting_node.alpha_to_mask(rgba)
    assert mask.shape == (4, 4)
    assert mask.dtype == np.float32
    assert mask[0, 0] == 1.0


def test_alpha_to_mask_rejects_non_rgba():
    with pytest.raises(ValueError):
        matting_node.alpha_to_mask(np.zeros((4, 4, 3), dtype=np.uint8))


def test_input_types_expose_models():
    required = matting_node.CFXMatting.INPUT_TYPES()["required"]
    assert "birefnet-general" in required["model"][0]


def test_outputs_are_mask_and_image():
    assert matting_node.CFXMatting.RETURN_TYPES == ("MASK", "IMAGE")


def test_rembg_import_is_lazy():
    assert "rembg" not in matting_node.__dict__
