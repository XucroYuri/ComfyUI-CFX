---
id: comfyui_controlnet_pick_pose
display_name: "ComfyUI-ControlNet · Pose Reference Picker (PoseWear)"
category: "ComfyUI-ControlNet/References"
version: 1.0.0
license: MIT
since: 2026-11-27
---

## 1. Purpose

Select a pose reference and its view for image conditioning. The catalog includes 98 PoseWear entries with five views each and two original skeleton examples.

## 2. Inputs and outputs

`pose` selects a catalog entry, `view` selects its angle, and `source_mode` defaults to `offline`. `auto` resolves to the front view or the local diagram. Outputs are RGB `IMAGE` `[1,H,W,3]` float32 in `[0,1]`, Chinese and English prompt strings, and attribution/source text.

## 3. Loading and caching

Local overrides and the cache live under `input/posewear` and are keyed by catalog ID and view. Offline mode reads local files. On-demand mode checks local files first and fetches the selected source image on a miss. Fetches use a fixed HTTPS origin, reject redirects, and cap encoded and decoded size. Cache writes are atomic. Bundled diagrams use package assets. Invalid selections or unavailable images raise errors.

## 4. Verification

Check offline loading, local override precedence, explicit download opt-in, prompt outputs, and compatible image shape. Exercise the existing CFX registry and test suite. PoseWear source images are obtained on demand. Credit and usage terms are recorded alongside the catalog.
