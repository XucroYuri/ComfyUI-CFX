import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import text as text_node

node = text_node.CFXText()


def test_concat_with_defaults():
    assert node.run("concat", text1="a", text2="b") == ("a, b",)


def test_concat_skips_empty_and_trims():
    assert node.run("concat", text1="  a  ", text2="", text3="b") == ("a, b",)


def test_concat_keeps_empty_when_disabled():
    assert node.run("concat", clean_whitespace=False, skip_empty=False, text1="a", text2="") == ("a, ",)


def test_delimiter_newline_escape():
    assert node.run("concat", delimiter="\\n", text1="a", text2="b") == ("a\nb",)


def test_all_empty_returns_empty_string():
    assert node.run("concat") == ("",)


def test_replace_literal():
    assert node.run("replace", search="cat", replace="dog", text1="a cat") == ("a dog",)


def test_replace_with_empty_search_is_noop():
    assert node.run("replace", search="", replace="X", text1="abc") == ("abc",)


def test_operation_ignores_unconnected_slots():
    assert node.run("concat", text1="a", text3="c") == ("a, c",)
