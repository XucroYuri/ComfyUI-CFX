import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.flow.nodes import text_file as text_file_node

saver = text_file_node.CFXSaveText()
loader = text_file_node.CFXLoadText()


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("CFX_TEXT_DIRS", str(tmp_path))
    saver.save("hello", "notes/a.txt")
    assert loader.load("notes/a.txt") == ("hello",)


def test_append_mode(tmp_path, monkeypatch):
    monkeypatch.setenv("CFX_TEXT_DIRS", str(tmp_path))
    saver.save("a", "x.txt")
    saver.save("b", "x.txt", mode="append")
    assert loader.load("x.txt")[0] == "ab"


def test_overwrite_mode(tmp_path, monkeypatch):
    monkeypatch.setenv("CFX_TEXT_DIRS", str(tmp_path))
    saver.save("a", "x.txt")
    saver.save("b", "x.txt")
    assert loader.load("x.txt")[0] == "b"


def test_resolve_rejects_traversal(tmp_path, monkeypatch):
    monkeypatch.setenv("CFX_TEXT_DIRS", str(tmp_path))
    with pytest.raises(ValueError):
        text_file_node.resolve("../outside.txt")


def test_resolve_rejects_absolute(tmp_path, monkeypatch):
    monkeypatch.setenv("CFX_TEXT_DIRS", str(tmp_path))
    with pytest.raises(ValueError):
        text_file_node.resolve(str(tmp_path / "outside.txt"))


def test_missing_file_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("CFX_TEXT_DIRS", str(tmp_path))
    with pytest.raises(FileNotFoundError):
        loader.load("nope.txt")
