import torch

from comfyui_cfx.packages.audio.nodes import trim as trim_node

node = trim_node.CFXTrimSilence()


def make_audio(waveform, sample_rate=16000):
    return {"waveform": waveform, "sample_rate": sample_rate}


def test_trims_lead_and_tail():
    waveform = torch.zeros(1, 1, 16000)
    waveform[..., 3200:9600] = 0.5
    out = node.run(make_audio(waveform), 0.01, 100, 50)[0]
    assert out["waveform"].shape[-1] < 16000
    assert torch.equal(out["waveform"], waveform[..., 2400:10400])


def test_all_silent_unchanged():
    waveform = torch.zeros(1, 1, 16000)
    out = node.run(make_audio(waveform), 0.01, 100, 50)[0]
    assert out["waveform"].shape[-1] == 16000


def test_all_loud_unchanged():
    waveform = torch.full((1, 1, 16000), 0.5)
    out = node.run(make_audio(waveform), 0.01, 100, 50)[0]
    assert out["waveform"].shape[-1] == 16000


def test_sample_rate_preserved():
    out = node.run(make_audio(torch.zeros(1, 1, 16000), 22050), 0.01, 100, 50)[0]
    assert out["sample_rate"] == 22050


def test_input_not_mutated():
    waveform = torch.zeros(1, 1, 16000)
    waveform[..., 3200:9600] = 0.5
    audio = make_audio(waveform)
    node.run(audio, 0.01, 100, 50)
    assert audio["waveform"].shape[-1] == 16000
    assert audio["sample_rate"] == 16000
    assert float(audio["waveform"][..., 0].abs().sum()) == 0.0


def test_stereo_handled():
    waveform = torch.zeros(1, 2, 16000)
    waveform[..., 3200:9600] = 0.5
    out = node.run(make_audio(waveform), 0.01, 100, 50)[0]
    assert out["waveform"].shape == (1, 2, 8000)
    assert torch.equal(out["waveform"], waveform[..., 2400:10400])
