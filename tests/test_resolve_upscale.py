import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.resolve.nodes import upscale as upscale_node  # noqa: E402

node = upscale_node.CFXUpscaleTiled()
tile_ranges = upscale_node.tile_ranges


class _StubUpscaler:
    """Deterministic 2x nearest-neighbour upscale standing in for a real model.

    Real ComfyUI's ``ImageUpscaleWithModel.upscale`` returns a ``NodeOutput`` whose
    ``[0]`` yields the tensor, so the stub mirrors that one-tuple contract.
    """

    def upscale(self, model, image):
        bchw = image.permute(0, 3, 1, 2)
        out = torch.nn.functional.interpolate(bchw, scale_factor=2.0, mode="nearest")
        return (out.permute(0, 2, 3, 1),)


@pytest.fixture
def stub_upscaler(monkeypatch):
    monkeypatch.setattr(upscale_node, "ImageUpscaleWithModel", _StubUpscaler)
    return _StubUpscaler


def _nearest_reference(image):
    bchw = image.permute(2, 0, 1).unsqueeze(0)
    out = torch.nn.functional.interpolate(bchw, scale_factor=2.0, mode="nearest")
    return out[0].permute(1, 2, 0)


def test_tile_ranges_single_window_when_tile_covers_axis():
    assert tile_ranges(40, 64, 8) == [(0, 40)]
    assert tile_ranges(64, 64, 8) == [(0, 64)]


def test_tile_ranges_exact_split_without_overlap():
    assert tile_ranges(128, 64, 0) == [(0, 64), (64, 128)]


def test_tile_ranges_cover_every_index():
    covered = set()
    for start, end in tile_ranges(100, 40, 10):
        assert 0 <= start < end <= 100
        covered.update(range(start, end))
    assert covered == set(range(100))


def test_tile_ranges_last_window_ends_at_length():
    ranges = tile_ranges(100, 40, 5)
    assert ranges == [(0, 40), (35, 75), (60, 100)]
    assert ranges[-1][1] == 100


def test_run_matches_whole_image_nearest(stub_upscaler):
    image = torch.rand(1, 24, 24, 3)
    (out,) = node.run(object(), image, tile_size=16, overlap=4)
    assert out.shape == (1, 48, 48, 3)
    assert torch.allclose(out[0], _nearest_reference(image[0]), atol=1e-6)


def test_run_matches_reference_across_irregular_tiles(stub_upscaler):
    image = torch.rand(1, 30, 50, 3)
    (out,) = node.run(object(), image, tile_size=16, overlap=6)
    assert out.shape == (1, 60, 100, 3)
    assert torch.allclose(out[0], _nearest_reference(image[0]), atol=1e-6)


def test_run_processes_only_first_image(stub_upscaler):
    image = torch.rand(2, 20, 20, 3)
    (out,) = node.run(object(), image, tile_size=16, overlap=4)
    assert out.shape == (1, 40, 40, 3)


def test_overlap_not_smaller_than_tile_raises(stub_upscaler):
    with pytest.raises(ValueError, match="overlap"):
        node.run(object(), torch.rand(1, 32, 32, 3), tile_size=64, overlap=64)
