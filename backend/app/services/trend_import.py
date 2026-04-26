import csv
import io
import json
import re
from pathlib import Path
from typing import Any, Optional

from app.models import Product, ProductTrend, ProductTrendImportPreviewItem
from app.services.database import list_products, upsert_product_trend
from app.services.trend_source_adapters import detect_adapter, get_adapter, list_adapters
from app.services.trend_source_adapters import build_trend_adapter_info


SUPPORTED_SUFFIXES = {".json", ".csv"}


def import_product_trends_from_content(
    content: str,
    filename: Optional[str] = None,
    adapter_name: Optional[str] = None,
) -> dict[str, Any]:
    analysis = _analyze_product_trend_content(content, filename=filename, adapter_name=adapter_name)
    imported_items: list[ProductTrend] = []

    for normalized in analysis["ready_items"]:
        saved_item = upsert_product_trend(ProductTrend(**normalized))
        imported_items.append(saved_item)

    return {
        "adapter": analysis["adapter"],
        "total_count": analysis["total_count"],
        "ready_count": analysis["ready_count"],
        "error_count": analysis["error_count"],
        "imported_count": len(imported_items),
        "mapped_count": analysis["mapped_count"],
        "generated_trend_id_count": analysis["generated_trend_id_count"],
        "items": imported_items,
    }


def preview_product_trends_from_content(
    content: str,
    filename: Optional[str] = None,
    adapter_name: Optional[str] = None,
) -> dict[str, Any]:
    analysis = _analyze_product_trend_content(content, filename=filename, adapter_name=adapter_name)
    return {
        "adapter": analysis["adapter"],
        "adapter_description": analysis["adapter_description"],
        "total_count": analysis["total_count"],
        "ready_count": analysis["ready_count"],
        "error_count": analysis["error_count"],
        "mapped_count": analysis["mapped_count"],
        "generated_trend_id_count": analysis["generated_trend_id_count"],
        "detected_headers": analysis["detected_headers"],
        "mapped_headers": analysis["mapped_headers"],
        "unmapped_headers": analysis["unmapped_headers"],
        "items": analysis["preview_items"],
    }


def list_adapter_info() -> list[dict[str, str]]:
    return [build_trend_adapter_info(adapter) for adapter in list_adapters()]


def _analyze_product_trend_content(
    content: str,
    filename: Optional[str] = None,
    adapter_name: Optional[str] = None,
) -> dict[str, Any]:
    input_name = filename or "pasted_trends"
    suffix = Path(input_name).suffix.lower()
    if suffix and suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Unsupported trend file type: {suffix}")

    raw_rows, detected_adapter_name, detected_headers = load_rows_from_content(content, filename=input_name)
    adapter = get_adapter(adapter_name or detected_adapter_name)
    mapped_headers, unmapped_headers = analyze_header_mapping(detected_headers, adapter.name)
    products = list_products()
    product_by_id = {product.product_id: product for product in products}

    preview_items: list[ProductTrendImportPreviewItem] = []
    ready_items: list[dict[str, Any]] = []
    mapped_count = 0
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

            generated_trend_id = bool(normalized.pop("_generated_trend_id", False))
            auto_mapped = False
            mapped_product_title: Optional[str] = None

            if normalized.get("product_id"):
                mapped_product = product_by_id.get(normalized["product_id"])
                mapped_product_title = mapped_product.title if mapped_product else None
            else:
                match = find_product_match(products, normalized["keyword"], normalized["category"])
                if match:
                    normalized["product_id"] = match["product_id"]
                    mapped_product_title = match["title"]
                    auto_mapped = True

            validated = ProductTrend(**normalized)
            ready_items.append(validated.model_dump())
            ready_count += 1
            if generated_trend_id:
                generated_ids += 1
            if validated.product_id:
                mapped_count += 1

            preview_items.append(
                ProductTrendImportPreviewItem(
                    row_number=index,
                    status="ready",
                    trend_id=validated.trend_id,
                    source=validated.source,
                    keyword=validated.keyword,
                    category=validated.category,
                    trend_score=validated.trend_score,
                    sales_score=validated.sales_score,
                    product_id=validated.product_id,
                    mapped_product_title=mapped_product_title,
                    auto_mapped=auto_mapped,
                    generated_trend_id=generated_trend_id,
                )
            )
        except Exception as error:  # noqa: BLE001
            error_count += 1
            preview_items.append(
                ProductTrendImportPreviewItem(
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
        "mapped_count": mapped_count,
        "generated_trend_id_count": generated_ids,
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
            raise ValueError("Trend JSON payload must be a list of objects")
        headers = collect_json_headers(payload)
        return payload, "generic", headers

    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)
    detected_adapter = detect_adapter(reader.fieldnames or [])
    headers = [field.strip() for field in (reader.fieldnames or []) if field and field.strip()]
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
    adapter = get_adapter(adapter_name)
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
    adapter = get_adapter(adapter_name)
    transformed_row = adapter.row_transform(dict(row), index)
    normalized: dict[str, Any] = {}

    for key, value in transformed_row.items():
        canonical_key = adapter.column_aliases.get(str(key).strip().lower())
        if not canonical_key:
            continue
        normalized[canonical_key] = clean_value(value)

    keyword = str(normalized.get("keyword", "")).strip()
    category = str(normalized.get("category", "")).strip()
    if not keyword or not category:
        raise ValueError(f"Trend row {index} is missing keyword or category")

    source = str(normalized.get("source") or source_name).strip()
    normalized["source"] = source
    normalized["keyword"] = keyword
    normalized["category"] = category
    normalized["trend_score"] = normalize_score(normalized.get("trend_score", 0))
    normalized["sales_score"] = normalize_score(normalized.get("sales_score", 0))

    trend_id = str(normalized.get("trend_id") or "").strip()
    if not trend_id:
        normalized["trend_id"] = build_trend_id(source, keyword, category, index)
        normalized["_generated_trend_id"] = True
    else:
        normalized["trend_id"] = slugify(trend_id)

    product_id = str(normalized.get("product_id") or "").strip()
    normalized["product_id"] = product_id or None

    return normalized


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


def find_product_match(products: list[Product], keyword: str, category: str) -> Optional[dict[str, str]]:
    keyword_terms = split_terms(keyword)
    category_lower = category.lower()

    best_match: Optional[tuple[float, dict[str, str]]] = None
    for product in products:
        score = 0.0
        product_terms = {
            product.title.lower(),
            product.brand.lower(),
            product.category.lower(),
            *(feature.lower() for feature in product.features),
        }

        if product.category.lower() == category_lower:
            score += 1.5

        for term in keyword_terms:
            if any(term in product_term for product_term in product_terms):
                score += 1.0

        if keyword.lower() in product.title.lower():
            score += 2.0

        if score <= 0:
            continue

        candidate = {
            "product_id": product.product_id,
            "title": product.title,
        }
        if not best_match or score > best_match[0]:
            best_match = (score, candidate)

    if not best_match or best_match[0] < 1.5:
        return None

    return best_match[1]


def split_terms(text: str) -> list[str]:
    return [term for term in re.split(r"[\s,/|、\-]+", text.lower()) if term]


def build_trend_id(source: str, keyword: str, category: str, index: int) -> str:
    return slugify(f"{source}_{category}_{keyword}_{index}")


def slugify(value: str) -> str:
    slug = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "_", value.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "trend_item"
