import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision.nodes import tags as tags_node

node = tags_node.CFXTagsFilter()


def test_exclude():
    assert node.run("cat, dog", exclude="dog")[0] == "cat"


def test_include():
    assert node.run("cat, dog", include="cat")[0] == "cat"


def test_dedupe_is_case_insensitive_by_default():
    assert node.run("Cat, cat")[0] == "Cat"


def test_max_tags():
    assert node.run("a, b, c", max_tags=1)[0] == "a"


def test_all_excluded():
    assert node.run("a, b", exclude="a,b")[0] == ""
