"""Tests for the Florence-2 region node (pure helpers + prompt construction)."""

import re

import pytest
import torch

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision.nodes import florence2_region as node


def _capture(monkeypatch):
    seen = {}

    def fake(florence2, image, prompt, parse_task, max_new_tokens, num_beams, do_sample):
        seen.update(
            prompt=prompt,
            parse_task=parse_task,
            max_new_tokens=max_new_tokens,
            num_beams=num_beams,
            do_sample=do_sample,
        )
        return "out", {"ok": True}

    monkeypatch.setattr(node, "run_florence2", fake)
    return seen


def test_quantize_edges():
    assert node.quantize(0, 100) == 0
    assert node.quantize(100, 100) == 999
    assert node.quantize(999, 100) == 999
    assert node.quantize(10, 0) == 0


def test_quantize_mid_value():
    assert node.quantize(50, 100) == 500
    assert node.quantize(1, 4) == 250


def test_loc_string_format_and_components():
    encoded = node.loc_string(0, 1, 20, 10, 20, 10)
    assert re.fullmatch(r"(<loc_\d+>){4}", encoded)
    assert encoded == "<loc_0><loc_100><loc_999><loc_999>"


def test_tasks_keys_match_task_combo():
    required = node.CFXFlorence2Region.INPUT_TYPES()["required"]
    assert list(node.TASKS) == required["task"][0]
    assert required["task"][1]["default"] == "region_to_description"


def test_inverted_box_raises_value_error():
    image = torch.zeros(1, 10, 20, 3)
    with pytest.raises(ValueError):
        node.CFXFlorence2Region().run(None, image, 5, 5, 4, 6)


def test_all_zero_box_uses_full_image(monkeypatch):
    seen = _capture(monkeypatch)
    node.CFXFlorence2Region().run(None, torch.zeros(1, 10, 20, 3))
    token = node.TASKS["region_to_description"]
    assert seen["prompt"] == token + node.loc_string(0, 0, 20, 10, 20, 10)


def test_run_builds_prompt_and_returns_backend_output(monkeypatch):
    seen = _capture(monkeypatch)
    result = node.CFXFlorence2Region().run(None, torch.zeros(1, 10, 20, 3), 2, 3, 12, 8)
    token = node.TASKS["region_to_description"]
    assert seen["prompt"] == token + node.loc_string(2, 3, 12, 8, 20, 10)
    assert seen["parse_task"] == token
    assert seen["max_new_tokens"] == 256
    assert seen["num_beams"] == 3
    assert seen["do_sample"] is False
    assert result == ("out", {"ok": True})


def test_box_is_clamped_to_image(monkeypatch):
    seen = _capture(monkeypatch)
    node.CFXFlorence2Region().run(None, torch.zeros(1, 10, 20, 3), -5, -5, 100, 100)
    token = node.TASKS["region_to_description"]
    assert seen["prompt"] == token + node.loc_string(0, 0, 20, 10, 20, 10)


def test_unknown_task_raises_value_error():
    with pytest.raises(ValueError):
        node.CFXFlorence2Region().run(None, torch.zeros(1, 10, 20, 3), task="bogus")

def test_strip_loc_tokens_removes_echoed_locations():
    assert node.strip_loc_tokens("a cat<loc_299><loc_299><loc_699><loc_900>") == "a cat"
    assert node.strip_loc_tokens("cat, <loc_1><loc_2>") == "cat"
    assert node.strip_loc_tokens("plain text") == "plain text"


def test_run_cleans_echoed_loc_tokens(monkeypatch):
    monkeypatch.setattr(node, "run_florence2", lambda *a, **k: ("cat<loc_5><loc_6>", "cat<loc_5><loc_6>"))
    text, parsed = node.CFXFlorence2Region().run(None, torch.zeros(1, 10, 20, 3), 1, 1, 5, 5)
    assert text == "cat"
    assert parsed == "cat"
