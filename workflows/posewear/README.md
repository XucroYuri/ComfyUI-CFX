# PoseWear references

Add **ComfyUI-ControlNet · Pose Reference Picker (PoseWear)** to a graph. Choose a pose and a view. `offline` reads bundled diagrams or local files under `ComfyUI/input/posewear`. `on demand` downloads one missing selection from PoseWear and caches it there. Put `<pose_id>_<view>.png`, `.jpg`, or `.webp` in that folder to use a local reference.

- `pose_preview.json` opens in the ComfyUI workflow editor. The bundled skeleton or cached poses can be previewed offline.
- `pose_preview_api.json` shows node inputs and the image connection in API format.
- `qwen21_pose_api.json` connects the output to the third image slot of Qwen-Image 2.1. Supply two identity images under `input/character` and select the matching model weights for the local installation.
- `pose_to_skeleton_api.json` uses optional DWPose and saves a keypoint JSON and a skeleton image. Start with the selected pose cached. The line-drawing example skips bounding-box detection. Check the generated joints before reuse.

Existing standalone workflows can switch the node class from `PoseWearReference` to `comfyui_controlnet_pick_pose`. Inputs and outputs keep their order. The node exports an image, Chinese and English prompts, and the source page. See [asset attribution](../../comfyui_cfx/packages/controlnet/pose_assets/NOTICE.md).

The CLI lists, inspects and exports pose entries. Run these from the repository root. Export requires Pillow.

```sh
python comfyui_cfx/packages/controlnet/posewear.py list --search 站姿
python comfyui_cfx/packages/controlnet/posewear.py show full_single_P001 --view diag
python comfyui_cfx/packages/controlnet/posewear.py export pose_step --offline --out step.png
```
