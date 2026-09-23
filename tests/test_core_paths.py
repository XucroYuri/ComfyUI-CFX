import pytest

pytest.importorskip("folder_paths")

from comfyui_cfx.core import paths


def test_safe_join_accepts_relative(tmp_path):
    joined = paths.safe_join(str(tmp_path), "sub/file.txt")
    assert joined.startswith(str(tmp_path))


def test_safe_join_rejects_traversal(tmp_path):
    with pytest.raises(ValueError):
        paths.safe_join(str(tmp_path), "../evil.txt")


def test_safe_join_rejects_absolute(tmp_path):
    with pytest.raises(ValueError):
        paths.safe_join(str(tmp_path), "C:/Windows/system32")


def test_safe_filename_rejects_separators():
    with pytest.raises(ValueError):
        paths.safe_filename("a/b.txt")


def test_safe_filename_accepts_plain():
    assert paths.safe_filename("out.png") == "out.png"
