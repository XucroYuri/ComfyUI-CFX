# Review · comfyui_controlnet_pick_pose

reviewer: Codex
date: 2026-11-27
verdict: PASS

- Offline misses do not access the network. Local PNG overrides win over downloaded files. Tests cover both cases, cached re-use, redirect refusal and symlink containment.
- The Ubuntu ComfyUI Python runtime loaded all 67 CFX node mappings. The offline diagram and live P001 diagonal download produced RGB BHWC tensors. The cached P001 tensor matched the online tensor exactly.
- The repository includes catalog metadata with attribution and two original skeletons. PoseWear artwork remains on the source host.
- Qwen and DWPose examples depend on the respective local nodes and models. This review verified node execution and cache behavior independently of model quality.
