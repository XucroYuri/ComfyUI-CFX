import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.segment.nodes import detect as detect_node


def test_input_types_expose_models_and_thresholds():
    required = detect_node.CFXGroundingDinoDetect.INPUT_TYPES()["required"]
    assert "IDEA-Research/grounding-dino-tiny" in required["model"][0]
    assert required["box_threshold"][1]["default"] == 0.30
    assert required["text_threshold"][1]["default"] == 0.25


def test_module_import_is_lazy():
    assert "transformers" not in detect_node.__dict__


def test_outputs_are_json_and_mask():
    assert detect_node.CFXGroundingDinoDetect.RETURN_TYPES == ("JSON", "MASK")
