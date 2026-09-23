---
id: comfyui_segment_face_crop
display_name: "ComfyUI-Segment · Face Crop"
category: "ComfyUI-Segment/Face"
version: 1.0.0
license: MIT
since: 2026-09-24
replaces:
  - "AutoCropFaces (ComfyUI-AutoCropFaces，作为 MIT 后端复用而非替代)"
  - "AGSoftCropFace（与 AutoCropFaces 同源副本，删除）"
---

## 1. 目的
人脸检测 + 裁剪的**唯一**入口，复用 MIT 的 `ComfyUI-AutoCropFaces`（RetinaFace）后端，
不再保留 AGSoft 的字节级重复副本。

## 2. 语义
- 透传到上游 `AutoCropFaces().auto_crop_faces(...)`；
- 返回 `(IMAGE 裁剪人脸, CROP_DATA)`；`CROP_DATA` 为上游自定义类型（原样透传）。

## 3. 接口
| 方向 | 名称 | 类型 | 必填 | 默认 |
|---|---|---|---|---|
| in | image | IMAGE | 是 | - |
| in | number_of_faces | INT | 是 | 5 |
| in | scale_factor | FLOAT | 是 | 1.5 |
| in | shift_factor | FLOAT | 是 | 0.45 |
| in | aspect_ratio | COMBO | 是 | 1:1 |
| in | start_index | INT | 否 | 0 |
| in | max_faces_per_image | INT | 否 | 50 |
| out | faces | IMAGE | - | - |
| out | crop_data | CROP_DATA | - | - |

## 4. 执行与缓存
上游模型在首次调用时加载。

## 5. 资源
RetinaFace MobileNet0.25（轻量），权重随上游插件自带。

## 6. 副作用与安全
无网络（权重随插件）。

## 7. 错误行为
后端缺失 → `FileNotFoundError`（含期望目录）。

## 8. 对抗性反例
1. **未检出人脸 → 上游返回原图与默认 crop data**（`(image, [(0,0,W,H), ...])`），不是空 batch；
2. `CFX_FACECROP_DIR` 覆盖路径；
3. 后端不存在 → 清晰报错；
4. 单张检出 → 返回单个张量而非 batch（上游既有行为，透传）。

## 9. 验收
`tests/test_segment_face.py`（后端定位/接口）；真实推理**已人工验证**（见 DEVLOG）。
