import csv
import io
import json
import re
from pathlib import Path
from typing import Any, Optional

from app.models import Product, ProductImportPreviewItem
from app.services.database import upsert_product
from app.services.product_source_adapters import (
    build_product_adapter_info,
    detect_product_source_adapter,
    get_product_source_adapter,
    list_product_source_adapters,
)


SUPPORTED_SUFFIXES = {".json", ".csv"}
PLACEHOLDER_IMAGE_URL = "https://images.unsplash.com/photo-1523275335684-37898b6baf30"


def import_products_from_content(
    content: str,
    filename: Optional[str] = None,
    adapter_name: Optional[str] = None,
) -> dict[str, Any]:
    analysis = _analyze_product_content(content, filename=filename, adapter_name=adapter_name)
    imported_items: list[Product] = []

    for normalized in analysis["ready_items"]:
        saved_item = upsert_product(Product(**normalized))
        imported_items.append(saved_item)

    return {
        "adapter": analysis["adapter"],
        "total_count": analysis["total_count"],
        "ready_count": analysis["ready_count"],
        "error_count": analysis["error_count"],
        "imported_count": len(imported_items),
        "generated_product_id_count": analysis["generated_product_id_count"],
        "items": imported_items,
    }


def preview_products_from_content(
    content: str,
    filename: Optional[str] = None,
    adapter_name: Optional[str] = None,
) -> dict[str, Any]:
    analysis = _analyze_product_content(content, filename=filename, adapter_name=adapter_name)
    return {
        "adapter": analysis["adapter"],
        "adapter_description": analysis["adapter_description"],
        "total_count": analysis["total_count"],
        "ready_count": analysis["ready_count"],
        "error_count": analysis["error_count"],
        "generated_product_id_count": analysis["generated_product_id_count"],
        "detected_headers": analysis["detected_headers"],
        "mapped_headers": analysis["mapped_headers"],
        "unmapped_headers": analysis["unmapped_headers"],
        "items": analysis["preview_items"],
    }


def list_product_adapter_info() -> list[dict[str, str]]:
    return [build_product_adapter_info(adapter) for adapter in list_product_source_adapters()]


def _analyze_product_content(
    content: str,
    filename: Optional[str] = None,
    adapter_name: Optional[str] = None,
) -> dict[str, Any]:
    input_name = filename or "pasted_products"
    suffix = Path(input_name).suffix.lower()
    if suffix and suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Unsupported product file type: {suffix}")

    raw_rows, detected_adapter_name, detected_headers = load_rows_from_content(content, filename=input_name)
    adapter = get_product_source_adapter(adapter_name or detected_adapter_name)
    mapped_headers, unmapped_headers = analyze_header_mapping(detected_headers, adapter.name)

    preview_items: list[ProductImportPreviewItem] = []
    ready_items: list[dict[str, Any]] = []
    generated_ids = 0
    ready_count = 0
    error_count = 0

    for index, row in enumerate(raw_rows, start=1):
        try:
            normalized = normalize_row(
                row,
                index=index,
                source_name=Path(input_name).stem,
                adapter_name=adapter.name,
            )
            generated_product_id = bool(normalized.pop("_generated_product_id", False))
            validated = Product(**normalized)
            ready_items.append(validated.model_dump())
            ready_count += 1
            if generated_product_id:
                generated_ids += 1

            preview_items.append(
                ProductImportPreviewItem(
                    row_number=index,
                    status="ready",
                    product_id=validated.product_id,
                    title=validated.title,
                    category=validated.category,
                    brand=validated.brand,
                    source=validated.source,
                    external_id=validated.external_id,
                    price=validated.price,
                    stock=validated.stock,
                    rating=validated.rating,
                    popularity_score=validated.popularity_score,
                    sales_score=validated.sales_score,
                    generated_product_id=generated_product_id,
                )
            )
        except Exception as error:  # noqa: BLE001
            error_count += 1
            preview_items.append(
                ProductImportPreviewItem(
                    row_number=index,
                    status="error",
                    error=str(error),
                )
            )

    return {
        "adapter": adapter.name,
        "adapter_description": adapter.description,
        "total_count": len(raw_rows),
        "ready_count": ready_count,
        "error_count": error_count,
        "generated_product_id_count": generated_ids,
        "detected_headers": detected_headers,
        "mapped_headers": mapped_headers,
        "unmapped_headers": unmapped_headers,
        "preview_items": preview_items,
        "ready_items": ready_items,
    }


