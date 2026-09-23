import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision import registry


def test_task_token_mapping():
    assert registry.task_token("tags") == "<GENERATE_TAGS>"
    assert registry.task_token("more_detailed_caption") == "<MORE_DETAILED_CAPTION>"
    assert registry.task_token("ocr") == "<OCR>"


def test_task_token_unknown_raises():
    with pytest.raises(ValueError):
        registry.task_token("does_not_exist")


def test_is_text_task():
    assert registry.is_text_task("<GENERATE_TAGS>")
    assert registry.is_text_task("<ANALYZE>")
    assert not registry.is_text_task("<OD>")
    assert not registry.is_text_task("<REGION_PROPOSAL>")


def test_cache_key_is_stable_and_complete():
    assert registry.cache_key("florence2", "/m", "fp16") == ("florence2", "/m", "fp16", "none")
    assert registry.cache_key("florence2", "/m", "fp16", "int8") == ("florence2", "/m", "fp16", "int8")


def test_models_include_promptgen_v2():
    assert "MiaoshouAI/Florence-2-base-PromptGen-v2.0" in registry.FLORENCE2_MODELS
