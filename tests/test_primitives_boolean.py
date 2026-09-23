import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import boolean as boolean_node

node = boolean_node.CFXBoolean()


def test_and_or():
    assert node.compute(True, "and", True) == (True,)
    assert node.compute(True, "and", False) == (False,)
    assert node.compute(False, "or", True) == (True,)


def test_xor_nand_nor():
    assert node.compute(True, "xor", True) == (False,)
    assert node.compute(True, "nand", True) == (False,)
    assert node.compute(False, "nor", False) == (True,)


def test_implication_truth_table():
    assert node.compute(True, "a_implies_b", False) == (False,)
    assert node.compute(False, "a_implies_b", False) == (True,)
    assert node.compute(False, "a_implies_b", True) == (True,)


def test_unary_ignores_b():
    assert node.compute(True, "not_a", True) == (False,)
    assert node.compute(False, "not_b", False) == (True,)


def test_ints_are_interpreted_as_bool():
    assert node.compute(1, "and", 0) == (False,)


def test_unknown_operation_raises():
    with pytest.raises(ValueError):
        node.compute(True, "bogus", True)
