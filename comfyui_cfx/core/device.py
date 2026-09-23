"""Device and dtype policy shared by all cfx packages (ADR-0002)."""

import torch
import comfy.model_management as mm

DTYPES = {
    "fp32": torch.float32,
    "fp16": torch.float16,
    "bf16": torch.bfloat16,
}


def compute_device():
    return mm.get_torch_device()


def offload_device():
    return mm.unet_offload_device()


def resolve_dtype(name: str) -> torch.dtype:
    try:
        return DTYPES[name]
    except KeyError:
        raise ValueError(f"unknown precision {name!r}, expected one of {sorted(DTYPES)}") from None
