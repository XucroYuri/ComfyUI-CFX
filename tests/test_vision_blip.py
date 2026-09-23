import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision.nodes import blip as blip_node


def test_input_types_expose_models_and_modes():
    required = blip_node.CFXBlipCaption.INPUT_TYPES()["required"]
    assert "Salesforce/blip-image-captioning-base" in required["model"][0]
    assert required["mode"][0] == ["caption", "interrogate"]


def test_default_question_present():
    required = blip_node.CFXBlipCaption.INPUT_TYPES()["required"]
    assert required["question"][1]["default"] == "What is in the image?"


def test_module_import_is_lazy():
    # transformers is imported inside _load(), not at module import time.
    assert "transformers" not in blip_node.__dict__
