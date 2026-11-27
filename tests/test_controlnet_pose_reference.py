import importlib.util
from io import BytesIO
from pathlib import Path
from urllib.request import HTTPRedirectHandler

import pytest
from PIL import Image

LIBRARY = Path(__file__).resolve().parents[1] / "comfyui_cfx/packages/controlnet/pose_library.py"
SPEC = importlib.util.spec_from_file_location("pose_library", LIBRARY)
pose_library = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pose_library)


def test_catalog_and_offline_diagram(tmp_path):
    assert len(pose_library.labels()) == 100
    image, row, entry = pose_library.load("pose_step", "auto", tmp_path)
    assert image.mode == "RGB" and image.size == (768, 1024)
    assert "stride" in pose_library.prompts(row, entry)[1]
    assert not list(tmp_path.iterdir())
    with pytest.raises(ValueError, match="unavailable"):
        pose_library.resolve("pose_step", "side")


def test_offline_and_local_override(tmp_path, monkeypatch):
    monkeypatch.setattr(pose_library, "build_opener", lambda *_: pytest.fail("unexpected network access"))
    with pytest.raises(FileNotFoundError):
        pose_library.load("full_single_P001", "diag", tmp_path)
    Image.new("RGB", (16, 24), "white").save(tmp_path / "full_single_P001_diag.png")
    image, _, _ = pose_library.load("full_single_P001", "diag", tmp_path, online=True)
    assert image.size == (16, 24)


def test_online_cache(tmp_path, monkeypatch):
    image = BytesIO()
    Image.new("RGB", (12, 18)).save(image, format="WEBP")
    calls = []

    class Opener:
        def open(self, request, timeout):
            calls.append(request.full_url)
            return BytesIO(image.getvalue())

    def opener(handler):
        assert isinstance(handler, HTTPRedirectHandler)
        assert handler.redirect_request(None, None, 302, None, None, "https://example.org") is None
        return Opener()

    monkeypatch.setattr(pose_library, "build_opener", opener)
    for online in (True, False):
        result, _, _ = pose_library.load("full_single_P001", "diag", tmp_path, online=online)
        assert result.size == (12, 18)
    assert calls == ["https://posewear.pages.dev/p/i/full_single_P001_diag.webp"]


def test_override_cannot_escape_cache(tmp_path):
    outside = tmp_path / "outside.png"
    Image.new("RGB", (16, 16)).save(outside)
    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "full_single_P001_diag.png").symlink_to(outside)
    with pytest.raises(ValueError, match="escapes"):
        pose_library.load("full_single_P001", "diag", cache)
