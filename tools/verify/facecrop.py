"""Verify FaceCrop (needs ComfyUI-AutoCropFaces; weights ship with that plugin)."""

import os

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.segment.nodes.face import CFXFaceCrop

node = CFXFaceCrop()
for name in ("example.png", "kaffi.jpg", "bridge.jpg"):
    image, tensor = load_image(os.environ["COMFYUI_PATH"], name)
    faces, crop_data = node.run(tensor, number_of_faces=5, aspect_ratio="1:1")
    shape = tuple(faces.shape) if hasattr(faces, "shape") else type(faces).__name__
    print(f"{name}: input={image.size} faces={shape} crop_data={len(crop_data) if crop_data else 0}")
print("OK")
