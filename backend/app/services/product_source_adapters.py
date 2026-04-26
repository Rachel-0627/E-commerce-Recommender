import re
from dataclasses import dataclass
from typing import Any, Callable, Optional


RowTransform = Callable[[dict[str, Any], int], dict[str, Any]]


def _identity_transform(row: dict[str, Any], _: int) -> dict[str, Any]:
    return row


def _catalog_transform(row: dict[str, Any], _: int) -> dict[str, Any]:
    if not _get_case_insensitive(row, "source"):
        row["source"] = "catalog_import"
    return row


def _bestseller_transform(row: dict[str, Any], _: int) -> dict[str, Any]:
    if not _get_case_insensitive(row, "source"):
        row["source"] = "bestseller_rank"

    if _get_case_insensitive(row, "sales_score") in (None, ""):
        rank_value = _get_case_insensitive(row, "rank")
        if rank_value not in (None, ""):
            try:
                rank_number = float(rank_value)
            except (TypeError, ValueError):
                return row
            row["sales_score"] = max(0.0, round(101 - min(rank_number, 100), 2))
    return row


def _amazon_bestseller_transform(row: dict[str, Any], _: int) -> dict[str, Any]:
    if not _get_case_insensitive(row, "source"):
        row["source"] = "amazon_bestsellers"

    rank_value = _get_case_insensitive(row, "bestseller rank") or _get_case_insensitive(row, "rank")
    if _get_case_insensitive(row, "sales_score") in (None, "") and rank_value not in (None, ""):
        try:
            rank_number = float(rank_value)
        except (TypeError, ValueError):
            rank_number = None
        if rank_number is not None:
            row["sales_score"] = max(0.0, round(101 - min(rank_number, 100), 2))

    review_count = _get_case_insensitive(row, "review count") or _get_case_insensitive(row, "reviews")
    if _get_case_insensitive(row, "popularity_score") in (None, "") and review_count not in (None, ""):
        try:
            review_number = float(review_count)
        except (TypeError, ValueError):
            review_number = None
        if review_number is not None:
            row["popularity_score"] = round(min(review_number / 20, 100), 2)

    return row


def _shopify_transform(row: dict[str, Any], _: int) -> dict[str, Any]:
    if not _get_case_insensitive(row, "source"):
        row["source"] = "shopify_export"

    body_html = _get_case_insensitive(row, "body_html") or _get_case_insensitive(row, "body (html)")
    if body_html and not _get_case_insensitive(row, "description"):
        row["description"] = _strip_html(str(body_html))

    if _get_case_insensitive(row, "external_id") in (None, ""):
        row["external_id"] = _get_case_insensitive(row, "variant sku") or _get_case_insensitive(row, "handle")

    return row


def _jd_transform(row: dict[str, Any], _: int) -> dict[str, Any]:
    if not _get_case_insensitive(row, "source"):
        row["source"] = "jd_catalog"
    return row


def _strip_html(value: str) -> str:
    normalized = re.sub(r"<br\s*/?>", " ", value, flags=re.IGNORECASE)
    normalized = re.sub(r"<[^>]+>", " ", normalized)
    return " ".join(normalized.split())


def _get_case_insensitive(row: dict[str, Any], key: str) -> Any:
    target = key.strip().lower()
    for row_key, value in row.items():
        if str(row_key).strip().lower() == target:
            return value
    return None


@dataclass(frozen=True)
class ProductSourceAdapter:
    name: str
    description: str
    column_aliases: dict[str, str]
    header_signatures: tuple[str, ...]
    preset_mappings: tuple[tuple[str, str], ...] = ()
    row_transform: RowTransform = _identity_transform


GENERIC_ADAPTER = ProductSourceAdapter(
    name="generic",
    description="通用商品导入，适合手工整理后的 JSON/CSV 商品清单。",
    column_aliases={
        "product_id": "product_id",
        "id": "product_id",
        "external_id": "external_id",
        "item_id": "external_id",
        "source": "source",
        "title": "title",
        "product_name": "title",
        "name": "title",
        "商品名称": "title",
        "商品标题": "title",
        "category": "category",
        "类目": "category",
        "一级类目": "category",
        "brand": "brand",
        "品牌": "brand",
        "price": "price",
        "sale_price": "price",
        "价格": "price",
        "description": "description",
        "summary": "description",
        "商品简介": "description",
        "features": "features",
        "feature_tags": "features",
        "tags": "features",
        "标签": "features",
        "image_url": "image_url",
        "image": "image_url",
        "image_link": "image_url",
        "图片链接": "image_url",
        "stock": "stock",
        "inventory": "stock",
        "库存": "stock",
        "rating": "rating",
        "score": "rating",
        "评分": "rating",
        "popularity_score": "popularity_score",
        "trend_score": "popularity_score",
        "hot_score": "popularity_score",
        "热度指数": "popularity_score",
        "sales_score": "sales_score",
        "sales_index": "sales_score",
        "销量指数": "sales_score",
        "rank": "rank",
        "sku": "external_id",
        "商品sku": "external_id",
    },
    header_signatures=(),
    preset_mappings=(
        ("title", "title"),
        ("category", "category"),
        ("brand", "brand"),
        ("price", "price"),
        ("image_url", "image_url"),
    ),
)


