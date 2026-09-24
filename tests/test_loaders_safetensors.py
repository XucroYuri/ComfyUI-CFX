import pytest

pytest.importorskip("folder_paths")
pytest.importorskip("safetensors")
pytest.importorskip("torch")

import folder_paths
import torch
from safetensors.torch import save_file

from comfyui_cfx.packages.loaders.nodes import safetensors_info as node_module

node = node_module.CFXSafetensorsInfo()


def test_info_counts_dtypes_metadata(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "models_dir", str(tmp_path))
    save_file(
        {"a": torch.zeros(2), "b": torch.zeros(2, dtype=torch.int8)},
        str(tmp_path / "model.safetensors"),
        metadata={"x": "1"},
    )

    (info,) = node.run("model.safetensors")

    assert info["tensor_count"] == 2
    assert info["dtypes"] == {"F32": 1, "I8": 1}
    assert info["metadata_keys"] == ["x"]


def test_traversal_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "models_dir", str(tmp_path))
    with pytest.raises(ValueError):
        node.run("../evil.safetensors")


def test_non_safetensors_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "models_dir", str(tmp_path))
    (tmp_path / "bad.safetensors").write_bytes(b"not a safetensors file at all")
    with pytest.raises(ValueError):
        node.run("bad.safetensors")
