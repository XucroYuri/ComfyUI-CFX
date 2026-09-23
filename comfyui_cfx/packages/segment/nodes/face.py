"""Face detection + crop (RetinaFace backend reused from ComfyUI-AutoCropFaces)."""

from ..face_backend import auto_crop_faces

ASPECT_RATIOS = ["9:16", "2:3", "3:4", "4:5", "1:1", "5:4", "4:3", "3:2", "16:9"]


class CFXFaceCrop:
    """Detect faces and return cropped face images (RetinaFace)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "number_of_faces": ("INT", {"default": 5, "min": 1, "max": 100}),
                "scale_factor": ("FLOAT", {"default": 1.5, "min": 0.5, "max": 10.0, "step": 0.5}),
                "shift_factor": ("FLOAT", {"default": 0.45, "min": 0.0, "max": 1.0, "step": 0.01}),
                "aspect_ratio": (ASPECT_RATIOS, {"default": "1:1"}),
            },
            "optional": {
                "start_index": ("INT", {"default": 0, "min": 0, "max": 10000}),
                "max_faces_per_image": ("INT", {"default": 50, "min": 1, "max": 1000}),
            },
        }

    RETURN_TYPES = ("IMAGE", "CROP_DATA")
    RETURN_NAMES = ("faces", "crop_data")
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Segment/Face"

    def run(self, image, number_of_faces=5, scale_factor=1.5, shift_factor=0.45,
            aspect_ratio="1:1", start_index=0, max_faces_per_image=50):
        return auto_crop_faces(
            image=image,
            number_of_faces=number_of_faces,
            start_index=start_index,
            max_faces_per_image=max_faces_per_image,
            scale_factor=scale_factor,
            shift_factor=shift_factor,
            aspect_ratio=aspect_ratio,
        )


NODE_CLASS_MAPPINGS = {
    "comfyui_segment_face_crop": CFXFaceCrop,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_segment_face_crop": "ComfyUI-Segment · Face Crop",
}
