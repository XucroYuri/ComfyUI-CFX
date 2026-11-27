"""Select an image conditioning reference from the PoseWear catalog."""

from pathlib import Path

import numpy as np
import torch

from ....core.types import ensure_image
from ..pose_library import labels, load, prompts, resolve


class CFXPoseReferencePicker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pose": (list(labels()),),
                "view": (["auto", "front", "diag", "side", "high", "low", "diagram"],),
                "source_mode": (["offline", "on demand"],),
            }
        }

    CATEGORY = "ComfyUI-ControlNet/References"
    FUNCTION = "pick"
    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("reference_image", "prompt_zh", "prompt_en", "source")

    @classmethod
    def VALIDATE_INPUTS(cls, pose, view):
        try:
            resolve(labels()[pose], view)
        except (KeyError, ValueError) as exc:
            return str(exc)
        return True

    @classmethod
    def IS_CHANGED(cls, pose, view, source_mode):
        return float("nan")

    def pick(self, pose, view, source_mode):
        # Keep the ControlNet registry importable in the ComfyUI-free test suite.
        import folder_paths

        from ....core.paths import safe_join

        root = Path(folder_paths.get_input_directory()).resolve()
        cache = Path(safe_join(str(root), "posewear"))
        if not cache.resolve().is_relative_to(root):
            raise ValueError("PoseWear cache escapes the ComfyUI input directory")
        image, row, entry = load(labels()[pose], view, cache, online=source_mode == "on demand")
        value = torch.from_numpy(np.asarray(image, dtype=np.float32) / 255).unsqueeze(0)
        return (ensure_image(value), *prompts(row, entry), row["source"])


NODE_CLASS_MAPPINGS = {"comfyui_controlnet_pick_pose": CFXPoseReferencePicker}
NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_controlnet_pick_pose": "ComfyUI-ControlNet · Pose Reference Picker (PoseWear)",
}
