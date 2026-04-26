from typing import Optional

from app.models import Product, ProductTrend, RecommendationItem, UserProfile
from app.services.explanation import build_reason_tags
from app.services.itemcf import recommend_with_itemcf
from app.services.llm_explanation import generate_explanation


def recommend_products(
    user: UserProfile,
    products: list[Product],
    limit: int,
    events: Optional[list[dict]] = None,
    product_trends: Optional[list[ProductTrend]] = None,
    direction_links: Optional[list[dict]] = None,
) -> list[RecommendationItem]:
    scored_products = []
    itemcf_scores = recommend_with_itemcf(user, products, events or [], limit=len(products)) if events else {}
    max_itemcf_score = max(itemcf_scores.values(), default=0)
    trend_scores = _build_trend_scores(products, product_trends or [])
    max_trend_score = max(trend_scores.values(), default=0)
    direction_role_by_product_id = _build_direction_role_map(direction_links or [])

    for product in products:
        if product.stock <= 0:
            continue

        if product.category in user.negative_tags:
            continue

        rule_score = _score_product(user, product)
        itemcf_score = itemcf_scores.get(product.product_id, 0)
        normalized_itemcf_score = itemcf_score / max_itemcf_score if max_itemcf_score else 0
        product_trend_score = trend_scores.get(product.product_id, 0)
        normalized_trend_score = product_trend_score / max_trend_score if max_trend_score else 0
        direction_product_role = direction_role_by_product_id.get(product.product_id)
        layered_boost = _score_direction_role(direction_product_role)
        score = rule_score + normalized_itemcf_score * 0.75 + normalized_trend_score * 0.35 + layered_boost
        recommendation_source = "itemcf" if itemcf_score > 0 else "profile_rule"
        reason_tags = build_reason_tags(
            user,
            product,
            recommendation_source,
            trend_score=normalized_trend_score,
            direction_product_role=direction_product_role,
        )
        explanation_result = generate_explanation(
            user,
            product,
            reason_tags,
            recommendation_source,
            direction_product_role=direction_product_role,
        )

        scored_products.append(
            RecommendationItem(
                product_id=product.product_id,
                title=product.title,
                category=product.category,
                brand=product.brand,
                price=product.price,
                image_url=product.image_url,
                score=round(score, 4),
                trend_score=round(normalized_trend_score, 4),
                recommendation_source=recommendation_source,
                direction_product_role=direction_product_role,
                reason_tags=reason_tags,
                explanation=explanation_result.text,
                explanation_provider=explanation_result.provider,
            )
        )

    return sorted(scored_products, key=lambda item: item.score, reverse=True)[:limit]


def _score_product(user: UserProfile, product: Product) -> float:
    score = 0.0

    interest_terms = set(user.long_term_interests + user.recent_interests)
    product_terms = {product.category, product.brand, *product.features}
    matched_terms = interest_terms & product_terms

    score += len(matched_terms) * 0.25

    if product.category in user.long_term_interests:
        score += 0.35

    if product.brand in user.brand_preference:
        score += 0.25

    if user.price_min <= product.price <= user.price_max:
        score += 0.2

    score += min(product.rating / 5, 1) * 0.2

    return score


def _build_trend_scores(products: list[Product], product_trends: list[ProductTrend]) -> dict[str, float]:
    scores: dict[str, float] = {product.product_id: 0.0 for product in products}

    for product in products:
        product_terms = {
            product.product_id.lower(),
            product.category.lower(),
            product.brand.lower(),
            product.title.lower(),
            *(feature.lower() for feature in product.features),
        }

        best_score = 0.0
        for trend in product_trends:
            trend_terms = {
                (trend.product_id or "").lower(),
                trend.category.lower(),
                trend.keyword.lower(),
            }
            if trend.product_id and trend.product_id == product.product_id:
                best_score = max(best_score, trend.trend_score)
                continue

            if trend.category == product.category or any(term and term in product_terms for term in trend_terms):
                best_score = max(best_score, trend.trend_score)

        scores[product.product_id] = best_score

    return scores


def _build_direction_role_map(direction_links: list[dict]) -> dict[str, str]:
    return {
        link["product_id"]: link["product_role"]
        for link in sorted(direction_links, key=lambda item: item.get("priority", 0))
        if link.get("product_id") and link.get("product_role")
    }


def _score_direction_role(direction_product_role: Optional[str]) -> float:
    if direction_product_role in {"核心商品", "入门款"}:
        return 0.18
    if direction_product_role == "进阶款":
        return 0.12
    if direction_product_role in {"搭配款", "替代款"}:
        return 0.08
    if direction_product_role:
        return 0.05
    return 0.0
