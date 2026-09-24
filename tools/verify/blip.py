"""Verify the BLIP caption node (downloads Salesforce/blip-image-captioning-base ~1 GB first run)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.vision.nodes.blip import CFXBlipCaption

_, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")

node = CFXBlipCaption()

caption = node.run(tensor, model="Salesforce/blip-image-captioning-base", mode="caption")[0]
print("caption:", caption)
assert caption, "caption is empty"

answer = node.run(
    tensor,
    model="Salesforce/blip-image-captioning-base",
    mode="interrogate",
    question="Is there a girl?",
)[0]
print("interrogate:", answer)
assert answer, "interrogate answer is empty"

print("OK")
