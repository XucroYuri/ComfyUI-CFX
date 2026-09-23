# ComfyUI-Vision · 开发记录（DEVLOG）

> 建仓日期：2026-09-23 ｜ 维护：只追加 ｜ 伞仓记录：`../../DEVLOG.md`

## 1. 使命与边界
- 使命：打标/描述/VLM 的统一节点面、模型复用与单一缓存。
- 不负责：控制流、分割、文本提示生成。
- 来源插件：florence2(**MIT**)、WD14(**MIT**)、Miaoshouai(**MIT**)、QwenVL(**GPL-3.0**)、was(BLIP, MIT)、mixlab(MIT)、AcademiaSD(MIT)。
- 许可：本包 **MIT**；QwenVL 的 GPL 代码须隔离。

## 2. 状态看板
| 模块 | 策略 | 状态 |
|---|---|---|
| `CFX Vision Model Loader` | REWRITE（统一注册表 + 有界 LRU） | TODO |
| `CFX Florence-2 Tasks`（15 任务） | 采用 kijai 自带后端 | TODO |
| `CFX WD14 Tagger` | KEEP-DESIGN + session 缓存 | TODO |
| `CFX VLM Caption`（Qwen2.5/3-VL） | 主路径保留；GPL 隔离 | TODO |
| `CFX BLIP Caption/Interrogate` | REWRITE（原生 BLIP） | TODO |
| `CFX CLIP Interrogator` | WRAP（可选 extra） | TODO |
| `compat.py` | NEW | TODO |
| 删除 rmbg `AILab_Florence2*` / `qwen3vl_caption_bridge.py` | DELETE | TODO |

## 3. 里程碑
- M1 — Loader + Florence-2 Tasks 可用且无 remote code | 状态：TODO
- M2 — Qwen-VL 在 transformers 5.14.1 主路径 + FP8 修复 | 状态：TODO

## 4. 变更日志（追加）
- 2026-09-23 | Architect | 建立 Vision 包与开发记录 | SPEC.md | DONE

## 5. 风险 / 阻塞
| 项 | 影响 | 缓解 | 状态 |
|---|---|---|---|
| QwenVL GPL-3.0 | 许可污染 | 隔离为 Community 包 | WATCH |
| rmbg Florence2 / mixlab MiniCPM remote code | 5.14.1 下崩 | 删除/迁移原生实现 | WATCH |

## 6. 下一步
1. 定稿 Loader 描述符与缓存键；
2. 迁移 Miaoshouai 直连 kijai 后端。
