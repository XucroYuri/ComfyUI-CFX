"""Vision model registry: model families, Florence-2 tasks, and cache keys."""

FLORENCE2_TASKS = {
    "caption": "<CAPTION>",
    "detailed_caption": "<DETAILED_CAPTION>",
    "more_detailed_caption": "<MORE_DETAILED_CAPTION>",
    "tags": "<GENERATE_TAGS>",
    "mixed_caption": "<MIXED_CAPTION>",
    "mixed_caption_plus": "<MIX_CAPTION_PLUS>",
    "analyze": "<ANALYZE>",
    "ocr": "<OCR>",
    "region_caption": "<OD>",
    "dense_region_caption": "<DENSE_REGION_CAPTION>",
    "region_proposal": "<REGION_PROPOSAL>",
    "phrase_grounding": "<CAPTION_TO_PHRASE_GROUNDING>",
    "referring_expression_segmentation": "<REFERRING_EXPRESSION_SEGMENTATION>",
}

TEXT_TASKS = frozenset({
    "<CAPTION>",
    "<DETAILED_CAPTION>",
    "<MORE_DETAILED_CAPTION>",
    "<GENERATE_TAGS>",
    "<MIXED_CAPTION>",
    "<MIX_CAPTION_PLUS>",
    "<ANALYZE>",
    "<OCR>",
})

FLORENCE2_MODELS = (
    "MiaoshouAI/Florence-2-base-PromptGen-v2.0",
    "MiaoshouAI/Florence-2-large-PromptGen-v2.0",
    "MiaoshouAI/Florence-2-base-PromptGen-v1.5",
    "MiaoshouAI/Florence-2-large-PromptGen-v1.5",
    "microsoft/Florence-2-base",
    "microsoft/Florence-2-base-ft",
    "microsoft/Florence-2-large",
    "microsoft/Florence-2-large-ft",
)


def task_token(name: str) -> str:
    try:
        return FLORENCE2_TASKS[name]
    except KeyError:
        raise ValueError(f"unknown Florence-2 task {name!r}") from None


def is_text_task(token: str) -> bool:
    return token in TEXT_TASKS


def cache_key(family: str, path: str, precision: str, quantization: str = "none") -> tuple:
    """Stable key describing a loaded vision model."""
    return (family, path, precision, quantization)
