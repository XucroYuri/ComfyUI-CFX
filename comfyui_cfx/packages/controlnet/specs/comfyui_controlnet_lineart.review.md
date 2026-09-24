# Adversarial Review: comfyui_controlnet_lineart

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- §1 诚实声明：SPEC 明确标注为**确定性非神经近似**，非 AnimeLineArt 神经模型。
- §2 形状：`image` 恒为 `[1,H,W,3]`、`mask` 恒为 `[1,H,W]`，有单测。
- §2 值域：线稿 `/255` 后复制，输出严格落在 `[0,1]`，有单测。
- §2 亮度：`0.299/0.587/0.114` 加权；单通道复制，1/3/4 通道均可处理。
- §2 阈值常数：`C = max(1, round(strength*50))`，`strength` 越大线越多/越敏感。
- §2 `invert`：False 时 `bitwise_not`，与 True 互补，有单测。
- §7 `block_size` 偶数或 <3：抛 `ValueError`，不静默修正，有单测。
- §7 非法输入：交给 `ensure_image` 统一抛错。
- §6 无副作用：无文件/网络/全局状态；`cv2` 惰性导入。
- 许可：实现为本仓原创（行为参考 controlnet_aux，未复制代码）。

## 未决疑点（交 Verifier / 后续）
1. 非神经近似对照片/阴影的鲁棒性弱于神经 AnimeLineArt，属已知折衷。
2. 仅处理 batch 第一项系有意设计，多 batch 语义待产品确认。
3. GPU 张量输入依赖一次 `.cpu()` 拷贝，未做大图性能测量（CPU 节点，优先级低）。

## 反例执行结果
| 反例 | 期望 | 结果 |
|---|---|---|
| block_size 偶数 | 报错 | PASS（ValueError） |
| block_size < 3 | 报错 | PASS（ValueError） |
| 全白图 | 输出形状不变 | PASS |
| 白底黑矩形 | 非零线像素 | PASS |
| invert=False | 与 True 不同 | PASS |
| batch>1 | 输出 batch=1 | PASS |
