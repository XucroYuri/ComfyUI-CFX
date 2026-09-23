"""VLM caption node (Qwen2.5/3-VL via native transformers)."""

from PIL import Image

from ....core.device import resolve_dtype
from ....core.types import ensure_image
from ..vlm import VLM_MODELS, build_messages, load


class CFXVlmCaption:
    """Caption an image with a native-transformers VLM (Qwen2.5-VL / Qwen3-VL)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (list(VLM_MODELS), {"default": VLM_MODELS[0]}),
                "prompt": ("STRING", {
                    "default": "Describe the image in detail.",
                    "multiline": True,
                }),
                "precision": (["bf16", "fp16", "fp32"], {"default": "bf16"}),
                "max_new_tokens": ("INT", {"default": 256, "min": 1, "max": 4096}),
                "do_sample": ("BOOLEAN", {"default": False}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.05}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Vision/VLM"

    def run(self, image, model, prompt, precision="bf16", max_new_tokens=256,
            do_sample=False, temperature=0.7):
        dtype = resolve_dtype(precision)
        processor, network = load(model, dtype)
        device = network.device

        first = ensure_image(image)[0].cpu().numpy()
        pil = Image.fromarray((first.clamp(0, 1).numpy() * 255.0).round().astype("uint8"))

        messages = build_messages(prompt)
        text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = processor(text=[text], images=[pil], return_tensors="pt").to(device).to(dtype)

        generated = network.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature if do_sample else None,
        )
        trimmed = generated[:, inputs["input_ids"].shape[1]:]
        return (processor.batch_decode(trimmed, skip_special_tokens=True)[0].strip(),)


NODE_CLASS_MAPPINGS = {
    "comfyui_vision_vlm_caption": CFXVlmCaption,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_vision_vlm_caption": "ComfyUI-Vision · VLM Caption",
}
