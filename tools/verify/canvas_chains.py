"""Cross-node chain verification: run real multi-node graphs through ComfyUI.

Chain A (Vision):      LoadImage -> Florence-2 run(region_proposal) -> JSON BBox -> Florence-2 Region -> Save Text
Chain B (Segment):     LoadImage -> SAM2 + Text-to-Mask -> Mask to SEGS -> SEGS to Mask -> Mask to BBox -> Save Text
Chain C (cross-pack):  LoadImage -> Florence-2 run(region_proposal) -> Annotations to Mask -> SEgs round-trip -> Save Text

Usage:
    set COMFYUI_PATH=D:\\path\\to\\ComfyUI
    python tools\\verify\\canvas_chains.py [base_url]
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

BASE = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CFX_BASE_URL", "http://127.0.0.1:8199")).rstrip("/")
COMFY = Path(os.environ["COMFYUI_PATH"])
RUN_ID = uuid.uuid4().hex[:8]
INFO = {}

FLORENCE = "MiaoshouAI/Florence-2-base-PromptGen-v2.0"
DETECT = "IDEA-Research/grounding-dino-tiny"
SAM2 = "sam2.1_hiera_tiny.safetensors"

EXPECTED = (
    "comfyui_primitives_json_bbox",
    "comfyui_flow_save_text",
    "comfyui_vision_florence2_loader",
    "comfyui_vision_florence2_run",
    "comfyui_vision_florence2_region",
    "comfyui_segment_sam2_loader",
    "comfyui_segment_text_to_mask",
    "comfyui_segment_mask_to_segs",
    "comfyui_segment_segs_to_mask",
    "comfyui_segment_mask_to_bbox",
)

VISION_REGION = {
    "1": {"class_type": "LoadImage", "inputs": {"image": "example.png"}},
    "2": {"class_type": "comfyui_vision_florence2_loader", "inputs": {"model": FLORENCE, "precision": "fp16"}},
    "3": {"class_type": "comfyui_vision_florence2_run", "inputs": {
        "florence2": ["2", 0], "image": ["1", 0], "task": "region_caption",
        "max_new_tokens": 128, "num_beams": 3, "do_sample": False}},
    "4": {"class_type": "comfyui_primitives_json_bbox", "inputs": {"annotations": ["3", 1], "index": 0}},
    "5": {"class_type": "comfyui_vision_florence2_region", "inputs": {
        "florence2": ["2", 0], "image": ["1", 0],
        "x0": ["4", 0], "y0": ["4", 1], "x1": ["4", 2], "y1": ["4", 3],
        "task": "region_to_description", "max_new_tokens": 64, "num_beams": 3}},
    "6": {"class_type": "comfyui_flow_save_text", "inputs": {
        "text": ["5", 0], "path": "cfx_chain_region.txt", "mode": "overwrite"}},
}

SEGMENT_CHAIN = {
    "1": {"class_type": "LoadImage", "inputs": {"image": "example.png"}},
    "2": {"class_type": "comfyui_segment_sam2_loader", "inputs": {
        "model": SAM2, "segmentor": "single_image", "precision": "fp16"}},
    "3": {"class_type": "comfyui_segment_text_to_mask", "inputs": {
        "image": ["1", 0], "prompt": "girl. dress.", "detect_model": DETECT,
        "box_threshold": 0.25, "text_threshold": 0.20, "sam2": ["2", 0]}},
    "4": {"class_type": "comfyui_segment_mask_to_segs", "inputs": {"image": ["1", 0], "mask": ["3", 0]}},
    "5": {"class_type": "comfyui_segment_segs_to_mask", "inputs": {"segs": ["4", 0]}},
    "6": {"class_type": "comfyui_segment_mask_to_bbox", "inputs": {"mask": ["5", 0]}},
    "7": {"class_type": "comfyui_flow_save_text", "inputs": {
        "text": ["6", 1], "path": "cfx_chain_segs.txt", "mode": "overwrite"}},
}

CROSS_CHAIN = {
    "1": {"class_type": "LoadImage", "inputs": {"image": "example.png"}},
    "2": {"class_type": "comfyui_vision_florence2_loader", "inputs": {"model": FLORENCE, "precision": "fp16"}},
    "3": {"class_type": "comfyui_vision_florence2_run", "inputs": {
        "florence2": ["2", 0], "image": ["1", 0], "task": "region_caption",
        "max_new_tokens": 128, "num_beams": 3, "do_sample": False}},
    "4": {"class_type": "comfyui_segment_annotations_to_mask", "inputs": {"annotations": ["3", 1], "image": ["1", 0]}},
    "5": {"class_type": "comfyui_segment_mask_to_segs", "inputs": {"image": ["1", 0], "mask": ["4", 0]}},
    "6": {"class_type": "comfyui_segment_segs_to_mask", "inputs": {"segs": ["5", 0]}},
    "7": {"class_type": "comfyui_segment_mask_to_bbox", "inputs": {"mask": ["6", 0]}},
    "8": {"class_type": "comfyui_flow_save_text", "inputs": {
        "text": ["7", 1], "path": "cfx_chain_cross.txt", "mode": "overwrite"}},
}


def get_json(path):
    with urllib.request.urlopen(f"{BASE}{path}", timeout=30) as response:
        return json.loads(response.read())


def post_prompt(graph):
    payload = json.dumps({"prompt": graph, "client_id": "cfx-chains"}).encode()
    request = urllib.request.Request(f"{BASE}/prompt", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read())["prompt_id"]
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"/prompt rejected: {exc.read().decode('utf-8', 'replace')[:800]}") from exc


def wait_for(prompt_id, timeout=1800):
    deadline = time.time() + timeout
    while time.time() < deadline:
        history = get_json(f"/history/{prompt_id}")
        entry = history.get(prompt_id)
        if entry:
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(f"prompt {prompt_id} failed: {_error_detail(status)}")
            if entry.get("outputs") or status.get("status_str") == "success":
                return entry
        time.sleep(2)
    raise TimeoutError(f"prompt {prompt_id} did not finish within {timeout}s")


def _error_detail(status):
    for name, payload in status.get("messages", []):
        if name == "execution_error":
            return f"{payload.get('node_type')}({payload.get('node_id')}): {payload.get('exception_message')}"
    return "unknown error"


def run_chain(name, graph, output_base, validate):
    output_name = f"{output_base}_{RUN_ID}.txt"
    target = COMFY / "output" / "text" / output_name
    entry = wait_for(post_prompt(_with_output(graph, output_name)))
    assert entry.get("outputs"), f"{name}: workflow produced no outputs"
    assert target.is_file(), f"{name}: expected {target} (unique name busts ComfyUI's node cache)"
    text = target.read_text(encoding="utf-8").strip()
    assert text, f"{name}: empty output"
    validate(text)
    print(f"{name}: {text[:170]}")


def _with_output(graph, output_name):
    """Fill GUI defaults for every required input, then give Save Text a per-run filename."""
    graph = json.loads(json.dumps(graph))
    for node in graph.values():
        required = INFO.get(node.get("class_type"), {}).get("input", {}).get("required", {})
        for field, declaration in required.items():
            if field in node["inputs"] or not isinstance(declaration, list) or len(declaration) < 2:
                continue
            options = declaration[1] if isinstance(declaration[1], dict) else {}
            default = options.get("default")
            if default is None and isinstance(declaration[0], list) and declaration[0]:
                default = declaration[0][0]
            if default is not None:
                node["inputs"][field] = default
        if node.get("class_type") == "comfyui_flow_save_text":
            node["inputs"]["path"] = output_name
    return graph


def main():
    info = get_json("/object_info")
    INFO.update(info)
    missing = [node for node in EXPECTED if node not in info]
    if missing:
        raise AssertionError(f"nodes not registered in ComfyUI: {missing}")
    print(f"object_info: {len(info)} node types; all {len(EXPECTED)} chain nodes present")

    run_chain("vision_region", VISION_REGION, "cfx_chain_region.txt",
              lambda text: _no_loc_tokens(text))
    run_chain("segment_chain", SEGMENT_CHAIN, "cfx_chain_segs.txt",
              lambda text: _has_boxes(text))
    run_chain("cross_pack", CROSS_CHAIN, "cfx_chain_cross.txt",
              lambda text: _has_boxes(text))
    print("canvas chains OK")


def _no_loc_tokens(text):
    assert "<loc_" not in text, f"region output still echoes loc tokens: {text[:120]!r}"


def _has_boxes(text):
    assert "box(es)" in text, f"expected a bbox summary, got {text[:120]!r}"


if __name__ == "__main__":
    main()
