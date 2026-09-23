# ComfyUI-CFX — engineering rules

These rules are enforced in review and by CI. They extend the ComfyUI root `AGENTS.md`.

## License gate (hard)

- `packages/**` is MIT only. **Never copy** code from GPL-3.0 plugins
  (`easy-use`, `tinyterra`, `wlsh`, `QwenVL`, `rmbg`, `impact-pack`) or from plugins
  without a license (`ComfyRoll`, `comfyui-various`, `YCNodes`).
- Those plugins may be used as **behaviour references** only. GPL-derived work goes into a
  separate, disabled `ComfyUI-<Domain>-Community` package.
- `tools/license_gate.py` must pass.

## Spec first

- No node implementation without a matching `specs/<node_id>.md`.
- Every merged node needs `specs/<node_id>.review.md` with `verdict: PASS`.
- `tools/spec_lint.py` must pass.

## Development record

- Each package keeps an append-only `DEVLOG.md`; entries are
  `- YYYY-MM-DD | <role> | <action> | <artifact> | <status>`.
- Node status moves `TODO → SPEC → IMPL → REVIEW → VERIFY → DONE`. History is never rewritten.

## Contracts

- Node ids: `comfyui_<domain>_<verb>_<noun>`. Display names: `ComfyUI-<Domain> · <Name>`.
  Categories: `ComfyUI-<Domain>/<Sub>`. Published ids never break.
- Use the `core.types` lattice (`IMAGE` BHWC float32, `MASK` BHW, `LATENT` dict, real
  `BOOLEAN`). No implicit cross-type conversion.
- No `transformers` remote code. Keep `core` free of `transformers`.
- Any filesystem path coming from a widget is validated with `core.paths` containment
  helpers before use.

## Style

- Small, direct changes. No speculative helpers, no dead branches, sparse comments.
- Keep imports at module scope. No `torch.no_grad`/`inference_mode` wrappers.
- Fail loudly; never silently degrade.
