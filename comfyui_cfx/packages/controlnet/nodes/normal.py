"""Normal map from depth (deterministic finite differences)."""

import torch

from ....core.types import ensure_image


def _central_diff(depth: torch.Tensor, dim: int) -> torch.Tensor:
    """Edge-safe central differences along ``dim`` (one-sided at the borders)."""
    size = depth.shape[dim]
    grad = torch.zeros_like(depth)
    if size < 2:
        return grad
    grad.narrow(dim, 1, size - 2).copy_(
        (depth.narrow(dim, 2, size - 2) - depth.narrow(dim, 0, size - 2)) * 0.5
    )
    grad.narrow(dim, 0, 1).copy_(depth.narrow(dim, 1, 1) - depth.narrow(dim, 0, 1))
    grad.narrow(dim, size - 1, 1).copy_(depth.narrow(dim, size - 1, 1) - depth.narrow(dim, size - 2, 1))
    return grad


class CFXNormalFromDepth:
    """Estimate a tangent-space normal map from a depth map via finite differences."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                "invert": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-ControlNet/Preprocessors"

    def run(self, image, strength=1.0, invert=False):
        depth = ensure_image(image).mean(dim=-1)
        if invert:
            depth = 1.0 - depth

        dy = _central_diff(depth, dim=1)
        dx = _central_diff(depth, dim=2)

        normal = torch.stack((-dx * strength, -dy * strength, torch.ones_like(depth)), dim=-1)
        normal = normal / torch.linalg.vector_norm(normal, dim=-1, keepdim=True)
        return (((normal + 1.0) * 0.5).contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_controlnet_normal_map_from_depth": CFXNormalFromDepth,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_controlnet_normal_map_from_depth": "ComfyUI-ControlNet · Normal from Depth",
}
