---
id: comfyui_vision_vlm_caption
display_name: "ComfyUI-Vision · VLM Caption"
category: "ComfyUI-Vision/VLM"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "AILab_QwenVL / AILab_QwenVL_Advanced (ComfyUI-QwenVL, GPL-3.0 — 隔离，不复制)"
  - "AcademiaSD 自带 VLM 加载器"
  - "MiniCPM_VQA_Simple (mixlab)"
---

## 1. 目的
用原生 transformers 加载 Qwen2.5/3-VL 做描述/问答，**不使用 `trust_remote_code`**，
也**不包含** GPL-3.0 的 `ComfyUI-QwenVL` 代码。

## 2. 语义
- 构造 `[{role:user, content:[image, text]}]`，`apply_chat_template`；
- `AutoProcessor` + `AutoModelForImageTextToText`（transformers 5.x 原生类）；
- 只解码新 token（裁剪输入长度）；`pixel_values` 转为模型 dtype。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | model | COMBO | 是 | Qwen/Qwen2.5-VL-3B-Instruct |
| in | prompt | STRING | 是 | Describe the image in detail. |
| in | precision | COMBO | 是 | bf16 |
| in | max_new_tokens | INT | 是 | 256 |
| in | do_sample | BOOLEAN | 是 | False |
| in | temperature | FLOAT | 是 | 0.7 |
| out | text | STRING | - | - |

## 4. 执行与缓存
`do_sample=False` 时确定性；模型按仓库名缓存于 `vlm._CACHE`。

## 5. 资源
模型经 `compute_device` 放到计算设备；dtype 由 `precision` 决定。

## 6. 副作用与安全
首次使用下载权重（用户触发）。**无 remote code**（`trust_remote_code` 默认关闭）。

## 7. 错误行为
依赖/模型缺失 → transformers 异常透传；未知 precision → `ValueError`（`resolve_dtype`）。

## 8. 对抗性反例
1. `do_sample=False` 且 `temperature` 非默认 → 不报错（忽略温度）；
2. 非 Qwen 的 image-text 模型（若加入列表）→ `AutoModelForImageTextToText` 自动分派；
3. batch 取首张；
4. 输出裁剪正确（不含 prompt 回显）。

## 9. 验收
`tests/test_vision_vlm.py`（消息构造/接口/延迟导入）；真实推理为人工 VERIFY。
