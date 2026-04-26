from dataclasses import dataclass
from typing import Any, Callable, Optional


RowTransform = Callable[[dict[str, Any], int], dict[str, Any]]


def _identity_transform(row: dict[str, Any], _: int) -> dict[str, Any]:
    return row


def _google_trends_transform(row: dict[str, Any], _: int) -> dict[str, Any]:
    if not row.get("source"):
        row["source"] = "google_trends"
    return row


def _ecommerce_rank_transform(row: dict[str, Any], _: int) -> dict[str, Any]:
    if not row.get("source"):
        row["source"] = "ecommerce_rank"

    rank_value = row.get("rank")
    sales_score = row.get("sales_score")
    if (sales_score in (None, "")) and rank_value not in (None, ""):
        try:
            rank_number = float(rank_value)
        except (TypeError, ValueError):
            return row

        row["sales_score"] = max(0.0, round(101 - min(rank_number, 100), 2))
    return row


@dataclass(frozen=True)
class SourceAdapter:
    name: str
    description: str
    column_aliases: dict[str, str]
    header_signatures: tuple[str, ...]
    preset_mappings: tuple[tuple[str, str], ...] = ()
    row_transform: RowTransform = _identity_transform


GENERIC_ADAPTER = SourceAdapter(
    name="generic",
    description="通用 JSON/CSV 趋势导入，适合手工整理后的榜单或调研结果。",
    column_aliases={
        "trend_id": "trend_id",
        "id": "trend_id",
        "product_id": "product_id",
        "source": "source",
        "keyword": "keyword",
        "query": "keyword",
        "trend_keyword": "keyword",
        "category": "category",
        "trend_score": "trend_score",
        "hot_score": "trend_score",
        "popularity_score": "trend_score",
        "sales_score": "sales_score",
        "sales_rank_score": "sales_score",
    },
    header_signatures=(),
    preset_mappings=(
        ("keyword", "keyword"),
        ("category", "category"),
        ("trend_score", "trend_score"),
        ("sales_score", "sales_score"),
    ),
)


GOOGLE_TRENDS_ADAPTER = SourceAdapter(
    name="google_trends",
    description="适配 Google Trends 风格导出，重点读取搜索词和热度分。",
    column_aliases={
        **GENERIC_ADAPTER.column_aliases,
        "search term": "keyword",
        "search_query": "keyword",
        "topic": "keyword",
        "interest score": "trend_score",
        "interest_over_time": "trend_score",
    },
    header_signatures=("search term", "interest score"),
    preset_mappings=(
        ("Search Term", "keyword"),
        ("Interest Score", "trend_score"),
        ("source", "source"),
    ),
    row_transform=_google_trends_transform,
)


ECOMMERCE_RANK_ADAPTER = SourceAdapter(
    name="ecommerce_rank",
    description="适配电商榜单/热销榜导出，支持商品名、热度分和排名列。",
    column_aliases={
        **GENERIC_ADAPTER.column_aliases,
        "product name": "keyword",
        "item_name": "keyword",
        "name": "keyword",
        "rank": "rank",
        "sales index": "sales_score",
        "sales volume score": "sales_score",
        "hot score": "trend_score",
        "hotness": "trend_score",
    },
    header_signatures=("product name", "rank"),
    preset_mappings=(
        ("Product Name", "keyword"),
        ("Rank", "sales_score"),
        ("Hot Score", "trend_score"),
    ),
    row_transform=_ecommerce_rank_transform,
)


ADAPTERS = {
    GENERIC_ADAPTER.name: GENERIC_ADAPTER,
    GOOGLE_TRENDS_ADAPTER.name: GOOGLE_TRENDS_ADAPTER,
    ECOMMERCE_RANK_ADAPTER.name: ECOMMERCE_RANK_ADAPTER,
}


def list_adapters() -> list[SourceAdapter]:
    return [ADAPTERS[name] for name in sorted(ADAPTERS)]


def build_trend_adapter_info(adapter: SourceAdapter) -> dict[str, Any]:
    return {
        "name": adapter.name,
        "description": adapter.description,
        "header_signatures": list(adapter.header_signatures),
        "field_mappings": [
            {"source_field": source_field, "target_field": target_field}
            for source_field, target_field in adapter.preset_mappings
        ],
    }


def get_adapter(name: Optional[str]) -> SourceAdapter:
    if not name:
        return GENERIC_ADAPTER
    if name not in ADAPTERS:
        available = ", ".join(sorted(ADAPTERS))
        raise ValueError(f"Unknown adapter '{name}'. Available adapters: {available}")
    return ADAPTERS[name]


def detect_adapter(field_names: list[str]) -> SourceAdapter:
    normalized_headers = {field.strip().lower() for field in field_names}

    for adapter in list_adapters():
        if not adapter.header_signatures:
            continue
        if all(signature in normalized_headers for signature in adapter.header_signatures):
            return adapter

    return GENERIC_ADAPTER
