"""WD14 booru tagger helpers.

Pure helpers (image preparation, threshold selection, formatting) are separated
from the ONNX session so they stay testable without a model file.
"""

import csv
import os

import numpy as np
from PIL import Image

import folder_paths

GENERAL_CATEGORY = 0
CHARACTER_CATEGORY = 4

WD14_MODELS = (
    "wd-v1-4-moat-tagger-v2",
    "wd-v1-4-convnext-tagger-v2",
    "wd-v1-4-swinv2-tagger-v3",
    "wd-eva02-large-tagger-v3",
    "wd-vit-tagger-v3",
)

_SESSIONS = {}


def model_dir() -> str:
    return os.path.join(folder_paths.models_dir, "wd14_tagger")


def model_files(model: str) -> tuple:
    root = os.path.join(model_dir(), model)
    return os.path.join(root, "model.onnx"), os.path.join(root, "selected_tags.csv")


def download_model(model: str) -> tuple:
    """Download any missing ``model.onnx`` / ``selected_tags.csv`` from SmilingWolf."""
    onnx_path, csv_path = model_files(model)
    missing = [
        (filename, target)
        for filename, target in (("model.onnx", onnx_path), ("selected_tags.csv", csv_path))
        if not os.path.exists(target)
    ]
    if not missing:
        return onnx_path, csv_path
    from huggingface_hub import hf_hub_download

    repo = f"SmilingWolf/{model}"
    os.makedirs(os.path.dirname(onnx_path), exist_ok=True)
    for filename, target in missing:
        hf_hub_download(repo_id=repo, filename=filename, local_dir=os.path.dirname(target))
    return onnx_path, csv_path


def get_session(model: str):
    """Return a cached ONNX session for ``model``."""
    onnx_path, _ = download_model(model)
    if onnx_path not in _SESSIONS:
        import onnxruntime

        providers = onnxruntime.get_available_providers()
        provider = "CUDAExecutionProvider" if "CUDAExecutionProvider" in providers else "CPUExecutionProvider"
        _SESSIONS[onnx_path] = onnxruntime.InferenceSession(onnx_path, providers=[provider])
    return _SESSIONS[onnx_path]


def load_tag_rows(csv_path: str) -> list:
    """Read ``selected_tags.csv`` into ``[(name, category), ...]``."""
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append((row["name"], int(row["category"])))
    return rows


def prepare_image(image: Image.Image, size: int) -> np.ndarray:
    """Pad to square with white, resize to ``size``, return float32 HWC BGR in [0,255]."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    side = max(width, height)
    canvas = Image.new("RGB", (side, side), (255, 255, 255))
    canvas.paste(rgb, ((side - width) // 2, (side - height) // 2))
    canvas = canvas.resize((size, size), Image.BICUBIC)
    return np.asarray(canvas, dtype=np.float32)[:, :, ::-1]


def select_tags(rows: list, probs, general_threshold: float, character_threshold: float) -> tuple:
    """Split scored rows into (general, character) name lists, highest score first."""
    general = []
    character = []
    for (name, category), prob in zip(rows, probs):
        score = float(prob)
        if category == GENERAL_CATEGORY and score >= general_threshold:
            general.append((name, score))
        elif category == CHARACTER_CATEGORY and score >= character_threshold:
            character.append((name, score))
    general.sort(key=lambda item: -item[1])
    character.sort(key=lambda item: -item[1])
    return [name for name, _ in general], [name for name, _ in character]


def format_tags(names, replace_underscore: bool = True, exclude: str = "") -> str:
    excluded = [item.strip().lower() for item in (exclude or "").split(",") if item.strip()]
    tags = []
    for name in names:
        tag = name.replace("_", " ") if replace_underscore else name
        if excluded and any(item in tag.lower() for item in excluded):
            continue
        tags.append(tag)
    return ", ".join(tags)
