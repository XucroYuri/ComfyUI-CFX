"""cfx type lattice (ADR-0001).

- IMAGE  : torch.Tensor [B, H, W, C], float32, values in [0, 1]
- MASK   : torch.Tensor [B, H, W],    float32, values in [0, 1]
- LATENT : dict containing at least ``{"samples": [B, C, h, w]}``

No implicit conversion between types happens here; nodes opt in explicitly.
"""

import torch

IMAGE = "IMAGE"
MASK = "MASK"
LATENT = "LATENT"


def is_image(value) -> bool:
    return isinstance(value, torch.Tensor) and value.dim() == 4 and value.shape[-1] in (1, 3, 4)


def is_mask(value) -> bool:
    return isinstance(value, torch.Tensor) and value.dim() == 3


def ensure_image(value) -> torch.Tensor:
    """Return ``value`` normalized to [B, H, W, C] float32.

    Accepts 3D HWC, 4D BHWC and 4D BCHW. Raises on anything else instead of guessing.
    """
    if not isinstance(value, torch.Tensor):
        raise TypeError(f"IMAGE must be a torch.Tensor, got {type(value).__name__}")

    x = value
    if x.dim() == 3:
        x = x.unsqueeze(0)
    if x.dim() != 4:
        raise ValueError(f"IMAGE must be 3D or 4D, got shape {tuple(value.shape)}")

    if x.shape[-1] not in (1, 3, 4):
        if x.shape[1] not in (1, 3, 4):
            raise ValueError(f"IMAGE needs a channel dim of 1/3/4, got shape {tuple(value.shape)}")
        x = x.permute(0, 2, 3, 1)

    if x.dtype != torch.float32:
        x = x.float()
    return x.contiguous()


def make_latent(samples: torch.Tensor) -> dict:
    if not isinstance(samples, torch.Tensor) or samples.dim() != 4:
        raise ValueError("LATENT samples must be a 4D tensor")
    return {"samples": samples}


def latent_samples(latent: dict) -> torch.Tensor:
    if not isinstance(latent, dict) or "samples" not in latent:
        raise ValueError("LATENT must be a dict containing 'samples'")
    return latent["samples"]
