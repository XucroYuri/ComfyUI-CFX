"""Fail if any package under packages/ is not MIT or contains copied GPL markers."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "comfyui_cfx" / "packages"
FORBIDDEN = ("GNU General Public License", "GPL-3.0", "GPLv3", "GPL-2.0")


def main() -> int:
    problems = []
    for package in sorted(p for p in PACKAGES.iterdir() if p.is_dir() and not p.name.startswith("_")):
        spec = package / "SPEC.md"
        if not spec.exists():
            problems.append(f"{package.name}: missing SPEC.md")
            continue
        if "MIT" not in spec.read_text(encoding="utf-8"):
            problems.append(f"{package.name}: SPEC.md does not declare MIT")

        for py in package.rglob("*.py"):
            source = py.read_text(encoding="utf-8", errors="replace")
            for marker in FORBIDDEN:
                if marker in source:
                    problems.append(f"{py.relative_to(ROOT)}: contains {marker!r}")

    if problems:
        print("\n".join(problems))
        return 1
    print("license_gate: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
