"""Verify the WD14 tagger node (downloads wd-v1-4-moat-tagger-v2 on first run)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.vision.nodes.wd14 import CFXWD14Tagger

_, tensor = load_image(os.environ["COMFYUI_PATH"], "example.png")

tags = CFXWD14Tagger().run(tensor, model="wd-v1-4-moat-tagger-v2")[0]

print("tags:", tags[:200])

lowered = tags.lower()
expected = ("1girl", "girl", "solo", "smile")
if not tags or not any(word in lowered for word in expected):
    print(f"FAIL: none of {expected} found in tags")
    raise SystemExit(1)

print("OK")
