import torch

from comfyui_cfx.packages.audio.nodes import normalize as normalize_node

node = normalize_node.CFXNormalizeAudio()


def make_audio(waveform, sample_rate=16000):
    return {"waveform": waveform, "sample_rate": sample_rate}


def test_peak_mode_hits_target_dbfs():
    waveform = torch.zeros(1, 1, 1600)
    waveform[..., 100:900] = 0.25
    out = node.run(make_audio(waveform), -1.0, "peak")[0]
    assert abs(float(out["waveform"].abs().max()) - 10 ** (-1.0 / 20)) < 1e-6


def test_loud_input_not_amplified_past_full_scale():
    waveform = torch.zeros(1, 1, 1600)
    waveform[..., 100:900] = 0.9
    out = node.run(make_audio(waveform), 0.0, "rms")[0]
    assert float(out["waveform"].abs().max()) <= 1.0


def test_silent_input_unchanged():
    waveform = torch.zeros(1, 1, 1600)
    out = node.run(make_audio(waveform), -1.0, "peak")[0]
    assert out["waveform"].shape[-1] == 1600
    assert torch.equal(out["waveform"], waveform)


def test_sample_rate_preserved():
    out = node.run(make_audio(torch.zeros(1, 1, 1600), 22050), -1.0, "peak")[0]
    assert out["sample_rate"] == 22050


def test_input_not_mutated():
    waveform = torch.zeros(1, 1, 1600)
    waveform[..., 100:900] = 0.25
    audio = make_audio(waveform)
    before = waveform.clone()
    node.run(audio, 0.0, "peak")
    assert audio["waveform"].shape == (1, 1, 1600)
    assert audio["sample_rate"] == 16000
    assert torch.equal(audio["waveform"], before)


def test_rms_mode_finite_and_bounded():
    waveform = torch.zeros(1, 2, 1600)
    waveform[..., 100:900] = 0.25
    out = node.run(make_audio(waveform), -3.0, "rms")[0]
    assert out["waveform"].shape == (1, 2, 1600)
    assert torch.isfinite(out["waveform"]).all()
    assert float(out["waveform"].abs().max()) <= 1.0