ECOMMERCE_CATALOG_ADAPTER = ProductSourceAdapter(
    name="ecommerce_catalog",
    description="适配电商商品清单导出，重点读取商品名、价格、库存和评分。",
    column_aliases={
        **GENERIC_ADAPTER.column_aliases,
        "product title": "title",
        "product category": "category",
        "product brand": "brand",
        "unit price": "price",
        "inventory count": "stock",
        "review rating": "rating",
        "thumbnail": "image_url",
        "hotness": "popularity_score",
        "sales volume score": "sales_score",
    },
    header_signatures=("product title", "unit price"),
    preset_mappings=(
        ("Product Title", "title"),
        ("Product Category", "category"),
        ("Product Brand", "brand"),
        ("Unit Price", "price"),
        ("Inventory Count", "stock"),
        ("Review Rating", "rating"),
    ),
    row_transform=_catalog_transform,
)


BESTSELLER_RANK_ADAPTER = ProductSourceAdapter(
    name="bestseller_rank",
    description="适配热销榜商品导出，支持排名、热度和销量信号。",
    column_aliases={
        **GENERIC_ADAPTER.column_aliases,
        "product name": "title",
        "hot rank": "rank",
        "sales volume score": "sales_score",
        "hotness": "popularity_score",
    },
    header_signatures=("product name", "rank"),
    preset_mappings=(
        ("Product Name", "title"),
        ("Rank", "sales_score"),
        ("Hotness", "popularity_score"),
    ),
    row_transform=_bestseller_transform,
)


AMAZON_BESTSELLERS_ADAPTER = ProductSourceAdapter(
    name="amazon_bestsellers",
    description="适配 Amazon Best Sellers 导出，支持 ASIN、排名、评论数和评分字段。",
    column_aliases={
        **GENERIC_ADAPTER.column_aliases,
        "asin": "external_id",
        "title": "title",
        "main category": "category",
        "review count": "reviews",
        "reviews": "reviews",
        "bestseller rank": "rank",
        "image url": "image_url",
    },
    header_signatures=("asin", "bestseller rank"),
    preset_mappings=(
        ("ASIN", "external_id"),
        ("Title", "title"),
        ("Main Category", "category"),
        ("Bestseller Rank", "sales_score"),
        ("Review Count", "popularity_score"),
    ),
    row_transform=_amazon_bestseller_transform,
)


SHOPIFY_PRODUCTS_ADAPTER = ProductSourceAdapter(
    name="shopify_products",
    description="适配 Shopify 商品导出，支持 Handle、Vendor、Tags、Variant Price 等字段。",
    column_aliases={
        **GENERIC_ADAPTER.column_aliases,
        "handle": "external_id",
        "vendor": "brand",
        "type": "category",
        "body (html)": "body_html",
        "variant price": "price",
        "variant inventory qty": "stock",
        "variant sku": "external_id",
        "image src": "image_url",
    },
    header_signatures=("handle", "vendor", "variant price"),
    preset_mappings=(
        ("Handle", "external_id"),
        ("Vendor", "brand"),
        ("Type", "category"),
        ("Body (HTML)", "description"),
        ("Variant Price", "price"),
        ("Variant Inventory Qty", "stock"),
    ),
    row_transform=_shopify_transform,
)


JD_CATALOG_ADAPTER = ProductSourceAdapter(
    name="jd_catalog",
    description="适配京东商品导出，支持中文表头、SKU、热度指数和销量指数。",
    column_aliases={
        **GENERIC_ADAPTER.column_aliases,
        "商品sku": "external_id",
        "sku编号": "external_id",
    },
    header_signatures=("商品名称", "价格", "商品sku"),
    preset_mappings=(
        ("商品名称", "title"),
        ("类目", "category"),
        ("品牌", "brand"),
        ("价格", "price"),
        ("商品SKU", "external_id"),
        ("热度指数", "popularity_score"),
        ("销量指数", "sales_score"),
    ),
    row_transform=_jd_transform,
)


ADAPTERS = {
    GENERIC_ADAPTER.name: GENERIC_ADAPTER,
    ECOMMERCE_CATALOG_ADAPTER.name: ECOMMERCE_CATALOG_ADAPTER,
    BESTSELLER_RANK_ADAPTER.name: BESTSELLER_RANK_ADAPTER,
    AMAZON_BESTSELLERS_ADAPTER.name: AMAZON_BESTSELLERS_ADAPTER,
    SHOPIFY_PRODUCTS_ADAPTER.name: SHOPIFY_PRODUCTS_ADAPTER,
    JD_CATALOG_ADAPTER.name: JD_CATALOG_ADAPTER,
}


def list_product_source_adapters() -> list[ProductSourceAdapter]:
    return [ADAPTERS[name] for name in sorted(ADAPTERS)]


def build_product_adapter_info(adapter: ProductSourceAdapter) -> dict[str, Any]:
    return {
        "name": adapter.name,
        "description": adapter.description,
        "header_signatures": list(adapter.header_signatures),
        "field_mappings": [
            {"source_field": source_field, "target_field": target_field}
            for source_field, target_field in adapter.preset_mappings
        ],
    }


def get_product_source_adapter(name: Optional[str]) -> ProductSourceAdapter:
    if not name:
        return GENERIC_ADAPTER
    if name not in ADAPTERS:
        available = ", ".join(sorted(ADAPTERS))
        raise ValueError(f"Unknown product adapter '{name}'. Available adapters: {available}")
    return ADAPTERS[name]


def detect_product_source_adapter(field_names: list[str]) -> ProductSourceAdapter:
    normalized_headers = {field.strip().lower() for field in field_names}

    for adapter in list_product_source_adapters():
        if not adapter.header_signatures:
            continue
        if all(signature in normalized_headers for signature in adapter.header_signatures):
            return adapter

    return GENERIC_ADAPTER
