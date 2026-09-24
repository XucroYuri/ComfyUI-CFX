"""Tests for the CLIP Interrogator node (interface + lazy import + dispatch)."""

import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision.nodes import clip_interrogator as node


def test_mode_methods_match_mode_combo():
    required = node.CFXClipInterrogator.INPUT_TYPES()["required"]
    assert list(node.MODE_METHODS) == required["mode"][0]


def test_clip_model_combo_exposes_both_entries():
    required = node.CFXClipInterrogator.INPUT_TYPES()["required"]
    models, options = required["clip_model"]
    assert models == ["ViT-L-14/openai", "ViT-H-14/laion2b_s32b_b79k"]
    assert options["default"] == "ViT-L-14/openai"


def test_module_import_is_lazy():
    # clip_interrogator is imported inside _load(), not at module import time.
    assert "clip_interrogator" not in node.__dict__


def test_unknown_mode_raises_value_error():
    with pytest.raises(ValueError):
        node.CFXClipInterrogator().run(None, mode="bogus")
