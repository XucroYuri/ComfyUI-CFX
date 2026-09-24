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
| `comfyui_segment_grounding_dino` | specs/….md | nodes/detect.py | ….review.md | tests/test_segment_detect.py | DONE（真实推理通过，修复 2 处 bug） |
| `registry.py`（家族/布局/缓存键） | — | registry.py | — | tests/test_segment_geometry.py | VERIFY |
| `comfyui_segment_sam2_loader` | specs/….md | nodes/sam2.py（+ backend.py） | ….review.md | tests/test_segment_sam2.py | DONE（真实推理通过） |
| `comfyui_segment_sam2_mask` | specs/….md | nodes/sam2.py | ….review.md | tests/test_segment_sam2.py | DONE（真实推理通过：覆盖 6.3%） |
| `comfyui_segment_sam2_points` | specs/….md | nodes/sam2_points.py | ….review.md | tests/test_segment_sam2_points.py | DONE（真实推理通过：覆盖 9.4%） |
| `comfyui_segment_matting` | specs/….md | nodes/matting.py | ….review.md | tests/test_segment_matting.py | DONE（真实推理通过，修复 1 处 bug） |
| `comfyui_segment_face_crop` | specs/….md | nodes/face.py（+ face_backend.py） | ….review.md | tests/test_segment_face.py | DONE（真实推理通过） |
| `comfyui_segment_text_to_mask` | specs/….md | nodes/text_to_mask.py | ….review.md | tests/test_segment_text_to_mask.py | DONE（真实推理通过：3 框 + MASK 覆盖 0.299） |
| `comfyui_segment_mask_to_bbox` | specs/….md | nodes/mask_to_bbox.py（+ geometry.py） | ….review.md | tests/test_segment_mask_to_bbox.py | DONE（纯几何） |

## 3. 里程碑
- M1 — 标注→掩码几何层 + GroundingDINO 文本检测 | 状态：DONE
- M2 — SAM2（单份 Apache 实现，经后端复用）| 状态：DONE
- M3 — 抠图（rembg MIT）/ FaceCrop（AutoCropFaces MIT 复用）| 状态：DONE

## 4. 变更日志（追加）
- 2026-09-23 | Architect | 建立 Segment 包与开发记录 | SPEC.md | DONE
- 2026-09-23 | Architect | 决策：文本检测统一 transformers；GPL 只重写；SAM2 只留一份 | SPEC.md | DONE
- 2026-09-24 | Spec-Writer/Implementer/Adversary | M1：annotations_to_mask + grounding_dino 全链路 PASS | nodes/*.py, specs/*.md | DONE
- 2026-09-24 | Verifier | 几何/分析/检测接口单测通过 | tests/test_segment_*.py | VERIFY
- 2026-09-24 | Architect | 决策：SAM2 复用 Apache 后端（不 vendor 第三份），CPU 强制 fp32 | backend.py | DONE
- 2026-09-24 | Spec-Writer/Implementer/Adversary | M2：sam2_loader/sam2_mask 全链路 PASS | nodes/sam2.py, specs/*.md | DONE
- 2026-09-24 | Verifier | 后端定位/批次转换/接口单测通过；SAM2 真实推理待人工验证 | tests/test_segment_sam2.py | VERIFY
- 2026-09-24 | Verifier | SAM2 真实推理端到端通过：加载 sam2.1_hiera_tiny(fp16) → 框提示 → MASK (1,768,768)、二值、覆盖 6.3% | verify_segment_sam2 | DONE
- 2026-09-24 | Spec-Writer/Implementer/Adversary | M3：matting（rembg MIT）+ face_crop（AutoCropFaces MIT 复用）全链路 PASS | nodes/*.py, specs/*.md | DONE
- 2026-09-24 | Verifier | 抠图 alpha 纯函数与 FaceCrop 后端/接口单测通过 | tests/test_segment_{matting,face}.py | VERIFY
- 2026-09-24 | Implementer | GDINO/Matting 改用 `core.images.first_image_to_pil` 修复 clamp-on-ndarray | nodes/*.py | FIXED
- 2026-09-24 | Verifier | FaceCrop 真实推理通过（example/kaffi/bridge 均无异常）；实测澄清「无人脸返回原图」并修正 SPEC | verify_segment_face | DONE
- 2026-09-24 | Verifier | GDINO 真实推理**失败**：ndarray 上调 `.clamp`；transformers 5 将 `box_threshold` 改名为 `threshold` | tools/verify/grounding_dino.py | REJECTED
- 2026-09-24 | Implementer | 修复 GDINO：tensor 上 clamp；`threshold=box_threshold`；标签优先读 `text_labels` | nodes/detect.py | FIXED
- 2026-09-24 | Verifier | GDINO 真实推理通过：4 框（dress/face/girl/girl）+ MASK | tools/verify/grounding_dino.py | DONE
- 2026-09-24 | Verifier | Matting 真实推理**失败**：ndarray 上调 `.clamp` | tools/verify/matting.py | REJECTED
- 2026-09-24 | Implementer | 修复 Matting：tensor 上 clamp 再转 numpy | nodes/matting.py | FIXED
- 2026-09-24 | Verifier | Matting 真实推理通过：MASK (1,768,768) 覆盖 0.289 + RGBA (1,768,768,4) | tools/verify/matting.py | DONE
- 2026-09-24 | Implementer | 新增 sam2_points / text_to_mask / mask_to_bbox；后端增 `segment_points` | nodes/*.py, backend.py | IMPL
- 2026-09-24 | Verifier | sam2_points 真实推理通过（覆盖 0.094）；text_to_mask 真实推理通过（3 框，覆盖 0.299） | tools/verify/{sam2_points,text_to_mask}.py | DONE
- 2026-09-24 | Spec-Writer/Implementer/Adversary | 新增 SAM2 点提示分割：`parse_points` 归一两种形状，正/负点 JSON 透传后端 | nodes/sam2_points.py, specs/comfyui_segment_sam2_points*.md | VERIFY
- 2026-09-24 | Spec-Writer/Implementer/Adversary | 新增 text_to_mask：GroundingDINO→SAM2 组合链（无框/无 sam2 走几何回退）并通过审查 | nodes/text_to_mask.py, specs/*.md | VERIFY
- 2026-09-24 | Verifier | text_to_mask 离线单测通过（SAM2 路径/几何回退/空框全 0/detections 透传） | tests/test_segment_text_to_mask.py | VERIFY
- 2026-09-24 | Spec-Writer/Implementer/Adversary | 新增 `mask_to_bbox`（`annotations_to_mask` 逆）：纯几何 `mask_to_bboxes` + 节点 + spec/review PASS | geometry.py, nodes/mask_to_bbox.py, specs/*.md | REVIEW
- 2026-09-24 | Verifier | mask→bbox 单测通过（矩形/向外对齐/夹取/空项/2D/阈值/多批） | tests/test_segment_mask_to_bbox.py | VERIFY

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| rmbg / impact-pack GPL-3.0 | 许可污染 | 只重写行为 + CI license-gate | WATCH |
| SAM3 仅存在于 GPL 插件 | 无法直接复制 | 重写或独立隔离包 | WATCH |

## 6. 下一步
1. `cfx-segment` M1–M3 已全部通过 L3 真实推理；剩余可选：SAM3 / 更多抠图模型。
2. 未验证节点见 `docs/verification-matrix.md`（当前仅 BLIP / VLM / Resolve 模型放大）。
