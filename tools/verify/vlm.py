"""Verify the VLM caption node (downloads Qwen2.5-VL-3B weights on first run)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.vision.nodes.vlm import CFXVlmCaption

_, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")

text = CFXVlmCaption().run(
    tensor,
    model="Qwen/Qwen2.5-VL-3B-Instruct",
    prompt="Describe this image in one sentence.",
    precision="bf16",
    max_new_tokens=64,
    do_sample=False,
)[0]
assert text, "VLM returned empty text"
print("caption:", text)
print("OK")
