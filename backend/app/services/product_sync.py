from __future__ import annotations

from pathlib import Path
from typing import Optional
import urllib.error
import urllib.request

from app.models import (
    ProductSyncRunAllResponse,
    ProductSyncRunResult,
    ProductSyncSource,
    ProductSyncSourceUpdate,
)
from app.services.database import (
    get_product_sync_source,
    insert_import_history,
    list_product_sync_sources,
    update_product_sync_source,
)
from app.services.product_import import import_products_from_content


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def run_product_sync_source(source_id: str) -> ProductSyncRunResult:
    source = get_product_sync_source(source_id)
    if not source:
        raise ValueError("Product sync source not found")

    return _run_sync(source)


def run_all_product_sync_sources(enabled_only: bool = True) -> ProductSyncRunAllResponse:
    sources = list_product_sync_sources(enabled=True if enabled_only else None)
    results = [_run_sync(source) for source in sources]

    return ProductSyncRunAllResponse(
        total_sources=len(results),
        success_count=sum(1 for item in results if item.status == "success"),
        error_count=sum(1 for item in results if item.status == "error"),
        items=results,
    )


def _run_sync(source: ProductSyncSource) -> ProductSyncRunResult:
    try:
        content, filename = _load_source_content(source)
        result = import_products_from_content(
            content=content,
            filename=filename,
            adapter_name=source.adapter,
        )

        update_product_sync_source(
            source.source_id,
            ProductSyncSourceUpdate(
                last_status="success",
                last_message=(
                    f"已同步 {result['imported_count']} 个商品"
                    f"（适配器 {result['adapter']}）"
                ),
                last_synced_at=_current_timestamp(),
                last_imported_count=result["imported_count"],
            ),
        )
        insert_import_history(
            {
                "entity_type": "product",
                "operation": "import",
                "status": "success",
                "adapter": result["adapter"],
                "filename": filename,
                "total_count": result["total_count"],
                "ready_count": result["ready_count"],
                "error_count": result["error_count"],
                "imported_count": result["imported_count"],
                "generated_id_count": result["generated_product_id_count"],
                "message": f"auto_sync:{source.source_id}",
            }
        )

        return ProductSyncRunResult(
            source_id=source.source_id,
            name=source.name,
            status="success",
            source_type=source.source_type,
            location=source.location,
            adapter=result["adapter"],
            imported_count=result["imported_count"],
            total_count=result["total_count"],
            ready_count=result["ready_count"],
            error_count=result["error_count"],
            generated_product_id_count=result["generated_product_id_count"],
            message=f"已同步 {result['imported_count']} 个商品",
        )
    except Exception as error:  # noqa: BLE001
        update_product_sync_source(
            source.source_id,
            ProductSyncSourceUpdate(
                last_status="error",
                last_message=str(error),
                last_synced_at=_current_timestamp(),
                last_imported_count=0,
            ),
        )
        insert_import_history(
            {
                "entity_type": "product",
                "operation": "import",
                "status": "error",
                "adapter": source.adapter or "auto",
                "filename": source.location,
                "message": f"auto_sync:{source.source_id} · {error}",
            }
        )
        return ProductSyncRunResult(
            source_id=source.source_id,
            name=source.name,
            status="error",
            source_type=source.source_type,
            location=source.location,
            adapter=source.adapter,
            message=str(error),
        )


def _load_source_content(source: ProductSyncSource) -> tuple[str, str]:
    if source.source_type == "file":
        source_path = Path(source.location)
        if not source_path.is_absolute():
            source_path = PROJECT_ROOT / source.location
        if not source_path.exists():
            raise FileNotFoundError(f"同步文件不存在：{source.location}")
        return source_path.read_text(encoding="utf-8"), source_path.name

    if source.source_type == "url":
        request = urllib.request.Request(
            source.location,
            headers={
                "User-Agent": "CodexProductSync/1.0",
                "Accept": "text/csv,application/json,text/plain,*/*",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                content_type = response.headers.get("Content-Type", "")
                suffix = ".json" if "json" in content_type.lower() else ".csv"
                return response.read().decode("utf-8"), _filename_from_url(source.location, suffix)
        except urllib.error.URLError as error:
            raise RuntimeError(f"无法读取远程来源：{error}") from error

    raise ValueError(f"Unsupported source type: {source.source_type}")


def _filename_from_url(location: str, fallback_suffix: str) -> str:
    tail = location.rstrip("/").split("/")[-1]
    if not tail:
        return f"remote_source{fallback_suffix}"
    if "." not in tail:
        return f"{tail}{fallback_suffix}"
    return tail


def _current_timestamp() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
