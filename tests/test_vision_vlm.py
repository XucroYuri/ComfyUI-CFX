"""Tests for the VLM caption node (interface + message construction)."""

import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision import vlm as vlm_module
from comfyui_cfx.packages.vision.nodes import vlm as vlm_node


def test_build_messages_has_image_then_text():
    messages = vlm_module.build_messages("hello")
    assert messages[0]["role"] == "user"
    types = [part["type"] for part in messages[0]["content"]]
    assert types == ["image", "text"]
    assert messages[0]["content"][1]["text"] == "hello"


def test_input_types_expose_qwen_models():
    required = vlm_node.CFXVlmCaption.INPUT_TYPES()["required"]
    assert "Qwen/Qwen2.5-VL-3B-Instruct" in required["model"][0]
    assert required["precision"][0] == ["bf16", "fp16", "fp32"]


def test_module_import_is_lazy():
    assert "transformers" not in vlm_module.__dict__
