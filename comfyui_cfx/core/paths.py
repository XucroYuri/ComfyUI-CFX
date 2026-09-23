"""Path containment helpers.

Every filesystem path that originates from a widget or a combo value must go through
one of these helpers before use (see AGENTS.md).
"""

import os
import folder_paths


def output_dir() -> str:
    return folder_paths.get_output_directory()


def temp_dir() -> str:
    return folder_paths.get_temp_directory()


def safe_join(root: str, name: str) -> str:
    """Join ``name`` under ``root``, rejecting absolute paths and traversal."""
    if not name or os.path.isabs(name):
        raise ValueError(f"path must be a relative name, got {name!r}")
    root_abs = os.path.abspath(root)
    candidate = os.path.abspath(os.path.join(root_abs, name))
    if os.path.commonpath([root_abs, candidate]) != root_abs:
        raise ValueError(f"path escapes {root_abs!r}: {name!r}")
    return candidate


def safe_filename(name: str) -> str:
    """Validate a bare file name (no separators, no traversal)."""
    base = os.path.basename(name)
    if base != name or base in ("", ".", ".."):
        raise ValueError(f"invalid file name {name!r}")
    return base
