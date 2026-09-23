"""Migration tool: rewrite old node ids in a workflow JSON to cfx node ids."""

import argparse
import json
import sys

# Best-effort map from replaced plugins' node ids to cfx node ids.
MAPPING = {
    # primitives
    "Image Resize": "comfyui_primitives_image_resize",
    "ImageResize+": "comfyui_primitives_image_resize",
    "Image Crop Location": "comfyui_primitives_image_crop",
    "ImageCrop+": "comfyui_primitives_image_crop",
    "Image Stitch": "comfyui_primitives_image_stitch",
    "Image Input Switch": "comfyui_primitives_switch",
    "Text Concatenate": "comfyui_primitives_text",
    "MathExpression|pysssss": "comfyui_primitives_math",
    "SimpleMath+": "comfyui_primitives_math",
    "ImageBatchToImageList": "comfyui_primitives_image_split",
    "ImageBatchMultiple+": "comfyui_primitives_image_batch",
    "SDXLEmptyLatentSizePicker+": "comfyui_primitives_resolution",
    "MaskFix+": "comfyui_primitives_mask_ops",
    # flow
    "ShowText|pysssss": "comfyui_flow_show_text",
    "StringFunction|pysssss": "comfyui_flow_string_function",
    "ConstrainImage|pysssss": "comfyui_flow_constrain_image",
    "LoadText|pysssss": "comfyui_flow_load_text",
    "SaveText|pysssss": "comfyui_flow_save_text",
    # vision
    "WD14Tagger|pysssss": "comfyui_vision_wd14_tagger",
    "Florence2Run": "comfyui_vision_florence2_run",
    "BLIP Model Loader": "comfyui_vision_blip_caption",
    "BLIP Analyze Image": "comfyui_vision_blip_caption",
}

# Nodes that the new libraries intentionally do not replace.
DEPRECATED = {
    "AILab_Florence2": "use comfyui_vision_florence2_run (rmbg's copy is GPL and duplicated)",
    "Qwen3VLCaptionBridge": "broken; remove (see cfx survey)",
}


def migrate_workflow(workflow: dict):
    """Return ``(migrated_workflow, report)``; input is not mutated."""
    report = {"mapped": {}, "deprecated": {}, "unknown": {}}
    migrated = json.loads(json.dumps(workflow))

    nodes = migrated.get("nodes")
    if isinstance(nodes, list):
        for node in nodes:
            _migrate_node(node, report)

    if "prompt" in migrated and isinstance(migrated["prompt"], dict):
        for value in migrated["prompt"].values():
            if isinstance(value, dict):
                _migrate_class_type(value, report)

    return migrated, report


def _migrate_node(node: dict, report: dict) -> None:
    class_type = node.get("type") or node.get("class_type")
    if not class_type:
        return
    new_type = _resolve(class_type, report)
    if new_type:
        if "type" in node:
            node["type"] = new_type
        if "class_type" in node:
            node["class_type"] = new_type


def _migrate_class_type(entry: dict, report: dict) -> None:
    class_type = entry.get("class_type")
    if not class_type:
        return
    new_type = _resolve(class_type, report)
    if new_type:
        entry["class_type"] = new_type


def _resolve(class_type: str, report: dict):
    if class_type in MAPPING:
        report["mapped"][class_type] = MAPPING[class_type]
        return MAPPING[class_type]
    if class_type in DEPRECATED:
        report["deprecated"][class_type] = DEPRECATED[class_type]
        return None
    report["unknown"].setdefault(class_type, 0)
    report["unknown"][class_type] += 1
    return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Migrate old ComfyUI nodes to cfx node ids")
    parser.add_argument("workflow", help="workflow JSON path")
    parser.add_argument("-o", "--output", help="write migrated workflow here")
    args = parser.parse_args(argv)

    with open(args.workflow, encoding="utf-8") as handle:
        workflow = json.load(handle)

    migrated, report = migrate_workflow(workflow)
    print("mapped:", json.dumps(report["mapped"], indent=2, ensure_ascii=False))
    print("deprecated:", json.dumps(report["deprecated"], indent=2, ensure_ascii=False))
    print("unmapped node types:", json.dumps(report["unknown"], indent=2, ensure_ascii=False))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(migrated, handle, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
