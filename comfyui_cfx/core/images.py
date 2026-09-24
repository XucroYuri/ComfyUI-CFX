"""Image <-> PIL conversion shared by the model-loading nodes."""

import numpy as np
from PIL import Image

from .types import ensure_image


def first_image_to_pil(image) -> Image.Image:
    """Clamp the first image of a batch to [0,1] and return a uint8 PIL image."""
    array = ensure_image(image)[0].clamp(0, 1).cpu().numpy()
    return Image.fromarray((array * 255.0).round().astype(np.uint8))
