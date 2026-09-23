import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import batch as batch_node

batcher = batch_node.CFXImageBatch()
splitter = batch_node.CFXImageSplit()


def test_batch_two_images():
    out = batcher.batch(image1=torch.rand(1, 8, 8, 3), image2=torch.rand(1, 8, 8, 3))[0]
    assert out.shape == (2, 8, 8, 3)


def test_batch_single_passthrough():
    only = torch.rand(1, 8, 8, 3)
    assert torch.equal(batcher.batch(image1=only)[0], only)


def test_batch_no_input_raises():
    with pytest.raises(ValueError):
        batcher.batch()


def test_batch_size_mismatch_raises():
    with pytest.raises(ValueError):
        batcher.batch(image1=torch.rand(1, 8, 8, 3), image2=torch.rand(1, 4, 8, 3))


def test_split_produces_single_image_items():
    items = splitter.split(torch.rand(3, 8, 8, 3))[0]
    assert len(items) == 3
    assert all(item.shape == (1, 8, 8, 3) for item in items)


def test_split_preserves_order():
    source = torch.rand(2, 4, 4, 3)
    items = splitter.split(source)[0]
    assert torch.equal(items[0][0], source[0])
    assert torch.equal(items[1][0], source[1])
