import struct

import pytest

pytest.importorskip("folder_paths")

import folder_paths

from comfyui_cfx.packages.loaders.nodes import quant as quant_node

node = quant_node.CFXGgufHeader()


def write_gguf(path, version=3, tensor_count=2, metadata_kv_count=5, magic=b"GGUF"):
    data = (
        magic
        + struct.pack("<I", version)
        + struct.pack("<Q", tensor_count)
        + struct.pack("<Q", metadata_kv_count)
    )
    path.write_bytes(data)
    return path


def test_parse_header(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "models_dir", str(tmp_path))
    write_gguf(tmp_path / "model.gguf", version=3, tensor_count=7, metadata_kv_count=11)
    assert node.run("model.gguf") == (
        {"magic": "GGUF", "version": 3, "tensor_count": 7, "metadata_kv_count": 11},
    )


def test_parse_v2_header(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "models_dir", str(tmp_path))
    write_gguf(tmp_path / "model.gguf", version=2, tensor_count=0, metadata_kv_count=1)
    (info,) = node.run("model.gguf")
    assert info["magic"] == "GGUF"
    assert info["version"] == 2


def test_bad_magic_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "models_dir", str(tmp_path))
    write_gguf(tmp_path / "model.gguf", magic=b"NOPE")
    with pytest.raises(ValueError, match="not a GGUF file"):
        node.run("model.gguf")


def test_truncated_header_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "models_dir", str(tmp_path))
    (tmp_path / "model.gguf").write_bytes(b"GGUF" + struct.pack("<I", 3))
    with pytest.raises(ValueError, match="truncated"):
        node.run("model.gguf")


def test_traversal_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "models_dir", str(tmp_path))
    with pytest.raises(ValueError):
        node.run("../evil.gguf")
