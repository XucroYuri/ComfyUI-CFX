import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.vision import backend, registry
from comfyui_cfx.packages.vision.nodes import florence2 as florence2_node


def test_run_task_choices_match_registry():
    choices = florence2_node.CFXFlorence2Run.INPUT_TYPES()["required"]["task"][0]
    assert set(choices) == set(registry.FLORENCE2_TASKS)


def test_loader_exposes_models_and_precisions():
    required = florence2_node.CFXFlorence2Loader.INPUT_TYPES()["required"]
    assert "MiaoshouAI/Florence-2-base-PromptGen-v2.0" in required["model"][0]
    assert required["precision"][0] == ["fp16", "bf16", "fp32"]


def test_backend_points_at_florence2_node():
    assert backend.backend_dir().endswith("comfyui-florence2")


def test_backend_custom_nodes_env_override(monkeypatch):
    monkeypatch.setenv("CFX_FLORENCE2_DIR", "X:/somewhere/custom_nodes")
    assert backend.backend_dir().replace("\\", "/") == "X:/somewhere/custom_nodes/comfyui-florence2"


def test_missing_backend_raises_clear_error(monkeypatch):
    monkeypatch.setenv("CFX_FLORENCE2_DIR", "Z:/definitely/missing")
    with pytest.raises(FileNotFoundError):
        backend.load_florence2("unused", None)
