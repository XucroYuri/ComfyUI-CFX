import pytest

torch = pytest.importorskip("torch")

from comfyui_cfx.packages.sampling.nodes import sigmas as sigmas_node

node = sigmas_node.CFXSplitSigmas()


def _sigmas(length=10, dtype=torch.float32, device="cpu"):
    return torch.linspace(1.0, 0.0, length, dtype=dtype, device=device)


def test_split_lengths():
    high, low = node.run(_sigmas(), 4)
    assert high.shape == (4,)
    assert low.shape == (6,)
    assert high.is_contiguous() and low.is_contiguous()


def test_step_zero():
    source = _sigmas()
    high, low = node.run(source, 0)
    assert high.numel() == 0
    assert torch.equal(low, source)


def test_step_len():
    source = _sigmas()
    high, low = node.run(source, source.numel())
    assert torch.equal(high, source)
    assert low.numel() == 0


def test_dtype_and_device_preserved():
    source = _sigmas(dtype=torch.float64)
    high, low = node.run(source, 4)
    assert high.dtype == source.dtype
    assert low.dtype == source.dtype
    assert high.device == source.device
    assert low.device == source.device


def test_step_out_of_range_raises():
    with pytest.raises(ValueError):
        node.run(_sigmas(), 11)


def test_non_1d_raises():
    with pytest.raises(ValueError):
        node.run(torch.zeros(2, 3), 1)


def test_concatenation_restores_original():
    source = _sigmas()
    high, low = node.run(source, 4)
    assert torch.equal(torch.cat((high, low)), source)
