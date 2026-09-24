"""Stitch a processed crop back into the original image (inverse of crop_by_mask)."""

from ....core.types import ensure_image

_CROP_KEYS = ("x", "y", "width", "height", "original_width", "original_height")


class CFXStitchCrop:
    """Paste a processed crop back into the base image at its crop rectangle."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "cropped": ("IMAGE",),
                "crop_data": ("JSON",),
            },
            "optional": {
                "mask": ("MASK",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Inpaint/Crop"

    def run(self, image, cropped, crop_data, mask=None):
        base = ensure_image(image)
        patch = ensure_image(cropped)
        _, base_h, base_w, _ = base.shape

        for key in _CROP_KEYS:
            if key not in crop_data:
                raise ValueError(f"stitch: crop_data is missing '{key}'")

        if int(crop_data["original_width"]) != base_w or int(crop_data["original_height"]) != base_h:
            raise ValueError(
                "stitch: crop_data original size "
                f"{crop_data['original_width']}x{crop_data['original_height']} "
                f"does not match base image {base_w}x{base_h}"
            )

        x = int(crop_data["x"])
        y = int(crop_data["y"])
        width = int(crop_data["width"])
        height = int(crop_data["height"])

        if patch.shape[1] != height or patch.shape[2] != width:
            raise ValueError(
                f"stitch: cropped patch {patch.shape[1]}x{patch.shape[2]} does not match crop_data {height}x{width}"
            )

        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(base_w, x + width)
        y1 = min(base_h, y + height)

        out = base.clone()
        if x1 <= x0 or y1 <= y0:
            return (out,)

        px0 = x0 - x
        py0 = y0 - y
        sub = patch[:, py0:py0 + (y1 - y0), px0:px0 + (x1 - x0), :]

        if mask is None:
            out[:, y0:y1, x0:x1, :] = sub
            return (out,)

        m = mask.float()
        if m.dim() == 3:
            m = m[0]
        elif m.dim() != 2:
            raise ValueError(f"stitch: mask must be 2D or 3D, got shape {tuple(mask.shape)}")

        if m.shape == (base_h, base_w):
            m = m[y0:y1, x0:x1]
        elif m.shape == (height, width):
            m = m[py0:py0 + (y1 - y0), px0:px0 + (x1 - x0)]
        else:
            raise ValueError(f"stitch: mask {tuple(m.shape)} does not match crop_data {height}x{width}")

        m = m.clamp(0.0, 1.0).unsqueeze(0).unsqueeze(-1)
        region = out[:, y0:y1, x0:x1, :]
        out[:, y0:y1, x0:x1, :] = region * (1.0 - m) + sub * m
        return (out,)


NODE_CLASS_MAPPINGS = {
    "comfyui_inpaint_stitch": CFXStitchCrop,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_inpaint_stitch": "ComfyUI-Inpaint · Stitch",
}
