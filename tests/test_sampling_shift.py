import pytest

torch = pytest.importorskip("torch")

from comfyui_cfx.packages.sampling.nodes import shift as shift_node

node = shift_node.CFXSigmaShift()


def _sigmas(length=10, dtype=torch.float32, device="cpu"):
    return torch.linspace(1.0, 0.0, length, dtype=dtype, device=device)


def test_factor_one_unchanged():
    source = _sigmas()
    out = node.run(source, 1.0)[0]
    assert torch.equal(out, source)


def test_factor_two_doubles():
    source = _sigmas()
    out = node.run(source, 2.0)[0]
    assert torch.allclose(out, source * 2.0)


def test_dtype_and_device_preserved():
    source = _sigmas(dtype=torch.float64)
    out = node.run(source, 2.0)[0]
    assert out.dtype == source.dtype
    assert out.device == source.device


def test_input_not_mutated():
    source = _sigmas()
    before = source.clone()
    node.run(source, 3.0)
    assert torch.equal(source, before)


def test_non_1d_raises():
    with pytest.raises(ValueError):
        node.run(torch.zeros(2, 3), 1.0)


def test_output_contiguous():
    source = _sigmas()
    sliced = source[::2]
    assert not sliced.is_contiguous()
    out = node.run(sliced, 2.0)[0]
    assert out.is_contiguous()
