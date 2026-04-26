import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from app.models import Product, UserProfile


EVENT_WEIGHTS = {
    "view": 1.0,
    "click": 2.0,
    "favorite": 3.0,
    "add_to_cart": 4.0,
    "purchase": 5.0,
    "dislike": -3.0,
}


def load_seed_events() -> list[dict[str, Any]]:
    data_path = Path(__file__).resolve().parents[3] / "data" / "events.json"
    if not data_path.exists():
        return []

    with data_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def recommend_with_itemcf(
    user: UserProfile,
    products: list[Product],
    events: list[dict[str, Any]],
    limit: int,
) -> dict[str, float]:
    product_by_id = {product.product_id: product for product in products}
    user_item_scores = _build_user_item_scores(events)
    target_scores = user_item_scores.get(user.user_id, {})

    if not target_scores:
        return {}

    item_similarity = _build_item_similarity(user_item_scores)
    disliked_items = {
        product_id
        for product_id, score in target_scores.items()
        if score < 0
    }
    candidate_scores: dict[str, float] = defaultdict(float)

    for source_product_id, source_score in target_scores.items():
        if source_score <= 0:
            continue

        for candidate_id, similarity in item_similarity.get(source_product_id, {}).items():
            if candidate_id == source_product_id or candidate_id in disliked_items:
                continue

            candidate = product_by_id.get(candidate_id)
            if not candidate or candidate.stock <= 0:
                continue

            if candidate.category in user.negative_tags:
                continue

            candidate_scores[candidate_id] += source_score * similarity

    ranked = sorted(candidate_scores.items(), key=lambda item: item[1], reverse=True)[:limit]
    return {product_id: score for product_id, score in ranked}


def _build_user_item_scores(events: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    user_item_scores: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))

    for event in events:
        user_id = event.get("user_id")
        product_id = event.get("product_id")
        event_type = event.get("event_type")

        if not user_id or not product_id or event_type not in EVENT_WEIGHTS:
            continue

        user_item_scores[user_id][product_id] += EVENT_WEIGHTS[event_type]

    return {
        user_id: dict(product_scores)
        for user_id, product_scores in user_item_scores.items()
    }


def _build_item_similarity(user_item_scores: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    cooccurrence: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    item_norms: dict[str, float] = defaultdict(float)

    for product_scores in user_item_scores.values():
        positive_items = {
            product_id: score
            for product_id, score in product_scores.items()
            if score > 0
        }

        for product_id, score in positive_items.items():
            item_norms[product_id] += score * score

        items = list(positive_items.items())
        for left_index, (left_id, left_score) in enumerate(items):
            for right_id, right_score in items[left_index + 1:]:
                weighted = left_score * right_score
                cooccurrence[left_id][right_id] += weighted
                cooccurrence[right_id][left_id] += weighted

    similarities: dict[str, dict[str, float]] = defaultdict(dict)

    for left_id, related_items in cooccurrence.items():
        for right_id, weighted_count in related_items.items():
            denominator = math.sqrt(item_norms[left_id]) * math.sqrt(item_norms[right_id])
            if denominator == 0:
                continue

            similarities[left_id][right_id] = weighted_count / denominator

    return {
        product_id: dict(related_items)
        for product_id, related_items in similarities.items()
    }
