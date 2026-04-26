from typing import Optional

from app.models import Product, UserProfile


def build_reason_tags(
    user: UserProfile,
    product: Product,
    recommendation_source: Optional[str] = None,
    trend_score: float = 0,
    direction_product_role: Optional[str] = None,
) -> list[str]:
    tags: list[str] = []

    if recommendation_source == "itemcf":
        tags.append("相似行为推荐")

    interest_set = set(user.long_term_interests + user.recent_interests)
    product_set = {product.category, product.brand, *product.features}

    if interest_set & product_set:
        tags.append("近期兴趣相关")

    if product.category in user.long_term_interests:
        tags.append("类目偏好匹配")

    if product.brand in user.brand_preference:
        tags.append("品牌偏好匹配")

    if user.price_min <= product.price <= user.price_max:
        tags.append("价格区间匹配")

    if product.rating >= 4.6:
        tags.append("评分较高")

    if trend_score >= 0.65:
        tags.append("近期热度较高")

    if direction_product_role:
        tags.append(direction_product_role)

    if not tags:
        tags.append("热门商品推荐")

    return tags


def build_template_explanation(
    user: UserProfile,
    product: Product,
    reason_tags: list[str],
    recommendation_source: Optional[str] = None,
    direction_product_role: Optional[str] = None,
) -> str:
    if direction_product_role in {"入门款", "核心商品"} and "价格区间匹配" in reason_tags:
        return f"这款{product.category}更适合作为当前方向的{direction_product_role}，价格和上手门槛都比较友好。"

    if direction_product_role in {"搭配款", "替代款", "进阶款"}:
        return f"如果你准备沿这个方向继续补齐配置，这款{product.category}更适合作为{direction_product_role}来考虑。"

    if "近期热度较高" in reason_tags and recommendation_source == "itemcf":
        return f"这款{product.category}既和相似用户行为相关，近期整体热度也比较高。"

    if "近期热度较高" in reason_tags:
        return f"这款{product.category}与你的偏好方向接近，而且近期关注度也比较高。"

    if recommendation_source == "itemcf":
        return f"根据相似用户的浏览和加购行为，这款{product.category}与你近期兴趣有较高关联。"

    matched_features = [
        feature
        for feature in product.features
        if feature in user.long_term_interests or feature in user.recent_interests
    ]

    if matched_features:
        feature_text = "、".join(matched_features[:2])
        return f"根据你近期关注的{feature_text}，这款{product.category}在功能和口碑上比较符合你的偏好。"

    if "价格区间匹配" in reason_tags:
        return f"这款{product.category}的价格处于你常看的区间内，也有不错的用户评分。"

    if "品牌偏好匹配" in reason_tags:
        return f"你对{product.brand}相关商品有偏好，这款商品可以作为备选。"

    return f"这款{product.category}近期表现较好，可以作为你的参考选择。"


def build_explanation(
    user: UserProfile,
    product: Product,
    reason_tags: list[str],
    recommendation_source: Optional[str] = None,
    direction_product_role: Optional[str] = None,
) -> str:
    return build_template_explanation(
        user,
        product,
        reason_tags,
        recommendation_source,
        direction_product_role,
    )
