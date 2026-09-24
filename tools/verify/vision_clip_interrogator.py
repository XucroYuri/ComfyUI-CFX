"""Verify CLIP Interrogator (downloads CLIP + BLIP models on first use)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.vision.nodes.clip_interrogator import CFXClipInterrogator

_, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")
text = CFXClipInterrogator().run(tensor, clip_model="ViT-L-14/openai", mode="fast", max_flavors=4)[0]
assert text and text.strip(), "interrogator returned empty text"
print("text:", text[:200])
print("OK")
