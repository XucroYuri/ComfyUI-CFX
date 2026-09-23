# Adversarial Review: comfyui_segment_face_crop

reviewer: Adversary
date: 2026-09-24
verdict: PASS

## 通过项
- **去重**：统一到一份 MIT RetinaFace 实现；AGSoft 的重复副本可删除。
- §7 后端缺失报 `FileNotFoundError` 且含期望目录。
- 直接透传上游返回值，不在中间层加工 `CROP_DATA`。

## 实测修正
- §8.1 经真实推理核实：**未检出人脸时上游返回原图与默认 crop data**（非空 batch），
  已按实测修正 SPEC；同时记录「单张检出返回单张量」的上游不规则返回形态。

## 未决疑点
1. 依赖上游 `AutoCropFaces.auto_crop_faces` 签名；已提供 `CFX_FACECROP_DIR` 覆盖。
2. 暴露上游自定义类型 `CROP_DATA`；若上游移除该类型会破坏，但类型名保持原样以兼容。
3. 上游返回形态不规则（原图 / 单张量 / batch），下游需能接受 IMAGE。
