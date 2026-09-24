import json

import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment import backend
from comfyui_cfx.packages.segment.nodes import sam2_points as sam2_points_node


def test_parse_points_pair_lists():
    assert sam2_points_node.parse_points("[[1, 2], [3.5, 4]]") == [
        {"x": 1.0, "y": 2.0},
        {"x": 3.5, "y": 4.0},
    ]


def test_parse_points_dicts():
    assert sam2_points_node.parse_points('[{"x": 5, "y": 6}]') == [{"x": 5.0, "y": 6.0}]


def test_parse_points_empty_text():
    assert sam2_points_node.parse_points("") == []
    assert sam2_points_node.parse_points("   ") == []


@pytest.mark.parametrize("text", ["nope", "{}", "[[1]]", '[{"x": 1}]', '{"x": 1, "y": 2}'])
def test_parse_points_invalid_raises(text):
    with pytest.raises(ValueError):
        sam2_points_node.parse_points(text)


def test_run_rejects_empty_positive(monkeypatch):
    calls = []
    monkeypatch.setattr(backend, "segment_points", lambda *args, **kwargs: calls.append(args) or (object(),))
    node = sam2_points_node.CFXSam2Points()
    with pytest.raises(ValueError):
        node.run(object(), object(), "[]")
    assert calls == []


def test_run_forwards_json_and_no_negative(monkeypatch):
    captured = {}

    def fake_segment_points(sam2, image, positive, negative=None, keep_model_loaded=False):
        captured.update(positive=positive, negative=negative, keep_model_loaded=keep_model_loaded)
        return ("MASK",)

    monkeypatch.setattr(backend, "segment_points", fake_segment_points)
    result = sam2_points_node.CFXSam2Points().run("model", "image", "[[128, 128]]")
    assert result == ("MASK",)
    assert isinstance(captured["positive"], str)
    assert json.loads(captured["positive"]) == [{"x": 128.0, "y": 128.0}]
    assert captured["negative"] is None
    assert captured["keep_model_loaded"] is False


def test_run_forwards_negative_points(monkeypatch):
    captured = {}

    def fake_segment_points(sam2, image, positive, negative=None, keep_model_loaded=False):
        captured.update(positive=positive, negative=negative)
        return ("MASK",)

    monkeypatch.setattr(backend, "segment_points", fake_segment_points)
    sam2_points_node.CFXSam2Points().run("model", "image", "[[1, 2]]", negative_points='[{"x": 3, "y": 4}]')
    assert json.loads(captured["positive"]) == [{"x": 1.0, "y": 2.0}]
    assert json.loads(captured["negative"]) == [{"x": 3.0, "y": 4.0}]


def test_input_types_expose_inputs():
    types = sam2_points_node.CFXSam2Points.INPUT_TYPES()
    assert types["required"]["sam2"] == ("CFX_SAM2",)
    assert types["required"]["image"] == ("IMAGE",)
    assert types["required"]["positive_points"][1]["default"] == "[[128, 128]]"
    assert types["optional"]["negative_points"][1]["default"] == ""
    assert types["optional"]["keep_model_loaded"][1]["default"] is False
    assert sam2_points_node.CFXSam2Points.RETURN_TYPES == ("MASK",)
    assert sam2_points_node.CFXSam2Points.RETURN_NAMES == ("mask",)
