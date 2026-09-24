"""Tests for the BLIP-2 caption/VQA node (interface + lazy import)."""

import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision.nodes import blip2 as node


def test_model_combo_exposes_all_entries():
    required = node.CFXBlip2Caption.INPUT_TYPES()["required"]
    models, options = required["model"]
    assert models == [
        "Salesforce/blip2-opt-2.7b",
        "Salesforce/blip2-flan-t5-xl",
        "Salesforce/blip2-opt-6.7b",
    ]
    assert options["default"] == "Salesforce/blip2-opt-2.7b"


def test_mode_combo_is_caption_or_vqa():
    required = node.CFXBlip2Caption.INPUT_TYPES()["required"]
    assert required["mode"][0] == ["caption", "vqa"]


def test_module_import_is_lazy():
    # transformers is imported inside _load(), not at module import time.
    assert "transformers" not in node.__dict__


def test_unknown_precision_raises_value_error():
    with pytest.raises(ValueError):
        node.CFXBlip2Caption().run(None, "Salesforce/blip2-opt-2.7b", precision="bogus")
