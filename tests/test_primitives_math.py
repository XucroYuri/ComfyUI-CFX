import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import math as math_node

node = math_node.CFXMath()


def test_basic_arithmetic():
    assert node.compute("a + b", 2, 3) == (5, 5.0)


def test_precedence_and_functions():
    assert node.compute("max(a, b) * 2", 4, 1) == (8, 8.0)
    assert node.compute("sqrt(16)") == (4, 4.0)


def test_if_expression():
    assert node.compute("a if a > b else b", 1, 7) == (7, 7.0)


def test_int_and_float_outputs():
    int_out, float_out = node.compute("a / b", 3, 2)
    assert int_out == 1
    assert float_out == 1.5


@pytest.mark.parametrize("expression", [
    "__import__('os')",
    "a.__class__",
    "open('x')",
    "lambda: 1",
    "[x for x in range(3)]",
])
def test_unsafe_expressions_rejected(expression):
    with pytest.raises(ValueError):
        math_node.evaluate(expression, {"a": 1})


def test_division_by_zero_raises():
    with pytest.raises(ValueError):
        math_node.evaluate("1 / 0", {})


def test_non_finite_raises():
    with pytest.raises(ValueError):
        math_node.evaluate("sqrt(-1)", {})


def test_empty_and_long_expressions_raise():
    with pytest.raises(ValueError):
        math_node.evaluate("", {})
    with pytest.raises(ValueError):
        math_node.evaluate("1+" * 5000 + "1", {})
