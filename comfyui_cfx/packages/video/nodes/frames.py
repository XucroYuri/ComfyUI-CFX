"""Select a frame range from an image batch (behaviour reimplementation)."""

from ....core.types import ensure_image


class CFXFrameRange:
    """Slice ``image[start:stop:step]`` along the batch dimension."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "start": ("INT", {"default": 0, "min": 0, "max": 100000}),
                "stop": ("INT", {"default": -1, "min": -1, "max": 100000}),
                "step": ("INT", {"default": 1, "min": 1, "max": 1000}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Video/Frames"

    def run(self, image, start, stop, step):
        image = ensure_image(image)
        batch = image.shape[0]
        stop = batch if stop < 0 or stop > batch else stop
        start = min(max(start, 0), batch)
        if start >= stop:
            raise ValueError("frame_range: empty range")
        return (image[start:stop:step].contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_video_frame_range": CFXFrameRange,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_video_frame_range": "ComfyUI-Video · Frame Range",
}
