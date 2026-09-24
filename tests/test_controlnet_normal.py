import pytest

torch = pytest.importorskip("torch")

from comfyui_cfx.packages.controlnet.nodes import normal as normal_node

node = normal_node.CFXNormalFromDepth()


def _flat_depth(value=0.5, size=8):
    return torch.full((1, size, size, 1), value)


def _ramp_depth(size=8):
    """Depth that varies along width only, so dx is non-zero and dy is zero."""
    column = torch.linspace(0.1, 0.9, size).reshape(1, 1, size, 1)
    return column.expand(1, size, size, 1).contiguous()


def test_output_shape():
    out = node.run(_ramp_depth())[0]
    assert out.shape == (1, 8, 8, 3)


def test_output_range_within_unit_interval():
    out = node.run(_ramp_depth())[0]
    assert float(out.min()) >= 0.0
    assert float(out.max()) <= 1.0


def test_flat_depth_gives_z_dominant_normals():
    out = node.run(_flat_depth())[0]
    assert torch.allclose(out[..., 0], torch.full_like(out[..., 0], 0.5))
    assert torch.allclose(out[..., 1], torch.full_like(out[..., 1], 0.5))
    assert torch.allclose(out[..., 2], torch.ones_like(out[..., 2]))


def test_decoded_vectors_are_unit_length():
    out = node.run(_ramp_depth())[0]
    decoded = out * 2.0 - 1.0
    lengths = decoded.pow(2).sum(dim=-1).sqrt()
    assert torch.allclose(lengths, torch.ones_like(lengths))


def test_invert_flips_xy_sign_pattern():
    depth = _ramp_depth()
    base = node.run(depth, invert=False)[0]
    inverted = node.run(depth, invert=True)[0]
    assert torch.allclose(inverted[..., 0], 1.0 - base[..., 0])
    assert torch.allclose(inverted[..., 1], 1.0 - base[..., 1])
    assert torch.allclose(inverted[..., 2], base[..., 2])


def test_batch_of_two():
    depth = torch.cat([_ramp_depth(8), _flat_depth(0.2, 8)], dim=0)
    out = node.run(depth)[0]
    assert out.shape == (2, 8, 8, 3)
