"""Map a depth map to a colorized RGB IMAGE via matplotlib colormaps."""

import torch

from ....core.types import ensure_image


class CFXDepthColormap:
    """Turn a single-channel depth estimate into a colorized RGB image."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "colormap": (
                    ["gray", "turbo", "viridis", "magma", "inferno", "plasma"],
                    {"default": "turbo"},
                ),
                "normalize": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Depth3D/Process"

    def run(self, image, colormap="turbo", normalize=True):
        img = ensure_image(image)
        depth = img.mean(dim=-1)

        if normalize:
            dmin = depth.amin(dim=(1, 2), keepdim=True)
            dmax = depth.amax(dim=(1, 2), keepdim=True)
            span = dmax - dmin
            scaled = (depth - dmin) / span.clamp_min(torch.finfo(depth.dtype).eps)
            depth = torch.where(span > 0, scaled, torch.zeros_like(depth))
        else:
            depth = depth.clamp(0.0, 1.0)

        if colormap == "gray":
            out = depth.unsqueeze(-1).repeat(1, 1, 1, 3)
        else:
            from matplotlib import colormaps

            rgb = colormaps[colormap](depth.numpy())[..., :3]
            out = torch.from_numpy(rgb).to(depth.dtype)

        return (out.contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_depth3d_colormap": CFXDepthColormap,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_depth3d_colormap": "ComfyUI-Depth3D · Colormap",
}
