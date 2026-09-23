# ComfyUI-Flow · SPEC

## 使命
连线/广播/上下文/控制流/UI 辅助的规范化与统一契约。

## 不负责
图像/模型推理原语。

## 依赖策略（已定）
- **不写包装代码**：`rgthree`（MIT）与 `cg-use-everywhere`（Apache-2.0）作为**推荐可选依赖**，
  在文档中声明兼容即可，避免耦合其大量前端 monkey-patch（见对抗性审查结论）。
- 本包只重写 pysssss（MIT）中**小而独立**的节点：String Function、Show Text、
  Constrain Image、Repeater、Load/Save Text。
- **刻意不移植** `PlaySound` / `SystemNotification`：OS 相关副作用、价值低、需额外运行期依赖。

## 边界规则
- 若未来引入虚拟连线能力，必须**隔离**为独立模块，状态不得泄漏到其他模块。

## 节点 ID 前缀
`comfyui_flow_<verb>_<noun>` · 分类 `ComfyUI-Flow/<Sub>`
