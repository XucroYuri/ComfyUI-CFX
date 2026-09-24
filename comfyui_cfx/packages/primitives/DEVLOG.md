# ComfyUI-Primitives · 开发记录（DEVLOG）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 伞仓记录：`../../DEVLOG.md`

## 1. 使命与边界
- 使命：唯一一套文本/数值/逻辑/图像/掩码/分辨率原语。
- 不负责：模型推理、连图与 UI。
- 来源插件：WAS、Comfyroll(**无证**)、easy-use/tinyterra/wlsh(**GPL**)、mtb、various(**无证**)、essentials、AGSoft、YCNodes(**无证**)、Jjk、controlaltai、image-saver、custom-scripts。
- 许可：**MIT**；禁止复制 GPL/无证代码。

## 2. 状态看板
| 节点 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_primitives_image_resize` | specs/image_resize.md | nodes/image.py | specs/image_resize.review.md | tests/test_primitives_image_resize.py | VERIFY |
| `comfyui_primitives_switch` | specs/….md | nodes/switch.py | ….review.md | tests/test_primitives_switch.py | VERIFY |
| `comfyui_primitives_boolean` | specs/….md | nodes/boolean.py | ….review.md | tests/test_primitives_boolean.py | VERIFY |
| `comfyui_primitives_math` | specs/….md | nodes/math.py | ….review.md | tests/test_primitives_math.py | VERIFY |
| `comfyui_primitives_text` | specs/….md | nodes/text.py | ….review.md | tests/test_primitives_text.py | VERIFY |
| `comfyui_primitives_image_crop` | specs/….md | nodes/crop.py | ….review.md | tests/test_primitives_image_crop.py | VERIFY |
| `comfyui_primitives_image_transform` | specs/….md | nodes/transform.py | ….review.md | tests/test_primitives_image_transform.py | VERIFY |
| `comfyui_primitives_image_stitch` | specs/….md | nodes/stitch.py | ….review.md | tests/test_primitives_image_stitch.py | VERIFY |
| `comfyui_primitives_mask_ops` | specs/….md | nodes/mask.py | ….review.md | tests/test_primitives_mask_ops.py | VERIFY |
| `comfyui_primitives_image_batch` | specs/….md | nodes/batch.py | ….review.md | tests/test_primitives_batch.py | VERIFY |
| `comfyui_primitives_image_split` | specs/….md | nodes/batch.py | ….review.md | tests/test_primitives_batch.py | VERIFY |
| `comfyui_primitives_resolution` | specs/….md | nodes/resolution.py | ….review.md | tests/test_primitives_resolution.py | VERIFY |
| `comfyui_primitives_save_image_metadata` | specs/….md | nodes/save.py | ….review.md | tests/test_primitives_save.py | VERIFY |
| `comfyui_primitives_seed` | specs/….md | nodes/seed.py | ….review.md | tests/test_primitives_seed.py | VERIFY |
| `comfyui_primitives_json_bbox` | specs/comfyui_primitives_json_bbox.md | nodes/json_access.py | specs/comfyui_primitives_json_bbox.review.md | tests/test_primitives_json_bbox.py | VERIFY |

## 3. 里程碑
- M1 — `image_resize` 全链路（SPEC→IMPL→REVIEW→VERIFY）跑通 | 状态：DONE
- M2 — Switch/Boolean/Math/Text 完成 | 状态：DONE
- M3 — Crop/Transform/Stitch/MaskOps 完成 | 状态：DONE
- M4 — Batch/Split/Seed/Resolution/Save 完成 | 状态：VERIFY

## 4. 变更日志（追加）
- 2026-09-23 | Architect | 建立 Primitives 包与开发记录 | SPEC.md | DONE
- 2026-09-23 | Spec-Writer | 写 image_resize 契约与对抗性反例 | specs/comfyui_primitives_image_resize.md | DONE
- 2026-09-23 | Implementer | 实现 CFXImageResize（stretch/crop/pad） | nodes/image.py | IMPL
- 2026-09-23 | Adversary | 审查并给出 verdict PASS | specs/comfyui_primitives_image_resize.review.md | DONE
- 2026-09-23 | Verifier | 10 项单测通过 | tests/test_primitives_image_resize.py | VERIFY
- 2026-09-23 | Spec-Writer | 写 switch/boolean/math/text 四份契约与审查 | specs/*.md | DONE
- 2026-09-23 | Implementer | 实现 switch/boolean/math/text（含 AST 白名单数学） | nodes/{switch,boolean,math,text}.py | IMPL
- 2026-09-23 | Adversary | 四节点 verdict PASS；修正 replace 空 search 缺陷 | specs/*.review.md | DONE
- 2026-09-23 | Verifier | 四节点单测通过 | tests/test_primitives_{switch,boolean,math,text}.py | VERIFY
- 2026-09-23 | Spec-Writer | 写 crop/transform/stitch/mask_ops 契约与审查 | specs/*.md | DONE
- 2026-09-23 | Implementer | 实现 crop/transform/stitch/mask_ops（fill_holes 用 scipy.ndimage） | nodes/{crop,transform,stitch,mask}.py | IMPL
- 2026-09-23 | Adversary | 四节点 verdict PASS | specs/*.review.md | DONE
- 2026-09-23 | Verifier | M3 单测通过 | tests/test_primitives_{image_crop,image_transform,image_stitch,mask_ops}.py | VERIFY
- 2026-09-23 | Architect | 将 `batch_list` 拆为 image_batch / image_split（ComfyUI 的 OUTPUT_IS_LIST 需在类定义期确定） | 本记录 | DONE
- 2026-09-23 | Spec-Writer/Implementer/Adversary | M4：batch/split/seed/resolution/save 契约、实现、审查全部 PASS | nodes/*.py, specs/*.md | DONE
- 2026-09-23 | Verifier | M4 单测通过 | tests/test_primitives_{batch,seed,resolution,save}.py | VERIFY
- 2026-09-25 | Spec-Writer/Implementer/Adversary | JSON BBox：契约、实现、审查全部 PASS，检测字典 → 4×INT 桥接 | nodes/json_access.py, specs/comfyui_primitives_json_bbox*.md | DONE
- 2026-09-25 | Verifier | JSON BBox 单测通过 | tests/test_primitives_json_bbox.py | VERIFY

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| 许可污染（GPL/无证） | 法务/发布受阻 | 只重写行为 + CI license-gate | WATCH |

## 6. 下一步
1. 写 `image_resize` SPEC + 对抗性反例；
2. 实现并跑通模板链路。
