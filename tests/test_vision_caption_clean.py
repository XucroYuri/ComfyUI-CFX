import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision.nodes import text as text_node

node = text_node.CFXCaptionClean()


def test_strip_special_tokens():
    assert node.run("<s>hello</s>")[0] == "hello"


def test_strip_generic_tokens():
    assert node.run("<CAPTION>hello")[0] == "hello"


def test_unclosed_token_is_kept():
    assert node.run("a < b")[0] == "a < b"


def test_collapse_whitespace():
    assert node.run("a   b\n c")[0] == "a b c"


def test_dedupe_tags_keeps_order():
    assert node.run("cat, dog, cat", dedupe_tags=True)[0] == "cat, dog"


def test_max_chars_breaks_at_delimiter():
    assert node.run("aa, bb, cc", max_chars=8)[0] == "aa, bb"


def test_whitespace_only_becomes_empty():
    assert node.run("   ")[0] == ""