def load_rows_from_content(content: str, filename: str) -> tuple[list[dict[str, Any]], Optional[str], list[str]]:
    suffix = Path(filename).suffix.lower()

    if suffix == ".json" or content.lstrip().startswith("["):
        payload = json.loads(content)
        if not isinstance(payload, list):
            raise ValueError("Product JSON payload must be a list of objects")
        headers = collect_json_headers(payload)
        return payload, "generic", headers

    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)
    headers = [field.strip() for field in (reader.fieldnames or []) if field and field.strip()]
    detected_adapter = detect_product_source_adapter(reader.fieldnames or [])
    return rows, detected_adapter.name, headers


def collect_json_headers(payload: list[dict[str, Any]]) -> list[str]:
    headers: list[str] = []
    seen: set[str] = set()
    for row in payload:
        if not isinstance(row, dict):
            continue
        for key in row.keys():
            normalized = str(key).strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                headers.append(normalized)
    return headers


def analyze_header_mapping(headers: list[str], adapter_name: str) -> tuple[list[dict[str, str]], list[str]]:
    adapter = get_product_source_adapter(adapter_name)
    mapped_headers: list[dict[str, str]] = []
    unmapped_headers: list[str] = []

    for header in headers:
        normalized = header.strip().lower()
        target_field = adapter.column_aliases.get(normalized)
        if target_field:
            mapped_headers.append({"source_field": header, "target_field": target_field})
        else:
            unmapped_headers.append(header)

    return mapped_headers, unmapped_headers


def normalize_row(
    row: dict[str, Any],
    index: int,
    source_name: str,
    adapter_name: str,
) -> dict[str, Any]:
    adapter = get_product_source_adapter(adapter_name)
    transformed_row = adapter.row_transform(dict(row), index)
    normalized: dict[str, Any] = {}

    for key, value in transformed_row.items():
        canonical_key = adapter.column_aliases.get(str(key).strip().lower())
        if not canonical_key:
            continue
        normalized[canonical_key] = clean_value(value)

    title = str(normalized.get("title", "")).strip()
    category = str(normalized.get("category", "")).strip()
    if not title or not category:
        raise ValueError(f"Product row {index} is missing title or category")

    brand = str(normalized.get("brand") or "Unknown").strip()
    source = str(normalized.get("source") or source_name).strip()

    normalized["title"] = title
    normalized["category"] = category
    normalized["brand"] = brand or "Unknown"
    normalized["source"] = source
    normalized["description"] = str(normalized.get("description") or f"{title} 商品导入记录").strip()
    normalized["features"] = normalize_features(normalized.get("features"))
    normalized["image_url"] = str(normalized.get("image_url") or PLACEHOLDER_IMAGE_URL).strip()
    normalized["price"] = normalize_float(normalized.get("price", 0))
    normalized["stock"] = normalize_int(normalized.get("stock", 0))
    normalized["rating"] = normalize_rating(normalized.get("rating", 0))
    normalized["popularity_score"] = normalize_score(normalized.get("popularity_score", 0))
    normalized["sales_score"] = normalize_score(normalized.get("sales_score", 0))
    normalized["external_id"] = str(normalized.get("external_id") or "").strip() or None

    product_id = str(normalized.get("product_id") or "").strip()
    if not product_id:
        normalized["product_id"] = build_product_id(title, category, brand, index)
        normalized["_generated_product_id"] = True
    else:
        normalized["product_id"] = slugify(product_id)

    return normalized


def normalize_features(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [term for term in split_terms(str(value)) if term]


def normalize_float(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    return round(float(value), 2)


def normalize_int(value: Any) -> int:
    if value in (None, ""):
        return 0
    return max(0, int(float(value)))


def normalize_rating(value: Any) -> float:
    score = normalize_float(value)
    if 0 <= score <= 5:
        return score
    if 0 <= score <= 100:
        return round(score / 20, 2)
    return 0.0


def normalize_score(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    number = float(value)
    if 0 <= number <= 1:
        return round(number * 100, 2)
    return round(number, 2)


def clean_value(value: Any) -> Any:
    if isinstance(value, str):
        cleaned = value.strip()
        return cleaned or ""
    return value


def split_terms(value: str) -> list[str]:
    return [
        segment.strip()
        for segment in re.split(r"[,/|;，、\n]+", value)
        if segment.strip()
    ]


def build_product_id(title: str, category: str, brand: str, index: int) -> str:
    core = f"{slugify(category)}-{slugify(brand)}-{slugify(title)}"
    return f"imp_{core or f'product-{index}'}"


def slugify(value: str) -> str:
    normalized = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "-", value.strip().lower())
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized or "item"
