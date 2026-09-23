"""Verify the Florence-2 loader + run nodes (needs comfyui-florence2 + model weights)."""

from _common import bootstrap, load_image

bootstrap()

from comfyui_cfx.packages.vision.nodes.florence2 import CFXFlorence2Loader, CFXFlorence2Run

handle = CFXFlorence2Loader().load("MiaoshouAI/Florence-2-base-PromptGen-v2.0", "fp16")[0]
print("loaded:", handle["path"])

_, tensor = load_image(__import__("os").environ.get("COMFYUI_PATH"), "example.png")
run = CFXFlorence2Run()
for task in ("tags", "more_detailed_caption"):
    text, _ = run.run(handle, tensor, task, max_new_tokens=256, num_beams=3)
    assert text, f"{task} returned empty text"
    print(f"{task}: {text[:120]}")

_, parsed = run.run(handle, tensor, "region_proposal", max_new_tokens=128, num_beams=3)
assert isinstance(parsed, dict), "detection task should return a dict"
print("region_proposal keys:", sorted(parsed))
print("OK")
