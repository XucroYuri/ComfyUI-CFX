import math

import pytest

pytest.importorskip("torch")
pytest.importorskip("comfy.utils")

from comfyui_cfx.packages.primitives.nodes import seed as seed_node

node = seed_node.CFXSeed()


def test_fixed_returns_seed():
    assert node.run(5, "fixed") == (5,)


def test_increment_wraps_at_max():
    assert node.run(seed_node.MAX_SEED, "increment") == (0,)


def test_decrement_wraps_at_zero():
    assert node.run(0, "decrement") == (seed_node.MAX_SEED,)


def test_randomize_stays_in_range():
    value = node.run(0, "randomize")[0]
    assert 0 <= value <= seed_node.MAX_SEED


def test_is_changed_nan_when_not_fixed():
    assert math.isnan(node.IS_CHANGED(1, "randomize"))
    assert math.isnan(node.IS_CHANGED(1, "increment"))


def test_is_changed_seed_when_fixed():
    assert node.IS_CHANGED(7, "fixed") == 7
