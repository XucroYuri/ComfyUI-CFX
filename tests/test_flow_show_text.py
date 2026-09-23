import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.flow.nodes import show_text as show_node

node = show_node.CFXShowText()


def test_returns_ui_and_result():
    result = node.show("hello")
    assert result["ui"]["text"] == ["hello"]
    assert result["result"] == ("hello",)


def test_empty_text():
    result = node.show("")
    assert result["ui"]["text"] == [""]
