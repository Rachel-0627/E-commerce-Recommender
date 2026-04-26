import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "backend"))

from app.sample_data import PRODUCTS, USERS  # noqa: E402


EVENT_WEIGHTS = [
    ("view", 0.42),
    ("click", 0.28),
    ("favorite", 0.12),
    ("add_to_cart", 0.1),
    ("purchase", 0.05),
    ("dislike", 0.03),
]


SYNTHETIC_USER_GROUPS = {
    "runner": {
        "users": [f"u_runner_{index:03d}" for index in range(1, 25)],
        "preferred_categories": {"运动鞋", "健身装备"},
        "preferred_features": {"跑步", "训练", "缓震", "透气", "长跑", "支撑"},
    },
    "home": {
        "users": [f"u_home_{index:03d}" for index in range(1, 25)],
        "preferred_categories": {"厨房", "收纳"},
        "preferred_features": {"咖啡", "厨房", "家居", "收纳", "办公"},
    },
    "mixed": {
        "users": [f"u_mixed_{index:03d}" for index in range(1, 13)],
        "preferred_categories": {"运动鞋", "健身装备", "厨房", "收纳"},
        "preferred_features": {"跑步", "透气", "咖啡", "家居", "办公"},
    },
    "beauty": {
        "users": [f"u_beauty_{index:03d}" for index in range(1, 20)],
        "preferred_categories": {"护肤", "彩妆"},
        "preferred_features": {"补水", "保湿", "抗老", "防晒", "玻尿酸", "成分党", "维C", "敏感肌"},
    },
    "tech": {
        "users": [f"u_tech_{index:03d}" for index in range(1, 20)],
        "preferred_categories": {"耳机", "智能设备", "电脑配件", "音频设备", "电源配件"},
        "preferred_features": {"降噪", "无线", "快充", "Type-C", "机械键盘", "高音质", "办公"},
    },
    "pet": {
        "users": [f"u_pet_{index:03d}" for index in range(1, 16)],
        "preferred_categories": {"宠物用品", "宠物食品", "宠物玩具", "宠物保健"},
        "preferred_features": {"猫咪", "冻干", "无添加", "自动喂食", "营养", "益生菌", "宠物健康"},
    },
}


def main() -> None:
    random.seed(20260415)
    data_dir = ROOT_DIR / "data"
    data_dir.mkdir(exist_ok=True)

    users = list(USERS.keys())
    for group in SYNTHETIC_USER_GROUPS.values():
        users.extend(group["users"])

    events = []
    now = datetime(2026, 4, 15, 10, 0, 0)

    for user_id in users:
        profile = _profile_for_user(user_id)
        event_count = 18 if user_id in USERS else random.randint(8, 22)
        candidate_products = _rank_products_for_profile(profile)

        for index in range(event_count):
            product = random.choices(
                candidate_products,
                weights=[weight for _, weight in candidate_products],
                k=1,
            )[0][0]
            event_type = _choose_event_type(product, profile)
            timestamp = now - timedelta(hours=random.randint(1, 900), minutes=random.randint(0, 59))

            events.append(
                {
                    "event_id": f"evt_{uuid4().hex[:12]}",
                    "user_id": user_id,
                    "product_id": product.product_id,
                    "event_type": event_type,
                    "scene": random.choice(["home", "detail", "cart"]),
                    "request_id": f"seed_{index:03d}",
                    "timestamp": timestamp.isoformat(),
                }
            )

    events.sort(key=lambda item: item["timestamp"])

    output_path = data_dir / "events.json"
    output_path.write_text(json.dumps(events, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(events)} events to {output_path}")


def _profile_for_user(user_id: str) -> dict[str, set[str]]:
    if user_id == "u_001":
        return {
            "categories": {"运动鞋", "健身装备"},
            "features": {"跑步", "马拉松", "缓震", "透气", "长跑", "支撑"},
        }

    if user_id == "u_002":
        return {
            "categories": {"家居", "收纳", "厨房"},
            "features": {"咖啡", "餐具", "厨房", "家居", "收纳", "办公"},
        }

    if user_id == "u_003":
        return {
            "categories": {"护肤", "彩妆"},
            "features": {"玻尿酸", "补水", "保湿", "抗老", "防晒", "维C", "敏感肌", "成分党"},
        }

    if user_id == "u_004":
        return {
            "categories": {"耳机", "智能设备", "电脑配件", "音频设备", "电源配件"},
            "features": {"降噪", "无线", "LDAC", "高音质", "机械键盘", "快充", "Type-C", "办公"},
        }

    if user_id == "u_005":
        return {
            "categories": {"宠物用品", "宠物食品", "宠物玩具", "宠物保健"},
            "features": {"猫咪", "冻干", "无添加", "自动喂食", "营养", "益生菌", "宠物健康", "高蛋白"},
        }

    for group_name, group in SYNTHETIC_USER_GROUPS.items():
        if user_id in group["users"]:
            return {
                "categories": set(group["preferred_categories"]),
                "features": set(group["preferred_features"]),
            }

    return {"categories": set(), "features": set()}


def _rank_products_for_profile(profile: dict[str, set[str]]) -> list[tuple[object, float]]:
    ranked = []

    for product in PRODUCTS:
        weight = 1.0

        if product.category in profile["categories"]:
            weight += 3.0

        feature_overlap = profile["features"] & set(product.features)
        weight += len(feature_overlap) * 1.4

        ranked.append((product, weight))

    return ranked


def _choose_event_type(product, profile: dict[str, set[str]]) -> str:
    event_names = [name for name, _ in EVENT_WEIGHTS]
    event_weights = [weight for _, weight in EVENT_WEIGHTS]

    if product.category in profile["categories"] or profile["features"] & set(product.features):
        event_weights = [0.34, 0.31, 0.15, 0.12, 0.06, 0.02]

    return random.choices(event_names, weights=event_weights, k=1)[0]


if __name__ == "__main__":
    main()
