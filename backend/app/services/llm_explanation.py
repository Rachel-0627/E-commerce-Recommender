import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional

from app.models import Product, UserProfile
from app.services.explanation import build_template_explanation


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
BLOCKED_PHRASES = ["最适合", "一定喜欢", "保证", "全网第一", "昨晚", "具体位置"]


@dataclass
class ExplanationResult:
    text: str
    provider: str


def get_llm_status() -> dict[str, object]:
    provider = os.getenv("LLM_PROVIDER", "template").strip().lower()
    api_key = os.getenv("OPENAI_API_KEY", "")
    model = os.getenv("OPENAI_MODEL", "")

    return {
        "provider": provider,
        "openai_configured": bool(api_key and model),
        "model": model or None,
        "fallback": "template",
    }


def generate_explanation(
    user: UserProfile,
    product: Product,
    reason_tags: list[str],
    recommendation_source: Optional[str] = None,
    direction_product_role: Optional[str] = None,
) -> ExplanationResult:
    template_text = build_template_explanation(
        user,
        product,
        reason_tags,
        recommendation_source,
        direction_product_role,
    )
    provider = os.getenv("LLM_PROVIDER", "template").strip().lower()

    if provider != "openai":
        return ExplanationResult(text=template_text, provider="template")

    api_key = os.getenv("OPENAI_API_KEY", "")
    model = os.getenv("OPENAI_MODEL", "")

    if not api_key or not model:
        return ExplanationResult(text=template_text, provider="template_missing_config")

    try:
        llm_text = _call_openai_responses_api(
            api_key=api_key,
            model=model,
            user=user,
            product=product,
            reason_tags=reason_tags,
            recommendation_source=recommendation_source,
            direction_product_role=direction_product_role,
        )
    except (TimeoutError, urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError, json.JSONDecodeError):
        return ExplanationResult(text=template_text, provider="template_fallback")

    cleaned_text = _clean_text(llm_text)
    if not _is_safe_explanation(cleaned_text):
        return ExplanationResult(text=template_text, provider="template_safety_fallback")

    return ExplanationResult(text=cleaned_text, provider="openai")


def _call_openai_responses_api(
    api_key: str,
    model: str,
    user: UserProfile,
    product: Product,
    reason_tags: list[str],
    recommendation_source: Optional[str],
    direction_product_role: Optional[str],
) -> str:
    prompt = _build_prompt(user, product, reason_tags, recommendation_source, direction_product_role)
    payload = {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": (
                    "你是电商推荐解释助手。只根据给定证据生成一句中文推荐解释，"
                    "不要编造商品信息，不要暴露隐私，不要使用绝对化营销词。"
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "max_output_tokens": 120,
    }
    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=12) as response:
        data = json.loads(response.read().decode("utf-8"))

    return _extract_response_text(data)


def _build_prompt(
    user: UserProfile,
    product: Product,
    reason_tags: list[str],
    recommendation_source: Optional[str],
    direction_product_role: Optional[str],
) -> str:
    evidence = {
        "user_profile": {
            "long_term_interests": user.long_term_interests,
            "recent_interests": user.recent_interests,
            "brand_preference": user.brand_preference,
            "price_range": [user.price_min, user.price_max],
        },
        "product": {
            "title": product.title,
            "category": product.category,
            "brand": product.brand,
            "price": product.price,
            "description": product.description,
            "features": product.features,
            "rating": product.rating,
        },
        "recommendation": {
            "source": recommendation_source,
            "reason_tags": reason_tags,
            "direction_product_role": direction_product_role,
        },
    }

    return (
        "请根据以下 JSON 证据生成一句不超过 50 个中文字符的推荐解释。\n"
        "要求：自然、具体、可信；不要出现“最适合”“一定喜欢”“保证”等绝对化表达；"
        "不要提到具体行为时间、位置或敏感个人信息。\n\n"
        f"{json.dumps(evidence, ensure_ascii=False)}"
    )


def _extract_response_text(data: dict) -> str:
    output_text = data.get("output_text")
    if output_text:
        return output_text

    parts = []
    for output_item in data.get("output", []):
        for content_item in output_item.get("content", []):
            if content_item.get("type") in {"output_text", "text"} and content_item.get("text"):
                parts.append(content_item["text"])

    if not parts:
        raise ValueError("OpenAI response did not include text output")

    return "\n".join(parts)


def _clean_text(text: str) -> str:
    cleaned = " ".join(text.strip().split())
    return cleaned[:90]


def _is_safe_explanation(text: str) -> bool:
    if not text or len(text) > 90:
        return False

    return not any(phrase in text for phrase in BLOCKED_PHRASES)
