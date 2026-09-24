import pytest

pytest.importorskip("torch")

import torch

from comfyui_cfx.packages.flux.nodes import blend as blend_node

node = blend_node.CFXConditioningBlend()


def _conditioning(tensor, meta=None):
    return [[tensor, {"guidance": 3.5} if meta is None else meta]]


def test_factor_zero_returns_a():
    a = _conditioning(torch.rand(1, 8))
    b = _conditioning(torch.rand(1, 8))
    (out,) = node.run(a, b, 0.0)
    assert torch.equal(out[0][0], a[0][0])


def test_factor_one_returns_b():
    a = _conditioning(torch.rand(1, 8))
    b = _conditioning(torch.rand(1, 8))
    (out,) = node.run(a, b, 1.0)
    assert torch.equal(out[0][0], b[0][0])


def test_factor_half_is_midpoint():
    a = _conditioning(torch.zeros(1, 8))
    b = _conditioning(torch.ones(1, 8))
    (out,) = node.run(a, b, 0.5)
    assert torch.allclose(out[0][0], torch.full((1, 8), 0.5))


def test_metadata_comes_from_a_and_input_not_mutated():
    a_meta = {"guidance": 3.5}
    b_meta = {"guidance": 9.0}
    a = [[torch.rand(1, 8), a_meta]]
    b = [[torch.rand(1, 8), b_meta]]
    (out,) = node.run(a, b, 0.5)
    assert out[0][1] == a_meta
    assert out[0][1] is not a_meta
    out[0][1]["guidance"] = 1.0
    assert a_meta == {"guidance": 3.5}
    assert b_meta == {"guidance": 9.0}


def test_length_mismatch_raises():
    a = [[torch.rand(1, 8), {}], [torch.rand(1, 8), {}]]
    b = [[torch.rand(1, 8), {}]]
    with pytest.raises(ValueError):
        node.run(a, b, 0.5)


def test_empty_inputs_raise():
    entry = [[torch.rand(1, 8), {}]]
    with pytest.raises(ValueError):
        node.run([], entry, 0.5)
    with pytest.raises(ValueError):
        node.run(entry, [], 0.5)


def test_dtype_of_a_preserved_when_b_float64():
    a = [[torch.rand(1, 8, dtype=torch.float32), {}]]
    b = [[torch.rand(1, 8, dtype=torch.float64), {}]]
    (out,) = node.run(a, b, 1.0)
    assert out[0][0].dtype == torch.float32
