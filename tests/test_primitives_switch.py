import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import switch as switch_node

node = switch_node.CFXSwitch()


def test_index_selects_slot():
    assert node.switch("index", 1, input1="a", input2="b") == ("b", 1)


def test_index_is_clamped():
    assert node.switch("index", 99, input8="z") == ("z", 7)
    assert node.switch("index", -5, input1="a") == ("a", 0)


def test_unconnected_slot_raises():
    with pytest.raises(ValueError):
        node.switch("index", 2, input1="a")


def test_first_connected_skips_none():
    assert node.switch("first_connected", input2=0, input3=5) == (0, 1)


def test_falsy_is_connected():
    assert node.switch("index", 0, input1=0) == (0, 0)
    assert node.switch("index", 0, input1=False) == (False, 0)


def test_first_connected_all_empty_raises():
    with pytest.raises(ValueError):
        node.switch("first_connected")
