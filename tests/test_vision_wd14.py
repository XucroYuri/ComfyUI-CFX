import numpy as np
import pytest
from PIL import Image

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision import wd14


def test_prepare_image_shape_and_dtype():
    prepared = wd14.prepare_image(Image.new("RGB", (8, 4), (255, 0, 0)), 16)
    assert prepared.shape == (16, 16, 3)
    assert prepared.dtype == np.float32


def test_prepare_image_pads_with_white():
    prepared = wd14.prepare_image(Image.new("RGB", (8, 4), (0, 0, 0)), 8)
    assert prepared[0, 0].min() >= 250


def test_prepare_image_square_is_not_padded():
    prepared = wd14.prepare_image(Image.new("RGB", (8, 8), (255, 0, 0)), 8)
    blue, green, red = prepared[4, 4]
    assert red > 250 and green < 5 and blue < 5


def test_select_tags_applies_dual_thresholds():
    rows = [("1girl", 0), ("solo", 0), ("hatsune_miku", 4), ("low", 0)]
    probs = [0.9, 0.2, 0.9, 0.1]
    general, character = wd14.select_tags(rows, probs, 0.35, 0.85)
    assert general == ["1girl"]
    assert character == ["hatsune_miku"]


def test_select_tags_sorted_by_score():
    rows = [("a", 0), ("b", 0)]
    probs = [0.4, 0.9]
    general, _ = wd14.select_tags(rows, probs, 0.35, 0.85)
    assert general == ["b", "a"]


def test_format_tags_replaces_underscore_and_excludes():
    assert wd14.format_tags(["hatsune_miku", "1girl"]) == "hatsune miku, 1girl"
    assert wd14.format_tags(["hatsune_miku", "1girl"], exclude="miku") == "1girl"


def test_load_tag_rows(tmp_path):
    csv_path = tmp_path / "tags.csv"
    csv_path.write_text("name,category,count\n1girl,0,10\nmiku,4,2\n", encoding="utf-8")
    assert wd14.load_tag_rows(str(csv_path)) == [("1girl", 0), ("miku", 4)]


def test_model_files_layout():
    onnx_path, csv_path = wd14.model_files("wd-v1-4-moat-tagger-v2")
    assert onnx_path.endswith("model.onnx")
    assert csv_path.endswith("selected_tags.csv")
