import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment.nodes import sam2_auto


def _handle(segmentor="automaskgenerator"):
    return {"segmentor": segmentor}


def test_run_returns_mask_and_bboxes(monkeypatch):
    mask = object()
    bboxes = [[1.0, 2.0, 3.0, 4.0]]
    monkeypatch.setattr(sam2_auto, "auto_mask", lambda *a, **k: (mask, object(), bboxes))
    result = sam2_auto.CFXSam2AutoMask().run(_handle(), "image")
    assert result == (mask, bboxes)


def test_run_forwards_keep_model_loaded_and_knobs(monkeypatch):
    captured = {}

    def fake_auto_mask(sam2, image, keep_model_loaded=False, **kwargs):
        captured.update(keep_model_loaded=keep_model_loaded, kwargs=kwargs)
        return (object(), object(), [])

    monkeypatch.setattr(sam2_auto, "auto_mask", fake_auto_mask)
    sam2_auto.CFXSam2AutoMask().run(
        _handle(), "image", keep_model_loaded=True, points_per_side=8, pred_iou_thresh=0.5
    )
    assert captured["keep_model_loaded"] is True
    assert captured["kwargs"]["points_per_side"] == 8
    assert captured["kwargs"]["pred_iou_thresh"] == 0.5


def test_wrong_segmentor_raises_helpful(monkeypatch):
    calls = []
    monkeypatch.setattr(sam2_auto, "auto_mask", lambda *a, **k: calls.append(a) or (object(), object(), []))
    with pytest.raises(ValueError) as exc:
        sam2_auto.CFXSam2AutoMask().run(_handle("single_image"), "image")
    assert "automaskgenerator" in str(exc.value)
    assert "SAM2 Loader" in str(exc.value)
    assert calls == []


def test_input_types_expose_inputs():
    types = sam2_auto.CFXSam2AutoMask.INPUT_TYPES()
    assert types["required"]["sam2"] == ("CFX_SAM2",)
    assert types["required"]["image"] == ("IMAGE",)
    assert types["optional"]["keep_model_loaded"][1]["default"] is False
    assert types["optional"]["points_per_side"][1]["default"] == 32
    assert types["optional"]["pred_iou_thresh"][1]["default"] == 0.8
    assert types["optional"]["stability_score_thresh"][1]["default"] == 0.95
    assert sam2_auto.CFXSam2AutoMask.RETURN_TYPES == ("MASK", "JSON")
    assert sam2_auto.CFXSam2AutoMask.RETURN_NAMES == ("mask", "bboxes")
    assert sam2_auto.CFXSam2AutoMask.FUNCTION == "run"
    assert sam2_auto.CFXSam2AutoMask.CATEGORY == "ComfyUI-Segment/SAM2"
