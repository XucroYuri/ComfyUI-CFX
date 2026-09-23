"""Pytest bootstrap: put the repo root on ``sys.path`` so ``comfyui_cfx`` imports."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
