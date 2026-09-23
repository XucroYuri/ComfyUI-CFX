"""dtype / device parametrization for node tests."""

import pytest
import torch

DTYPES = [torch.float32, torch.float16, torch.bfloat16]


@pytest.fixture(params=DTYPES, ids=lambda d: str(d).split(".")[-1])
def dtype(request):
    return request.param
