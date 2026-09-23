"""Synthetic tensors in the cfx type lattice (ADR-0001)."""

import torch


def make_image(batch: int = 1, height: int = 64, width: int = 64, channels: int = 3) -> torch.Tensor:
    return torch.rand(batch, height, width, channels, dtype=torch.float32)


def make_mask(batch: int = 1, height: int = 64, width: int = 64) -> torch.Tensor:
    return torch.rand(batch, height, width, dtype=torch.float32)


def make_latent(batch: int = 1, channels: int = 4, height: int = 8, width: int = 8) -> dict:
    return {"samples": torch.randn(batch, channels, height, width, dtype=torch.float32)}
