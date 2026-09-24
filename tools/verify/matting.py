"""Verify Matting via rembg (downloads the u2net model on first run)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.segment.nodes.matting import CFXMatting

image, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")
width, height = image.size

mask, rgba = CFXMatting().run(tensor, model="u2net")

assert mask.ndim == 3 and mask.shape[0] == 1, f"unexpected mask shape {tuple(mask.shape)}"
assert tuple(mask.shape[1:]) == (height, width), (
    f"mask spatial size {tuple(mask.shape[1:])} != input image {(height, width)}"
)
assert float(mask.min()) >= 0.0 and float(mask.max()) <= 1.0, (
    f"mask out of [0, 1]: min={float(mask.min())} max={float(mask.max())}"
)
assert (mask <= 0.01).any() and (mask >= 0.99).any(), "mask is constant"

assert rgba.shape == (1, height, width, 4), f"unexpected rgba shape {tuple(rgba.shape)}"

coverage = float((mask > 0.5).float().mean())
print("mask shape:", tuple(mask.shape))
print("coverage: %.3f" % coverage)
print("rgba shape:", tuple(rgba.shape))
print("OK")
