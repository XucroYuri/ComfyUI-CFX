"""Image cropping primitives."""

from ....core.types import ensure_image


class CFXImageCrop:
    """Crop by pixel box or by insets, clamped to stay inside the image."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mode": (["pixel", "inset"], {"default": "pixel"}),
            },
            "optional": {
                "x": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "y": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "width": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "height": ("INT", {"default": 0, "min": 0, "max": 16384}),
                "left": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 16384.0}),
                "right": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 16384.0}),
                "top": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 16384.0}),
                "bottom": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 16384.0}),
                "inset_unit": (["px", "percent"], {"default": "px"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height")
    FUNCTION = "crop"
    CATEGORY = "ComfyUI-Primitives/Image"

    def crop(self, image, mode, x=0, y=0, width=0, height=0,
             left=0.0, right=0.0, top=0.0, bottom=0.0, inset_unit="px"):
        img = ensure_image(image)
        _, in_h, in_w, _ = img.shape

        if mode == "pixel":
            x0 = min(max(int(x), 0), in_w - 1)
            y0 = min(max(int(y), 0), in_h - 1)
            box_w = int(width) if width > 0 else in_w - x0
            box_h = int(height) if height > 0 else in_h - y0
            x1 = min(in_w, x0 + box_w)
            y1 = min(in_h, y0 + box_h)
        else:
            if inset_unit == "percent":
                left, right = left / 100.0 * in_w, right / 100.0 * in_w
                top, bottom = top / 100.0 * in_h, bottom / 100.0 * in_h
            x0 = min(max(int(round(left)), 0), in_w - 1)
            y0 = min(max(int(round(top)), 0), in_h - 1)
            x1 = min(in_w, max(x0 + 1, int(round(in_w - right))))
            y1 = min(in_h, max(y0 + 1, int(round(in_h - bottom))))

        cropped = img[:, y0:y1, x0:x1, :].contiguous()
        return (cropped, x1 - x0, y1 - y0)


NODE_CLASS_MAPPINGS = {
    "comfyui_primitives_image_crop": CFXImageCrop,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_primitives_image_crop": "ComfyUI-Primitives · Image Crop",
}
