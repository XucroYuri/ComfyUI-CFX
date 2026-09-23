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
| `comfyui_primitives_image_crop` | | | | | TODO |
| `comfyui_primitives_image_transform` | | | | | TODO |
| `comfyui_primitives_image_stitch` | | | | | TODO |
| `comfyui_primitives_mask_ops` | | | | | TODO |
| `comfyui_primitives_batch_list` | | | | | TODO |
| `comfyui_primitives_resolution` | | | | | TODO |
| `comfyui_primitives_save_image_metadata` | | | | | TODO |
| `comfyui_primitives_seed` | | | | | TODO |

## 3. 里程碑
- M1 — `image_resize` 全链路（SPEC→IMPL→REVIEW→VERIFY）跑通 | 状态：DONE
- M2 — Switch/Boolean/Math/Text 完成 | 状态：VERIFY

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

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| 许可污染（GPL/无证） | 法务/发布受阻 | 只重写行为 + CI license-gate | WATCH |

## 6. 下一步
1. 写 `image_resize` SPEC + 对抗性反例；
2. 实现并跑通模板链路。
