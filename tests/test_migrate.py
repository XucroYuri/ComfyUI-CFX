from tools import migrate


def test_maps_type_in_nodes_list():
    workflow = {"nodes": [{"type": "Image Resize", "id": 1}]}
    migrated, report = migrate.migrate_workflow(workflow)
    assert migrated["nodes"][0]["type"] == "comfyui_primitives_image_resize"
    assert report["mapped"]["Image Resize"] == "comfyui_primitives_image_resize"


def test_maps_class_type_in_api_prompt():
    workflow = {"prompt": {"1": {"class_type": "StringFunction|pysssss", "inputs": {}}}}
    migrated, report = migrate.migrate_workflow(workflow)
    assert migrated["prompt"]["1"]["class_type"] == "comfyui_flow_string_function"


def test_deprecated_nodes_reported_but_unchanged():
    workflow = {"nodes": [{"type": "Qwen3VLCaptionBridge"}]}
    migrated, report = migrate.migrate_workflow(workflow)
    assert "Qwen3VLCaptionBridge" in report["deprecated"]
    assert migrated["nodes"][0]["type"] == "Qwen3VLCaptionBridge"


def test_unknown_nodes_counted():
    workflow = {"nodes": [{"type": "KSampler"}, {"type": "KSampler"}]}
    _, report = migrate.migrate_workflow(workflow)
    assert report["unknown"]["KSampler"] == 2


def test_input_workflow_is_not_mutated():
    workflow = {"nodes": [{"type": "Image Resize"}]}
    migrate.migrate_workflow(workflow)
    assert workflow["nodes"][0]["type"] == "Image Resize"
