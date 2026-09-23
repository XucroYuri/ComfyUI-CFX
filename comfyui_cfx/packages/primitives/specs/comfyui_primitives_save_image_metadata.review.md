# Adversarial Review: comfyui_primitives_save_image_metadata

reviewer: Adversary
date: 2026-09-23
verdict: PASS

## 通过项
- §6 路径安全：`validate_prefix` 拒绝绝对路径与 `..`，有测试。
- §8.3 RGBA→RGB（jpg/webp）处理。
- §8.5 `embed_workflow=False` 时不写工作流文本。
- 目录由 `folder_paths.get_save_image_path` 解析，不自行拼接根。

## 未决疑点
1. JPG/WEBP 的 EXIF UserComment（A1111 式）未实现（需 `piexif` 额外依赖）；当前仅 PNG 内嵌元数据。已在 SPEC 记录。
2. `quality` 对 PNG 无效（PIL 忽略），行为一致、不报错。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| `../evil` | 报错 | PASS |
| 绝对路径 | 报错 | PASS |
| RGBA→jpg | 转 RGB | PASS（实现保证） |
| embed_workflow=False | 不写工作流 | PASS |
