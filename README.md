# ComfyUI-CFX

Consolidated ComfyUI custom-node suite. One monorepo, multiple domain packages, unified
type lattice, SPEC-driven development, MIT.

## Packages

| Package | Mission | Priority |
|---|---|---|
| `packages/core` | Type lattice, device/dtype, memory, path safety, logging | P0 |
| `packages/testkit` | fixtures, dtype/device matrix, memory regression, golden workflows | P0 |
| `packages/primitives` | text / number / logic / image / mask primitives | P0 |
| `packages/flow` | wiring / broadcast / context / control flow / UI | P0 |
| `packages/vision` | tagging / captioning / VLM | P0 |
| `packages/segment` | segmentation / matting / detection / face | P0 |

## Install

```bat
git clone <repo> ComfyUI\custom_nodes\ComfyUI-CFX
pip install -r requirements.txt
```

## Develop

```bat
pytest
python tools\spec_lint.py
python tools\license_gate.py
```

Every package has a `DEVLOG.md` (append-only development record) and every node has a
contract under `specs/<node_id>.md` plus an adversarial review `specs/<node_id>.review.md`.

## License

MIT. Code is never copied from GPL-3.0 or unlicensed plugins; those are used as
behaviour references only. GPL-derived capabilities live in a separate, disabled
`ComfyUI-<Domain>-Community` package.
