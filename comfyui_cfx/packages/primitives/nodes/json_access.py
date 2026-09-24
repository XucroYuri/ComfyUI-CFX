"""JSON access primitives."""


def _entries(annotations, index):
    """Select the detection entry list and whether it holds polygons."""
    if not isinstance(annotations, dict):
        raise ValueError(f"annotations must be a dict, got {type(annotations).__name__}")
    if "bboxes" in annotations:
        entries, polygon = annotations["bboxes"], False
    elif "polygons" in annotations:
        entries, polygon = annotations["polygons"], True
    else:
        raise ValueError("annotations must contain 'bboxes' or 'polygons' (0 entries available)")

    count = len(entries)
    if index < 0 or index >= count:
        noun = "entry" if count == 1 else "entries"
        raise ValueError(f"index {index} out of range; {count} {noun} available")
    return entries[index], polygon


def _corners(entry, polygon):
    """Reduce a box or polygon to its four enclosing, normalized integer corners."""
    if polygon:
        xs = [float(point[0]) for point in entry]
        ys = [float(point[1]) for point in entry]
    else:
        xs = [float(entry[0]), float(entry[2])]
        ys = [float(entry[1]), float(entry[3])]
    return round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys))


class CFXJsonBBox:
    """Extract one ``[x0, y0, x1, y1]`` box from a detection dict as four INTs."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "annotations": ("JSON",),
                "index": ("INT", {"default": 0, "min": 0, "max": 4096}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT", "JSON")
    RETURN_NAMES = ("x0", "y0", "x1", "y1", "bbox")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Primitives/JSON"

    def run(self, annotations, index=0):
        entry, polygon = _entries(annotations, index)
        x0, y0, x1, y1 = _corners(entry, polygon)
        return (x0, y0, x1, y1, {"bbox": [x0, y0, x1, y1], "index": index})


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_json_bbox": CFXJsonBBox,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_json_bbox": "ComfyUI-Primitives · JSON BBox",
}
