import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.flow.nodes import string_function as string_node

node = string_node.CFXStringFunction()


def test_append():
    assert node.run("append", text="a", other="b") == ("a, b",)


def test_prepend():
    assert node.run("prepend", text="b", other="a") == ("a, b",)


def test_append_with_empty_side():
    assert node.run("append", text="", other="b") == ("b",)
    assert node.run("append", text="a", other="") == ("a",)


def test_replace_literal():
    assert node.run("replace", text="a cat", other="cat", replacement="dog") == ("a dog",)


def test_replace_with_empty_search_is_noop():
    assert node.run("replace", text="abc", other="", replacement="X") == ("abc",)


def test_regex_replace():
    assert node.run("regex_replace", text="a1b2", other=r"\d", replacement="#") == ("a#b#",)


def test_regex_invalid_raises():
    with pytest.raises(ValueError):
        node.run("regex_replace", text="x", other="(", replacement="")


def test_tidy_cleans_segments():
    assert node.run("append", text=" a ,, b ", other=" c ", tidy=True) == ("a, b, c",)


def test_unknown_action_raises():
    with pytest.raises(ValueError):
        node.run("bogus", text="a")
