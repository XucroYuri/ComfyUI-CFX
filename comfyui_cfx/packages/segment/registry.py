"""Segmentation model registry: families, local layout, and cache keys."""

import os

import folder_paths

FAMILIES = {
    "grounding-dino": {"subdir": "grounding-dino", "files": ("model.safetensors",)},
    "sam2": {"subdir": "sam2", "files": ("sam2.1_hiera_large.safetensors",)},
    "birefnet": {"subdir": "rmbg", "files": ("model.safetensors",)},
    "retinaface": {"subdir": "retinaface", "files": ("mobilenet0.25_Final.pth",)},
}


def model_root() -> str:
    return os.path.join(folder_paths.models_dir, "cfx-segment")


def family_dir(family: str) -> str:
    try:
        subdir = FAMILIES[family]["subdir"]
    except KeyError:
        raise ValueError(f"unknown segment family {family!r}") from None
    return os.path.join(model_root(), subdir)


def cache_key(family: str, path: str, precision: str = "fp16") -> tuple:
    return (family, path, precision)
