# ComfyUI-Segment · 开发记录（DEVLOG）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 伞仓记录：`../../DEVLOG.md`

## 1. 使命与边界
- 使命：分割/抠图/检测/人脸的统一节点面与单一模型来源。
- 不负责：语义分割预处理器（归 ControlNet）、深度（归 Depth3D）。
- 来源插件：rmbg(**GPL-3.0**)、impact-pack(**GPL-3.0**)、segment-anything-2(**Apache-2.0**)、sam2(Apache 声明)、AutoCropFaces(**MIT**)、florence2(**MIT**)、controlnet_aux(**Apache-2.0**)、essentials(**MIT**)。
- 许可：本包 **MIT**；GPL 只重写行为。

## 2. 状态看板
| 模块 | 策略 | 状态 |
|---|---|---|
| `SegmentModelLoader`（family → SAM/GDINO/BiRefNet/…） | NEW（单 manifest + 单根目录） | TODO |
| `SegmentDetect`（transformers GDINO / Ultralytics） | REWRITE | TODO |
| `SegmentMask`（SAM 族，含视频） | 保留一份 Apache SAM2 | TODO |
| `SegmentRefineMask` | REWRITE | TODO |
| `FaceCrop`（唯一 RetinaFace） | 采用 AutoCropFaces(MIT) | TODO |
| 兼容转换器 `SEGS↔MASK`、`Florence2BoxesToMask` | NEW | TODO |
| 删除：neverbiasu sam2 / AGSoft RetinaFace / rmbg Florence2 与 vendored sam2 | DELETE | TODO |

## 3. 里程碑
- M1 — Loader + Detect(GDINO) + Mask(SAM2) 可用 | 状态：TODO
- M2 — RefineMask 与 FaceCrop 完成 | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-23 | Architect | 建立 Segment 包与开发记录 | SPEC.md | DONE

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| rmbg / impact-pack GPL-3.0 | 许可污染 | 只重写行为 + CI license-gate | WATCH |
| SAM3 仅存在于 GPL 插件 | 无法直接复制 | 重写或独立隔离包 | WATCH |

## 6. 下一步
1. 定义 `SEG_MODEL` 句柄与 manifest；
2. 用 transformers GDINO 打通 `SegmentDetect`。
