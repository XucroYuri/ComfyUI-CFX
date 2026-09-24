import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.video.nodes import pad as pad_node

node = pad_node.CFXPadFrames()


def make_batch(batch=4, height=3, width=2, channels=3):
    index = torch.arange(batch, dtype=torch.float32).reshape(batch, 1, 1, 1)
    return index.expand(batch, height, width, channels).contiguous()


def frame_ids(image):
    return image[:, 0, 0, 0].tolist()


def test_pads_up_to_count():
    out = node.run(make_batch(4), 10, "repeat_last")[0]
    assert out.shape == (10, 3, 2, 3)


def test_repeat_last_duplicates_last_frame():
    img = make_batch(4)
    out = node.run(img, 9, "repeat_last")[0]
    assert frame_ids(out) == [0, 1, 2, 3, 3, 3, 3, 3, 3]
    assert torch.equal(out[4:], img[-1:].expand(5, -1, -1, -1))


def test_loop_cycles_from_start():
    out = node.run(make_batch(3), 8, "loop")[0]
    assert frame_ids(out) == [0, 1, 2, 0, 1, 2, 0, 1]


def test_loop_first_padded_frame_equals_first_frame():
    img = make_batch(3)
    out = node.run(img, 7, "loop")[0]
    assert torch.equal(out[3], img[0])


def test_batch_at_count_returns_unchanged_shape():
    img = make_batch(6)
    out = node.run(img, 6, "loop")[0]
    assert out.shape == (6, 3, 2, 3)


def test_batch_above_count_is_not_truncated():
    img = make_batch(6)
    out = node.run(img, 3, "repeat_last")[0]
    assert out.shape == (6, 3, 2, 3)


def test_original_frames_are_untouched():
    img = make_batch(4)
    for mode in ("repeat_last", "loop"):
        out = node.run(img, 11, mode)[0]
        assert torch.equal(out[:4], img)


def test_output_is_contiguous_bhwc():
    out = node.run(make_batch(4), 10, "loop")[0]
    assert out.dim() == 4
    assert out.is_contiguous()


def test_empty_batch_raises():
    with pytest.raises(ValueError, match="empty image batch"):
        node.run(torch.zeros(0, 3, 2, 3), 5, "repeat_last")


def test_unknown_mode_raises():
    with pytest.raises(ValueError, match="unknown mode"):
        node.run(make_batch(2), 5, "bogus")
