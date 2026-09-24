import torch

from comfyui_cfx.packages.depth3d.nodes import colormap as colormap_node

node = colormap_node.CFXDepthColormap()


def test_output_shape_and_dtype():
    out = node.run(torch.rand(2, 8, 8, 3), "turbo")[0]
    assert out.shape == (2, 8, 8, 3)
    assert out.dtype == torch.float32
    assert out.is_contiguous()


def test_output_in_unit_range():
    out = node.run(torch.rand(2, 8, 8, 1), "viridis")[0]
    assert float(out.min()) >= 0.0
    assert float(out.max()) <= 1.0


def test_gray_replicates_normalized_depth():
    image = torch.linspace(0.1, 0.9, steps=16).reshape(1, 4, 4, 1)
    out = node.run(image, "gray", normalize=True)[0]
    depth = image.mean(dim=-1)
    expected = (depth - depth.amin(dim=(1, 2), keepdim=True)) / (
        depth.amax(dim=(1, 2), keepdim=True) - depth.amin(dim=(1, 2), keepdim=True)
    )
    for channel in range(3):
        assert torch.allclose(out[..., channel], expected.squeeze(0), atol=1e-6)


def test_different_colormaps_differ():
    image = torch.linspace(0.0, 1.0, steps=16).reshape(1, 4, 4, 1)
    turbo = node.run(image, "turbo")[0]
    viridis = node.run(image, "viridis")[0]
    assert not torch.allclose(turbo, viridis)


def test_constant_image_is_finite_and_constant():
    image = torch.full((1, 4, 4, 3), 0.7)
    out = node.run(image, "turbo", normalize=True)[0]
    assert torch.isfinite(out).all()
    assert torch.allclose(out, out[0, 0, 0].expand_as(out))
    assert float(out.min()) >= 0.0
    assert float(out.max()) <= 1.0


def test_normalize_false_clamps_out_of_range():
    image = torch.tensor([-2.0, 0.5, 3.0]).reshape(1, 1, 3, 1)
    out = node.run(image, "gray", normalize=False)[0]
    assert torch.isfinite(out).all()
    assert float(out.min()) >= 0.0
    assert float(out.max()) <= 1.0
    assert torch.allclose(out[0, 0, :, 0], torch.tensor([0.0, 0.5, 1.0]))
