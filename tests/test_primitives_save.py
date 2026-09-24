import pytest
import torch

pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import save as save_node


def test_validate_prefix_defaults_when_empty():
    assert save_node.validate_prefix("") == "ComfyUI-CFX"


def test_validate_prefix_rejects_parent_segments():
    with pytest.raises(ValueError):
        save_node.validate_prefix("../evil")


def test_validate_prefix_rejects_absolute_path(tmp_path):
    with pytest.raises(ValueError):
        save_node.validate_prefix(str(tmp_path / "out.png"))


def test_validate_prefix_allows_subfolder():
    assert save_node.validate_prefix("batch/set1") == "batch/set1"


def test_save_writes_one_file_per_image(tmp_path, monkeypatch):
    monkeypatch.setattr(save_node, "output_dir", lambda: str(tmp_path))
    monkeypatch.setattr(
        save_node.folder_paths,
        "get_save_image_path",
        lambda prefix, folder, width, height: (str(tmp_path), "img", 1, "", prefix),
    )
    node = save_node.CFXSaveImageMetadata()
    result = node.save(torch.rand(2, 8, 8, 3), "test", "positive", "negative")

    names = sorted(path.name for path in tmp_path.iterdir())
    assert names == ["img_00001_.png", "img_00002_.png"]
    assert result["ui"]["images"][0]["filename"] == "img_00001_.png"
