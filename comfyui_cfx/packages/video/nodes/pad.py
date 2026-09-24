"""Pad an image batch up to a target frame count (behaviour reimplementation)."""

import torch

from ....core.types import ensure_image


class CFXPadFrames:
    """Grow ``image`` along the batch dim to exactly ``count`` frames."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "count": ("INT", {"default": 81, "min": 1, "max": 100000}),
                "mode": (["repeat_last", "loop"], {"default": "repeat_last"}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Video/Frames"

    def run(self, image, count, mode):
        img = ensure_image(image)
        batch = img.shape[0]
        if batch >= count:
            return (img,)
        if batch == 0:
            raise ValueError("pad_frames: empty image batch")

        missing = count - batch
        if mode == "repeat_last":
            pad = torch.cat([img[-1:]] * missing, dim=0)
        elif mode == "loop":
            chunks = []
            taken = 0
            while taken < missing:
                take = min(batch, missing - taken)
                chunks.append(img[:take])
                taken += take
            pad = torch.cat(chunks, dim=0)
        else:
            raise ValueError(f"pad_frames: unknown mode {mode!r}")

        return (torch.cat((img, pad), dim=0).contiguous(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_video_pad_frames": CFXPadFrames,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_video_pad_frames": "ComfyUI-Video · Pad Frames",
}
