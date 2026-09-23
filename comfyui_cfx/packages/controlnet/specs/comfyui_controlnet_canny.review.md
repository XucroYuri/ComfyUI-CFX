# Adversarial Review: comfyui_controlnet_canny

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §2 形状：`image` 恒为 `[1,H,W,3]`、`mask` 恒为 `[1,H,W]`，有单测。
- §2 值域：边缘 `/255` 后复制，输出严格落在 `[0,1]`。
- §2 亮度：`0.299/0.587/0.114` 加权；单通道复制，1/3/4 通道均可处理。
- §7.1 `high < low`：抛 `ValueError`，不静默交换，有单测。
- §7 非法输入：交给 `ensure_image` 统一抛错。
- §8.3 合成黑底白方块：产生非零边缘，有单测。
- §8.4 阈值单调性：`count(high) <= count(low)`，有单测。
- §6 无副作用：无文件/网络/全局状态；`cv2` 惰性导入。
- 许可：实现为本仓原创（行为参考 controlnet_aux，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. 抗锯齿图与真实照片的抗噪表现未做基准；当前无高斯预模糊，保留上游最直接语义。
2. 仅处理 batch 第一项系有意设计，多 batch 语义待产品确认。
3. GPU 张量输入依赖一次 `.cpu()` 拷贝，未做大图性能测量（CPU 节点，优先级低）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| high < low | 报错 | PASS（ValueError） |
| 全黑图 | 边缘为 0 | PASS |
| 黑底白方块 | 非零边缘 | PASS |
| 高阈值 | 边缘不增 | PASS |
| batch>1 | 输出 batch=1 | PASS |
