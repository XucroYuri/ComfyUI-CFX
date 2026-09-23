"""VRAM accounting helpers.

CUDA is not required; on CPU these return 0 so tests stay portable.
"""

import torch


def allocated_bytes() -> int:
    if not torch.cuda.is_available():
        return 0
    return torch.cuda.memory_allocated()


def grew(before: int, after: int, tolerance: int = 0) -> bool:
    return after - before > tolerance
