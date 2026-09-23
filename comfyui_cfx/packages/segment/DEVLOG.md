# ComfyUI-Segment · 开发记录（DEVLOG）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 伞仓记录：`../../DEVLOG.md`

## 1. 使命与边界
- 使命：分割/抠图/检测/人脸的统一节点面与单一模型来源。
- 不负责：语义分割预处理器（归 ControlNet）、深度（归 Depth3D）。
- 来源插件：rmbg(**GPL-3.0**)、impact-pack(**GPL-3.0**)、segment-anything-2(**Apache-2.0**)、sam2(Apache 声明)、AutoCropFaces(**MIT**)、florence2(**MIT**)、controlnet_aux(**Apache-2.0**)、essentials(**MIT**)。
- 许可：本包 **MIT**；GPL 只重写行为。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_segment_annotations_to_mask` | specs/….md | nodes/annotations.py（+ geometry.py） | ….review.md | tests/test_segment_{geometry,annotations}.py | VERIFY |
| `comfyui_segment_grounding_dino` | specs/….md | nodes/detect.py | ….review.md | tests/test_segment_detect.py | VERIFY（推理人工） |
| `registry.py`（家族/布局/缓存键） | — | registry.py | — | tests/test_segment_geometry.py | VERIFY |
| SAM2 掩码阶段（单份 Apache 实现） | — | — | — | — | TODO（M2） |
| 抠图（BiRefNet/RMBG，重写） | — | — | — | — | TODO（M2） |
| FaceCrop（唯一 RetinaFace） | — | — | — | — | TODO（M2） |

## 3. 里程碑
- M1 — 标注→掩码几何层 + GroundingDINO 文本检测 | 状态：VERIFY
- M2 — SAM2 掩码 / 抠图 / FaceCrop | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-23 | Architect | 建立 Segment 包与开发记录 | SPEC.md | DONE
- 2026-09-23 | Architect | 决策：文本检测统一 transformers；GPL 只重写；SAM2 只留一份 | SPEC.md | DONE
- 2026-09-24 | Spec-Writer/Implementer/Adversary | M1：annotations_to_mask + grounding_dino 全链路 PASS | nodes/*.py, specs/*.md | DONE
- 2026-09-24 | Verifier | 几何/分析/检测接口单测通过 | tests/test_segment_*.py | VERIFY

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| rmbg / impact-pack GPL-3.0 | 许可污染 | 只重写行为 + CI license-gate | WATCH |
| SAM3 仅存在于 GPL 插件 | 无法直接复制 | 重写或独立隔离包 | WATCH |

## 6. 下一步
1. 定义 `SEG_MODEL` 句柄与 manifest；
2. 用 transformers GDINO 打通 `SegmentDetect`。
