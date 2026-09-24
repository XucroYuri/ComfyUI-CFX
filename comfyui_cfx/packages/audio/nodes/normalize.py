"""Normalize an AUDIO waveform toward a target dBFS level (behaviour reimplementation)."""


class CFXNormalizeAudio:
    """Scale a waveform so its peak or RMS lands at ``target_dbfs``, never clipping."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "target_dbfs": ("FLOAT", {"default": -1.0, "min": -60.0, "max": 0.0, "step": 0.1}),
                "mode": (["peak", "rms"],),
            },
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "run"
    CATEGORY = "ComfyUI-Audio/Process"

    def run(self, audio, target_dbfs, mode):
        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        peak = float(waveform.abs().max())
        measured = peak if mode == "peak" else float(waveform.pow(2).mean().sqrt())
        if measured == 0.0:
            return ({"waveform": waveform, "sample_rate": sample_rate},)

        target = 10.0 ** (target_dbfs / 20.0)
        gain = target / measured
        if gain * peak > 1.0:
            gain = 1.0 / peak

        return ({"waveform": waveform * gain, "sample_rate": sample_rate},)


NODE_CLASS_MAPPINGS = {
    "comfyui_audio_normalize": CFXNormalizeAudio,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "comfyui_audio_normalize": "ComfyUI-Audio · Normalize",
}
