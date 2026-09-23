"""Fail if a registered node is missing its contract or adversarial review.

For every node id found in ``packages/*/nodes/*.py`` the matching
``packages/<domain>/specs/<id>.md`` and ``<id>.review.md`` (with ``verdict: PASS``)
must exist. Also requires each package to ship a ``DEVLOG.md`` and ``SPEC.md``.
"""

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "comfyui_cfx" / "packages"


def node_ids():
    for path in sorted(PACKAGES.glob("*/nodes/*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "NODE_CLASS_MAPPINGS" and isinstance(node.value, ast.Dict):
                    for key in node.value.keys:
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            yield key.value, path


def main() -> int:
    problems = []
    for package in sorted(p for p in PACKAGES.iterdir() if p.is_dir() and not p.name.startswith("_")):
        for required in ("SPEC.md", "DEVLOG.md"):
            if not (package / required).exists():
                problems.append(f"{package.name}: missing {required}")

    for node_id, path in node_ids():
        domain = path.parents[1]
        spec = domain / "specs" / f"{node_id}.md"
        review = domain / "specs" / f"{node_id}.review.md"
        if not spec.exists():
            problems.append(f"missing spec: {spec.relative_to(ROOT)}")
        if not review.exists():
            problems.append(f"missing review: {review.relative_to(ROOT)}")
        elif "verdict: PASS" not in review.read_text(encoding="utf-8"):
            problems.append(f"review not PASS: {review.relative_to(ROOT)}")

    if problems:
        print("\n".join(problems))
        return 1
    print("spec_lint: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
