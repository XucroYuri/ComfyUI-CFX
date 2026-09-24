"""Verify BLIP-2 captioning (downloads the 350m checkpoint on first use)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.vision.nodes.blip2 import CFXBlip2Caption

_, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")
text = CFXBlip2Caption().run(
    tensor, model="Salesforce/blip2-opt-350m", mode="caption", max_new_tokens=32, precision="bf16"
)[0]
assert text and text.strip(), "blip2 returned empty text"
print("caption:", text[:200])
print("OK")
