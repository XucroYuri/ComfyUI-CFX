# ComfyUI-Vision · 开发记录（DEVLOG）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 伞仓记录：`../../DEVLOG.md`

## 1. 使命与边界
- 使命：打标/描述/VLM 的统一节点面、模型复用与单一缓存。
- 不负责：控制流、分割、文本提示生成。
- 来源插件：florence2(**MIT**)、WD14(**MIT**)、Miaoshouai(**MIT**)、QwenVL(**GPL-3.0**)、was(BLIP, MIT)、mixlab(MIT)、AcademiaSD(MIT)。
- 许可：本包 **MIT**；QwenVL 的 GPL 代码须隔离。

## 2. 状态看板
| 节点/模块 | SPEC | 实现 | 审查 | 验收 | 状态 |
|---|---|---|---|---|---|
| `comfyui_vision_caption_clean` | specs/….md | nodes/text.py | ….review.md | tests/test_vision_caption_clean.py | VERIFY |
| `comfyui_vision_tags_filter` | specs/….md | nodes/tags.py | ….review.md | tests/test_vision_tags_filter.py | VERIFY |
| `comfyui_vision_florence2_loader` | specs/….md | nodes/florence2.py | ….review.md | tests/test_vision_florence2.py | VERIFY |
| `comfyui_vision_florence2_run` | specs/….md | nodes/florence2.py | ….review.md | tests/test_vision_florence2.py | VERIFY（真实推理人工） |
| `registry.py`（任务/模型/缓存键） | — | registry.py | — | tests/test_vision_registry.py | VERIFY |
| `backend.py`（Florence-2 后端适配） | — | backend.py | — | tests/test_vision_florence2.py | VERIFY |
| `comfyui_vision_wd14_tagger` | specs/….md | nodes/wd14.py（+ wd14.py） | ….review.md | tests/test_vision_wd14.py | VERIFY（ONNX 推理人工） |
| `comfyui_vision_blip_caption` | specs/….md | nodes/blip.py | ….review.md | tests/test_vision_blip.py | VERIFY（推理人工） |
| `comfyui_vision_vlm_caption` | specs/….md | nodes/vlm.py（+ vlm.py） | ….review.md | tests/test_vision_vlm.py | VERIFY（推理人工） |
| 迁移旧节点 | — | tools/migrate.py | — | tests/test_migrate.py | VERIFY |

## 3. 里程碑
- M1 — 文本层 + 注册表 + Florence-2 加载/运行 | 状态：DONE
- M2 — WD14 / BLIP / 迁移工具 | 状态：DONE
- M3 — VLM（Qwen2.5/3-VL，原生 transformers，GPL 隔离） | 状态：VERIFY

## 4. 变更日志（追加）
- 2026-09-23 | Architect | 建立 Vision 包与开发记录 | SPEC.md | DONE
- 2026-09-23 | Architect | 决策：Florence-2 复用 comfyui-florence2 自带后端；QwenVL GPL 隔离 | SPEC.md | DONE
- 2026-09-23 | Spec-Writer/Implementer/Adversary | caption_clean/tags_filter/florence2(loader+run) 全链路 PASS | nodes/*.py, specs/*.md | DONE
- 2026-09-23 | Verifier | 文本层与注册表单测通过；Florence-2 真实推理已人工验证 | tests/test_vision_*.py | VERIFY
- 2026-09-24 | Spec-Writer/Implementer/Adversary | M2：wd14_tagger/blip_caption 全链路 PASS；新增 tools/migrate.py 与测试 | nodes/*.py, specs/*.md, tools/migrate.py | DONE
- 2026-09-24 | Verifier | WD14 纯函数（预处理/阈值/格式化）与迁移工具单测通过 | tests/test_vision_wd14.py, tests/test_migrate.py | VERIFY
- 2026-09-24 | Spec-Writer/Implementer/Adversary | M3：vlm_caption（Qwen2.5/3-VL 原生 transformers，无 remote code，GPL 隔离）全链路 PASS | nodes/vlm.py, specs/*.md | DONE
- 2026-09-24 | Verifier | VLM 接口/消息构造/延迟导入单测通过；真实推理待人工验证 | tests/test_vision_vlm.py | VERIFY

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| QwenVL GPL-3.0 | 许可污染 | 隔离为 Community 包 | WATCH |
| rmbg Florence2 / mixlab MiniCPM remote code | 5.14.1 下崩 | 删除/迁移原生实现 | WATCH |

## 6. 下一步
1. 定稿 Loader 描述符与缓存键；
2. 迁移 Miaoshouai 直连 kijai 后端。
