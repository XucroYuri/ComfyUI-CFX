# ComfyUI-Flow · SPEC

## 使命
连线/广播/上下文/控制流/UI 辅助的规范化与统一契约。

## 不负责
图像/模型推理原语。

## 来源（可 wrap）
rgthree（MIT）、cg-use-everywhere（Apache-2.0）、custom-scripts/pysssss（MIT）。

## 许可
MIT；包装宽松上游时保留署名/NOTICE。

## 边界规则
- 虚拟连线模块（cg-use-everywhere）必须**隔离**，其状态不得泄漏到其他模块。
- wrap 的节点保留原 `class_type` 以兼容旧工作流。

## 节点 ID 前缀
`comfyui_flow_<verb>_<noun>` · 分类 `ComfyUI-Flow/<Sub>`
