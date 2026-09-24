import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

import torch

from comfyui_cfx.packages.segment.nodes import text_to_mask


class _FakeDetect:
    def __init__(self, detections):
        self._detections = detections
        self.calls = []

    def run(self, image, prompt, model, box_threshold, text_threshold):
        self.calls.append((prompt, model, box_threshold, text_threshold))
        return (self._detections, None)


def _patch_detect(monkeypatch, detections):
    fake = _FakeDetect(detections)
    monkeypatch.setattr(text_to_mask, "CFXGroundingDinoDetect", lambda: fake)
    return fake


def _image(height=8, width=6):
    return torch.zeros((1, height, width, 3), dtype=torch.float32)


def test_sam2_path_uses_box_batch(monkeypatch):
    detections = {"bboxes": [[1, 2, 3, 4], [5, 6, 7, 8]], "labels": ["cat", "dog"]}
    _patch_detect(monkeypatch, detections)
    captured = {}

    def fake_segment(sam2, image, bboxes=None, keep_model_loaded=False):
        captured["sam2"] = sam2
        captured["bboxes"] = bboxes
        captured["keep_model_loaded"] = keep_model_loaded
        return (torch.ones((1, 8, 6), dtype=torch.float32),)

    monkeypatch.setattr(text_to_mask, "segment", fake_segment)
    node = text_to_mask.CFXTextToMask()

    mask, out = node.run(_image(), "cat. dog.", "model", 0.3, 0.25, sam2="SAM2", keep_model_loaded=True)

    assert captured["sam2"] == "SAM2"
    assert captured["bboxes"] == [[[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]]]
    assert captured["keep_model_loaded"] is True
    assert mask.shape == (1, 8, 6)
    assert out is detections


def test_fallback_boxes_to_mask(monkeypatch):
    detections = {"bboxes": [[1, 1, 3, 3]], "labels": ["x"]}
    _patch_detect(monkeypatch, detections)
    monkeypatch.setattr(text_to_mask, "segment", lambda *a, **k: pytest.fail("segment must not run"))
    node = text_to_mask.CFXTextToMask()

    mask, out = node.run(_image(5, 5), "x.", "model", 0.3, 0.25)

    assert mask.shape == (1, 5, 5)
    assert mask[0, 2, 2] == 1.0
    assert mask[0, 0, 0] == 0.0
    assert out is detections


def test_empty_detections_give_zero_mask(monkeypatch):
    detections = {"bboxes": [], "labels": []}
    _patch_detect(monkeypatch, detections)
    monkeypatch.setattr(text_to_mask, "segment", lambda *a, **k: pytest.fail("segment must not run"))
    node = text_to_mask.CFXTextToMask()

    mask, out = node.run(_image(4, 7), "nothing.", "model", 0.3, 0.25)

    assert mask.shape == (1, 4, 7)
    assert float(mask.sum()) == 0.0
    assert out is detections


def test_interface_contract():
    node = text_to_mask.CFXTextToMask
    required = node.INPUT_TYPES()["required"]
    assert "IDEA-Research/grounding-dino-tiny" in required["detect_model"][0]
    assert required["box_threshold"][1]["default"] == 0.30
    assert required["text_threshold"][1]["default"] == 0.25
    assert "sam2" in node.INPUT_TYPES()["optional"]
    assert node.RETURN_TYPES == ("MASK", "JSON")
    assert node.RETURN_NAMES == ("mask", "detections")
    assert node.CATEGORY == "ComfyUI-Segment/Detect"
