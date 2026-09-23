"""Shared helpers for the verification scripts.

Each script bootstraps the ComfyUI-CFX package inside a ComfyUI environment.
Set ``COMFYUI_PATH`` to the ComfyUI directory that has the required custom nodes
installed (e.g. comfyui-florence2 / ComfyUI-segment-anything-2 / ComfyUI-AutoCropFaces).
"""

import importlib.util
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def bootstrap(comfy_path=None):
    comfy = Path(comfy_path or os.environ.get("COMFYUI_PATH", ""))
    if not comfy.is_dir():
        raise SystemExit("set COMFYUI_PATH to your ComfyUI directory before running this script")
    sys.path.insert(0, str(comfy))
    os.chdir(comfy)

    spec = importlib.util.spec_from_file_location(
        "ComfyUI-CFX", REPO / "__init__.py", submodule_search_locations=[str(REPO)]
    )
    package = importlib.util.module_from_spec(spec)
    sys.modules["ComfyUI-CFX"] = package
    spec.loader.exec_module(package)
    return comfy


def load_image(comfy, name):
    import torchvision.transforms.functional as F
    from PIL import Image

    image = Image.open(Path(comfy) / "input" / name).convert("RGB")
    tensor = F.to_tensor(image).unsqueeze(0).permute(0, 2, 3, 1).contiguous().float()
    return image, tensor
