# ADR-0002: 依赖与 transformers 基线

状态：Accepted（2026-09-23）
背景：宿主环境 `transformers 5.14.1`；旧插件的 `trust_remote_code`（Florence-2 等）
在 v5 下逐层崩溃（`forced_bos_token_id`、`_supports_sdpa`、`GenerationMixin`、`_tied_weights_keys`）。
同时 `omnivoice(>=5.3.0)`、`dots.tts(>=4.57.0)`、`comfy 核心(>=4.50.3)` 与需 `<4.50` 的旧插件互斥。

## 决策
1. transformers 基线 = **5.x**（保留 TTS 全引擎）。
2. cfx 各包**禁止** `trust_remote_code`；需要旧模型时使用自带实现
   （如 Florence-2 采用 `ComfyUI-Florence2` 的 `comfy.ops` 实现）。
3. 4.x↔5.x 差异集中在 `packages/vision/compat.py`
   （`AutoModelForVision2Seq → AutoModelForImageTextToText`、
   `load_sharded_checkpoint` 回退 `safetensors.torch.load_model` 等）。
4. `core` 不依赖 `transformers`。

## 后果
正：单环境可共存、避免 remote code 崩溃。负：个别依赖 4.x 的旧能力需重写。
