"""Trim leading/trailing silence from an AUDIO waveform (behaviour reimplementation)."""

import torch


class CFXTrimSilence:
    """Keep the span between the first and last loud frame, plus ``pad_ms`` on both sides."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "threshold": ("FLOAT", {"default": 0.01, "min": 0.0, "max": 1.0, "step": 0.001}),
                "min_silence_ms": ("INT", {"default": 100, "min": 0, "max": 10000}),
                "pad_ms": ("INT", {"default": 50, "min": 0, "max": 10000}),
            },
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Audio/Process"

    def run(self, audio, threshold, min_silence_ms, pad_ms):
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]
        n = waveform.shape[-1]

        frame = max(1, round(sample_rate * min_silence_ms / 1000))
        n_frames = (n + frame - 1) // frame
        squared = waveform.pow(2)
        remainder = n_frames * frame - n
        if remainder:
            squared = torch.cat([squared, squared.new_zeros(*squared.shape[:-1], remainder)], dim=-1)
        frames = squared.reshape(*squared.shape[:-1], n_frames, frame).mean(dim=-1).sqrt()
        rms = frames.mean(dim=(0, 1))

        active = rms > threshold
        if not bool(active.any()):
            return ({"waveform": waveform, "sample_rate": sample_rate},)

        loud = active.nonzero()
        first = int(loud[0, 0])
        last = int(loud[-1, 0])

        pad = round(sample_rate * pad_ms / 1000)
        start = max(0, first * frame - pad)
        end = min(n, (last + 1) * frame + pad)
        if start == 0 and end == n:
            return ({"waveform": waveform, "sample_rate": sample_rate},)

        return ({"waveform": waveform[..., start:end].contiguous(), "sample_rate": sample_rate},)


NODE_CLASS_MAPPINGS = {
    "comfyui_audio_trim_silence": CFXTrimSilence,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_audio_trim_silence": "ComfyUI-Audio · Trim Silence",
}
