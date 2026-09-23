import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.flow.nodes import repeater as repeater_node

node = repeater_node.CFXRepeater()


def test_repeats_value():
    values = node.repeat("x", 3)[0]
    assert values == ["x", "x", "x"]


def test_repeats_once():
    assert node.repeat(5, 1)[0] == [5]


def test_repeats_keeps_identity():
    payload = {"k": 1}
    values = node.repeat(payload, 2)[0]
    assert values[0] is payload and values[1] is payload
