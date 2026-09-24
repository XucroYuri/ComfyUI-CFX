import pytest

pytest.importorskip("torch")

import torch

from comfyui_cfx.packages.flux.nodes import concat as concat_node

node = concat_node.CFXConditioningConcat()


def _entry():
    return [torch.rand(1, 8), {"guidance": 3.5}]


def test_length_is_sum():
    a = [_entry(), _entry()]
    b = [_entry()]
    (out,) = node.run(a, b)
    assert len(out) == len(a) + len(b)


def test_order_a_entries_first():
    a1, a2 = _entry(), _entry()
    b1 = _entry()
    (out,) = node.run([a1, a2], [b1])
    assert out[0] is a1
    assert out[1] is a2
    assert out[2] is b1


def test_entries_are_same_references_and_inputs_not_mutated():
    a1, b1 = _entry(), _entry()
    a = [a1]
    b = [b1]
    (out,) = node.run(a, b)
    assert out is not a
    assert out is not b
    assert out[0] is a1
    assert out[1] is b1
    assert a == [a1]
    assert b == [b1]
    assert len(a) == 1
    assert len(b) == 1


def test_empty_inputs_raise():
    entry = [_entry()]
    with pytest.raises(ValueError):
        node.run([], entry)
    with pytest.raises(ValueError):
        node.run(entry, [])


def test_non_list_inputs_raise():
    entry = [_entry()]
    with pytest.raises(ValueError):
        node.run("not-a-list", entry)
    with pytest.raises(ValueError):
        node.run(entry, None)
