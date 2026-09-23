"""Logging helper with one-time warnings."""

import logging

LOGGER = logging.getLogger("ComfyUI-CFX")
_seen = set()


def warn_once(key: str, message: str) -> None:
    if key in _seen:
        return
    _seen.add(key)
    LOGGER.warning(message)
