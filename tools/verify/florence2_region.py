"""Verify Florence-2 region refinement (region -> description / category / OCR)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.vision.nodes.florence2 import CFXFlorence2Loader
from comfyui_cfx.packages.vision.nodes.florence2_region import CFXFlorence2Region

handle = CFXFlorence2Loader().load("MiaoshouAI/Florence-2-base-PromptGen-v2.0", "fp16")[0]
image, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")
width, height = image.size

text, parsed = CFXFlorence2Region().run(
    handle, tensor,
    int(width * 0.30), int(height * 0.30), int(width * 0.70), int(height * 0.90),
    "region_to_description", max_new_tokens=64, num_beams=3,
)
print("region text:", repr(text)[:200])
print("OK")
