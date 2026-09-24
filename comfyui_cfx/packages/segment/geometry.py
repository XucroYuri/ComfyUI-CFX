"""Pure rasterization of detection annotations into masks."""

import numpy as np
from PIL import Image, ImageDraw


def _canvas(width: int, height: int) -> Image.Image:
    return Image.new("L", (max(1, int(width)), max(1, int(height))), 0)


def boxes_to_mask(boxes, height: int, width: int, line_width: int = 0) -> np.ndarray:
    """Rasterize ``[x0, y0, x1, y1]`` boxes; ``line_width=0`` fills them."""
    canvas = _canvas(width, height)
    draw = ImageDraw.Draw(canvas)
    for box in boxes:
        x0, y0, x1, y1 = (float(value) for value in box[:4])
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        if line_width and line_width > 0:
            draw.rectangle([x0, y0, x1, y1], outline=255, width=int(line_width))
        else:
            draw.rectangle([x0, y0, x1, y1], fill=255)
    return np.asarray(canvas, dtype=np.float32) / 255.0


def polygons_to_mask(polygons, height: int, width: int) -> np.ndarray:
    """Rasterize polygons given as sequences of ``[x, y]`` points."""
    canvas = _canvas(width, height)
    draw = ImageDraw.Draw(canvas)
    for polygon in polygons:
        points = [(float(point[0]), float(point[1])) for point in polygon]
        if len(points) >= 3:
            draw.polygon(points, fill=255)
    return np.asarray(canvas, dtype=np.float32) / 255.0


def annotations_to_mask(annotations, height: int, width: int, line_width: int = 0) -> np.ndarray:
    """Convert a Florence-2 style annotation dict (``bboxes`` or ``polygons``) to a mask."""
    if not isinstance(annotations, dict):
        raise ValueError("annotations must be a dict with 'bboxes' or 'polygons'")
    if annotations.get("polygons"):
        return polygons_to_mask(annotations["polygons"], height, width)
    if annotations.get("bboxes"):
        return boxes_to_mask(annotations["bboxes"], height, width, line_width)
    raise ValueError("annotations contain neither 'bboxes' nor 'polygons'")


def annotations_to_box_batch(annotations) -> list:
    """Convert annotation bboxes into the per-image batch shape SAM2 expects."""
    if not isinstance(annotations, dict) or not annotations.get("bboxes"):
        raise ValueError("annotations must contain 'bboxes'")
    boxes = [[float(value) for value in box[:4]] for box in annotations["bboxes"]]
    return [boxes]


def mask_to_bboxes(mask, threshold: float = 0.5, multiple_of: int = 1) -> list:
    """Invert :func:`boxes_to_mask`: bbox of pixels ``> threshold`` per ``[B, H, W]`` item.

    Boxes are ``[x0, y0, x1, y1]`` with exclusive ``x1``/``y1``, grown OUTWARD to
    ``multiple_of`` and clamped to the image. An empty item contributes no entry.
    """
    array = np.asarray(mask, dtype=np.float32)
    if array.ndim != 3:
        raise ValueError(f"mask must be [B,H,W], got shape {array.shape}")
    step = max(1, int(multiple_of))
    boxes = []
    for item in array:
        height, width = item.shape
        ys, xs = np.nonzero(item > threshold)
        if xs.size == 0:
            continue
        x0 = (int(xs.min()) // step) * step
        y0 = (int(ys.min()) // step) * step
        x1 = -(-(int(xs.max()) + 1) // step) * step
        y1 = -(-(int(ys.max()) + 1) // step) * step
        x0 = max(0, min(x0, width))
        y0 = max(0, min(y0, height))
        x1 = max(0, min(x1, width))
        y1 = max(0, min(y1, height))
        boxes.append({"bbox": [x0, y0, x1, y1], "area": (x1 - x0) * (y1 - y0)})
    return boxes
