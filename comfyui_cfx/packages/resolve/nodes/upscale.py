"""Tiled model upscaling (UltimateSDUpscale-style) over ComfyUI's upscale runner."""

import torch
from comfy_extras.nodes_upscale_model import ImageUpscaleWithModel

from ....core.types import ensure_image


def tile_ranges(length: int, tile: int, overlap: int) -> list[tuple[int, int]]:
    """Half-open ``[start, end)`` windows covering ``range(length)``.

    Consecutive windows are ``tile - overlap`` apart. The last window is moved back
    so it keeps width ``tile`` whenever the axis is longer than a tile.
    """
    if tile >= length:
        return [(0, length)]
    step = max(1, tile - overlap)
    ranges = []
    start = 0
    while start < length:
        end = min(start + tile, length)
        ranges.append((start, end))
        if end >= length:
            break
        start += step
    last_start, last_end = ranges[-1]
    if last_start + tile > length:
        ranges[-1] = (length - tile, last_end)
    return ranges


def _axis_weights(length: int, start: int, total: int, feather: int) -> torch.Tensor:
    """Feather weights for one output axis: interior edges ramp 0→1, borders stay 1."""
    weights = torch.ones(length, dtype=torch.float32)
    if feather <= 0:
        return weights
    feather = min(feather, length)
    ramp = torch.linspace(0.0, 1.0, feather)
    if start > 0:
        weights[:feather] = ramp
    if start + length < total:
        weights[length - feather:] = ramp.flip(0)
    return weights


class CFXUpscaleTiled:
    """Upscale the first image of a batch by running the model over feathered tiles."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "upscale_model": ("UPSCALE_MODEL",),
                "image": ("IMAGE",),
                "tile_size": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "overlap": ("INT", {"default": 32, "min": 0, "max": 512}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Resolve/Upscale"

    def run(self, upscale_model, image, tile_size=512, overlap=32):
        if overlap >= tile_size:
            raise ValueError(f"overlap ({overlap}) must be smaller than tile_size ({tile_size})")

        source = ensure_image(image)[0]  # only the first image of the batch is processed
        in_h, in_w, channels = source.shape
        rows = tile_ranges(in_h, tile_size, overlap)
        cols = tile_ranges(in_w, tile_size, overlap)

        upscaler = ImageUpscaleWithModel()
        canvas = acc = None

        for y0, y1 in rows:
            for x0, x1 in cols:
                upscaled = upscaler.upscale(upscale_model, source[y0:y1, x0:x1].unsqueeze(0))
                if upscaled.shape[1] == 0 or upscaled.shape[2] == 0:
                    raise ValueError("upscale model returned an empty tile")

                if canvas is None:
                    scale = upscaled.shape[2] / (x1 - x0)
                    out_h, out_w = round(in_h * scale), round(in_w * scale)
                    feather = round(overlap * scale)
                    canvas = torch.zeros(out_h, out_w, channels)
                    acc = torch.zeros(out_h, out_w, 1)

                oy, ox = round(y0 * scale), round(x0 * scale)
                tile_h = min(upscaled.shape[1], out_h - oy)
                tile_w = min(upscaled.shape[2], out_w - ox)
                wy = _axis_weights(upscaled.shape[1], oy, out_h, feather)[:tile_h]
                wx = _axis_weights(upscaled.shape[2], ox, out_w, feather)[:tile_w]
                weight = (wy[:, None] * wx[None, :]).unsqueeze(-1)
                canvas[oy:oy + tile_h, ox:ox + tile_w] += upscaled[0, :tile_h, :tile_w] * weight
                acc[oy:oy + tile_h, ox:ox + tile_w] += weight

        return ((canvas / acc.clamp(min=1e-8)).unsqueeze(0),)


NODE_CLASS_MAPPINGS = {
    "comfyui_resolve_upscale_tiled": CFXUpscaleTiled,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_resolve_upscale_tiled": "ComfyUI-Resolve · Upscale (Tiled)",
}
