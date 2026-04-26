from typing import Optional

from app.models import (
    Direction,
    DirectionRecommendationItem,
    DirectionRecommendationRequest,
    DirectionStarterProduct,
    Product,
    UserProfile,
)


def recommend_directions(
    directions: list[Direction],
    products_by_direction: dict[str, list[DirectionStarterProduct]],
    request: DirectionRecommendationRequest,
    user: Optional[UserProfile] = None,
) -> list[DirectionRecommendationItem]:
    interest_terms = set(request.interests + request.preferred_categories)
    budget = request.budget

    if user:
        interest_terms.update(user.long_term_interests)
        interest_terms.update(user.recent_interests)
        interest_terms.update(user.brand_preference)
        if budget is None:
            budget = (user.price_min + user.price_max) / 2

    scored_directions = []
    has_resources = bool(request.existing_resources)

    for direction in directions:
        score = 0.0
        reasons: list[str] = []

        overlap = interest_terms & (set(direction.target_interests) | {direction.category})
        if overlap:
            matched = sorted(overlap)[:2]
            score += len(overlap) * 0.4
            reasons.append(f"与你关注的{'、'.join(matched)}更匹配")

        if budget is not None and direction.budget_min <= budget <= direction.budget_max:
            score += 0.35
            reasons.append("预算范围匹配")
        elif budget is not None and _ranges_overlap(direction.budget_min, direction.budget_max, budget):
            score += 0.15
            reasons.append("预算接近可接受区间")

        if not has_resources and direction.difficulty_level in {"入门", "低门槛"}:
            score += 0.25
            reasons.append("适合从低门槛方向开始")

        if request.preferred_categories and direction.category in request.preferred_categories:
            score += 0.25
            reasons.append("符合你当前倾向的品类")

        if not reasons:
            reasons.append("可以作为当前阶段的起步方向")

        scored_directions.append(
            DirectionRecommendationItem(
                direction_id=direction.direction_id,
                title=direction.title,
                category=direction.category,
                description=direction.description,
                target_scene=direction.target_scene,
                difficulty_level=direction.difficulty_level,
                budget_min=direction.budget_min,
                budget_max=direction.budget_max,
                score=round(score, 4),
                reasons=reasons,
                starter_products=products_by_direction.get(direction.direction_id, [])[:3],
            )
        )

    return sorted(scored_directions, key=lambda item: item.score, reverse=True)[: request.limit]


def build_direction_products(
    products: list[Product],
    links: list[dict],
) -> dict[str, list[DirectionStarterProduct]]:
    products_by_id = {product.product_id: product for product in products}
    grouped: dict[str, list[DirectionStarterProduct]] = {}

    for link in sorted(links, key=lambda item: (item["direction_id"], item["priority"])):
        product = products_by_id.get(link["product_id"])
        if not product:
            continue

        grouped.setdefault(link["direction_id"], []).append(
            DirectionStarterProduct(
                product_id=product.product_id,
                title=product.title,
                category=product.category,
                brand=product.brand,
                price=product.price,
                product_role=link["product_role"],
                priority=link["priority"],
            )
        )

    return grouped


def _ranges_overlap(budget_min: float, budget_max: float, budget: float) -> bool:
    return budget_min <= budget * 1.2 and budget_max >= budget * 0.8
