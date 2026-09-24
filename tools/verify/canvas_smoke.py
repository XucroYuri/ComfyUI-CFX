"""Canvas smoke test: submit real workflows to a running ComfyUI and check the results.

This is the in-ComfyUI equivalent of building the graph on the canvas: it verifies that
ComfyUI loads the plugin, registers all nodes, and that two real chains execute end to end.

Usage:
    set COMFYUI_PATH=D:\\path\\to\\ComfyUI
    python tools\\verify\\canvas_smoke.py            # default http://127.0.0.1:8199
    python tools\\verify\\canvas_smoke.py http://127.0.0.1:8199
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CFX_BASE_URL", "http://127.0.0.1:8199")).rstrip("/")
COMFY = Path(os.environ["COMFYUI_PATH"]) if os.environ.get("COMFYUI_PATH") else None

EXPECTED = (
    "comfyui_primitives_image_resize",
    "comfyui_primitives_text",
    "comfyui_primitives_save_image_metadata",
    "comfyui_flow_save_text",
    "comfyui_vision_florence2_loader",
    "comfyui_vision_florence2_run",
    "comfyui_vision_tags_filter",
    "comfyui_segment_sam2_loader",
    "comfyui_inpaint_crop_by_mask",
)

WORKFLOW_PRIMITIVES = {
    "1": {"class_type": "LoadImage", "inputs": {"image": "example.png"}},
    "2": {"class_type": "comfyui_primitives_image_resize", "inputs": {
        "image": ["1", 0], "mode": "stretch", "width": 256, "height": 256, "multiple_of": 8}},
    "3": {"class_type": "comfyui_primitives_text", "inputs": {
        "operation": "concat", "delimiter": " | ", "clean_whitespace": True, "skip_empty": True,
        "search": "", "replace": "", "text1": "cfx", "text2": "canvas smoke"}},
    "4": {"class_type": "comfyui_primitives_save_image_metadata", "inputs": {
        "images": ["2", 0], "filename_prefix": "cfx_smoke", "positive": "cfx", "negative": "",
        "format": "png", "quality": 95, "embed_workflow": True, "save_metadata_txt": True}},
    "5": {"class_type": "comfyui_flow_save_text", "inputs": {
        "text": ["3", 0], "path": "cfx_smoke.txt", "mode": "overwrite"}},
}

WORKFLOW_FLORENCE = {
    "1": {"class_type": "LoadImage", "inputs": {"image": "example.png"}},
    "2": {"class_type": "comfyui_vision_florence2_loader", "inputs": {
        "model": "MiaoshouAI/Florence-2-base-PromptGen-v2.0", "precision": "fp16"}},
    "3": {"class_type": "comfyui_vision_florence2_run", "inputs": {
        "florence2": ["2", 0], "image": ["1", 0], "task": "tags",
        "max_new_tokens": 128, "num_beams": 3, "do_sample": False}},
    "4": {"class_type": "comfyui_vision_tags_filter", "inputs": {
        "tags": ["3", 0], "include": "", "exclude": "", "delimiter": ", ",
        "case_sensitive": False, "max_tags": 8}},
    "5": {"class_type": "comfyui_flow_save_text", "inputs": {
        "text": ["4", 0], "path": "cfx_tags.txt", "mode": "overwrite"}},
}


def get_json(path):
    with urllib.request.urlopen(f"{BASE}{path}", timeout=30) as response:
        return json.loads(response.read())


def post_prompt(graph):
    payload = json.dumps({"prompt": graph, "client_id": "cfx-smoke"}).encode()
    request = urllib.request.Request(f"{BASE}/prompt", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read())["prompt_id"]


def wait_for(prompt_id, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        history = get_json(f"/history/{prompt_id}")
        if prompt_id in history:
            entry = history[prompt_id]
            status = entry.get("status", {})
            if status.get("completed") or status.get("status_str") == "success" or entry.get("outputs"):
                return entry
        time.sleep(2)
    raise TimeoutError(f"prompt {prompt_id} did not finish within {timeout}s")


def main():
    info = get_json("/object_info")
    missing = [node for node in EXPECTED if node not in info]
    if missing:
        raise AssertionError(f"nodes not registered in ComfyUI: {missing}")
    print(f"object_info: {len(info)} node types; all {len(EXPECTED)} sampled cfx nodes present")

    primitives = wait_for(post_prompt(WORKFLOW_PRIMITIVES))
    print("primitives workflow outputs:", sorted(primitives["outputs"].keys()))
    image_outputs = primitives["outputs"].get("4", {}).get("images", [])
    assert image_outputs, "save_image_metadata produced no image"
    name = image_outputs[0]["filename"]
    if COMFY:
        saved = COMFY / "output" / image_outputs[0].get("subfolder", "") / name
        assert saved.is_file(), f"expected saved image at {saved}"
        text_file = COMFY / "output" / "text" / "cfx_smoke.txt"
        assert text_file.is_file() and text_file.read_text(encoding="utf-8").strip() == "cfx | canvas smoke", text_file
    print(f"primitives workflow OK (saved {name})")

    florence = wait_for(post_prompt(WORKFLOW_FLORENCE))
    assert florence.get("outputs"), "florence-2 workflow produced no outputs"
    if COMFY:
        tags_file = COMFY / "output" / "text" / "cfx_tags.txt"
        assert tags_file.is_file(), f"missing {tags_file}"
        tags = tags_file.read_text(encoding="utf-8").strip()
        assert tags, "florence-2 produced no tags"
        print("florence-2 tags:", tags[:160])
    print("canvas smoke OK")


if __name__ == "__main__":
    main()
