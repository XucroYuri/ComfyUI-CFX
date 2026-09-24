import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment.nodes import segs as segs_node

to_segs = segs_node.CFXMaskToSegs()
to_mask = segs_node.CFXSegsToMask()

KEYS = {
    "cropped_image",
    "cropped_mask",
    "confidence",
    "crop_region",
    "bbox",
    "label",
    "control_net_wrapper",
}


def _image(batch=1, height=10, width=10):
    return torch.rand(batch, height, width, 3, dtype=torch.float32)


def _mask(batch=1, height=10, width=10):
    return torch.zeros(batch, height, width, dtype=torch.float32)


def test_structure_keys_dtypes_shapes():
    mask = _mask()
    mask[0, 2:5, 3:7] = 1.0
    segs = to_segs.run(_image(), mask, label="cat", confidence=0.75)[0]

    assert isinstance(segs, list)
    assert len(segs) == 1
    (height, width), meta = segs[0]
    assert (height, width) == (10, 10)
    assert set(meta) == KEYS
    assert meta["bbox"] == (3, 2, 7, 5)
    assert meta["crop_region"] == (3, 2, 7, 5)
    assert meta["label"] == "cat"
    assert meta["confidence"] == 0.75
    assert meta["control_net_wrapper"] is None
    assert meta["cropped_image"].shape == (3, 4, 3)
    assert meta["cropped_mask"].shape == (3, 4)
    assert meta["cropped_image"].dtype == torch.float32
    assert meta["cropped_mask"].dtype == torch.float32


def test_roundtrip_recovers_mask():
    mask = _mask(1, 12, 12)
    mask[0, 2:6, 3:9] = 1.0
    segs = to_segs.run(_image(1, 12, 12), mask)[0]
    recovered = to_mask.run(segs)[0]

    assert recovered.shape == (1, 12, 12)
    assert torch.allclose(recovered, mask)
    assert torch.allclose(recovered[mask > 0.5], mask[mask > 0.5])


def test_empty_mask_yields_empty_segs():
    assert to_segs.run(_image(), _mask())[0] == []


def test_segs_to_mask_ors_two_segments():
    mask = _mask(2, 10, 10)
    mask[0, 1:3, 1:3] = 1.0
    mask[1, 6:8, 6:8] = 1.0
    segs = to_segs.run(_image(2, 10, 10), mask)[0]

    assert len(segs) == 2
    union = to_mask.run(segs)[0]
    assert union.shape == (1, 10, 10)
    assert torch.allclose(union[0], torch.maximum(mask[0], mask[1]))


def test_single_image_broadcasts_over_mask_batch():
    mask = _mask(2, 10, 10)
    mask[0, 1:3, 1:3] = 1.0
    mask[1, 6:8, 6:8] = 1.0
    segs = to_segs.run(_image(1, 10, 10), mask)[0]
    assert len(segs) == 2


def test_segs_to_mask_empty_raises():
    with pytest.raises(ValueError):
        to_mask.run([])


def test_width_height_override():
    mask = _mask(1, 10, 10)
    mask[0, 2:4, 2:4] = 1.0
    segs = to_segs.run(_image(), mask)[0]

    overridden = to_mask.run(segs, width=20, height=16)[0]
    assert overridden.shape == (1, 16, 20)
    assert float(overridden[0, 2, 2]) == 1.0
    assert float(overridden[0, 10, 10]) == 0.0
