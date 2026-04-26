import json
from uuid import uuid4
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.models import (
    DirectionCreate,
    DirectionProductLinkCreate,
    DirectionRecommendationRequest,
    DirectionRecommendationResponse,
    DirectionUpdate,
    ExplanationFeedbackCreate,
    ImportHistoryItem,
    ProductBatchImportRequest,
    ProductBatchImportResponse,
    ProductBatchPreviewResponse,
    ProductCreate,
    ProductSyncRunAllResponse,
    ProductSyncRunResult,
    ProductSyncSourceCreate,
    ProductSyncSourceUpdate,
    ProductTrendBatchImportRequest,
    ProductTrendBatchImportResponse,
    ProductTrendBatchPreviewResponse,
    ProductTrendCreate,
    ProductTrendUpdate,
    ProductUpdate,
    RecommendationResponse,
    UserEventCreate,
    UserProfileCreate,
    UserProfileUpdate,
)
from app.sample_data import DIRECTION_PRODUCT_LINKS, DIRECTIONS, PRODUCTS, PRODUCT_SYNC_SOURCES, USERS
from app.services.database import (
    build_analytics_summary,
    count_user_events,
    delete_product_trend,
    get_direction,
    get_product as get_product_from_db,
    get_product_sync_source,
    get_user_profile,
    init_db,
    insert_explanation_feedback,
    insert_import_history,
    insert_recommendation_logs,
    insert_user_event,
    list_import_history,
    list_product_trends,
    list_products as list_products_from_db,
    list_product_sync_sources,
    list_runtime_events,
    list_user_profiles,
    list_direction_product_links,
    list_directions,
    replace_direction_product_links,
    seed_catalog,
    seed_product_sync_sources,
    update_direction,
    update_product,
    update_product_sync_source,
    update_product_trend,
    update_user_profile,
    upsert_direction,
    upsert_product,
    upsert_product_sync_source,
    upsert_product_trend,
    upsert_user_profile,
)
from app.services.direction_recommendation import build_direction_products, recommend_directions
from app.services.itemcf import load_seed_events
from app.services.llm_explanation import get_llm_status
from app.services.product_import import (
    import_products_from_content,
    list_product_adapter_info,
    preview_products_from_content,
)
from app.services.product_sync import run_all_product_sync_sources, run_product_sync_source
from app.services.recommendation import recommend_products
from app.services.trend_import import (
    import_product_trends_from_content,
    list_adapter_info,
    preview_product_trends_from_content,
)

app = FastAPI(
    title="E-commerce Recommendation + AI Explanation API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SEED_EVENT_LOGS = load_seed_events()
init_db()
seed_catalog(USERS, PRODUCTS, DIRECTIONS, DIRECTION_PRODUCT_LINKS)
seed_product_sync_sources(PRODUCT_SYNC_SOURCES)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/llm/status")
def llm_status():
    return get_llm_status()


@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    user = get_user_profile(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/api/users")
def list_users():
    return {"items": list_user_profiles()}


@app.post("/api/users")
def create_or_replace_user(user: UserProfileCreate):
    return upsert_user_profile(user)


@app.patch("/api/users/{user_id}")
def patch_user(user_id: str, update: UserProfileUpdate):
    user = update_user_profile(user_id, update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/api/directions")
def get_directions():
    return {"items": list_directions()}


@app.post("/api/directions")
def create_or_replace_direction(direction: DirectionCreate):
    return upsert_direction(direction)


@app.get("/api/directions/{direction_id}")
def get_direction_detail(direction_id: str):
    direction = get_direction(direction_id)
    if not direction:
        raise HTTPException(status_code=404, detail="Direction not found")
    return direction


@app.patch("/api/directions/{direction_id}")
def patch_direction(direction_id: str, update: DirectionUpdate):
    direction = update_direction(direction_id, update)
    if not direction:
        raise HTTPException(status_code=404, detail="Direction not found")
    return direction


@app.get("/api/directions/{direction_id}/products")
def get_direction_products(direction_id: str):
    if not get_direction(direction_id):
        raise HTTPException(status_code=404, detail="Direction not found")
    return {"items": list_direction_product_links(direction_id)}


@app.put("/api/directions/{direction_id}/products")
def replace_direction_products(direction_id: str, links: list[DirectionProductLinkCreate]):
    if not get_direction(direction_id):
        raise HTTPException(status_code=404, detail="Direction not found")

    normalized_links = [
        DirectionProductLinkCreate(
            direction_id=direction_id,
            product_id=link.product_id,
            product_role=link.product_role,
            priority=link.priority,
        )
        for link in links
    ]
    return {"items": replace_direction_product_links(direction_id, normalized_links)}


@app.get("/api/products")
def list_products(
    source: Optional[str] = None,
    category: Optional[str] = None,
):
    return {"items": list_products_from_db(source=source, category=category)}


@app.get("/api/product-source-adapters")
def get_product_source_adapters():
    return {"items": list_product_adapter_info()}


@app.get("/api/product-sync-sources")
def get_product_sync_sources(enabled: Optional[bool] = None):
    return {"items": list_product_sync_sources(enabled=enabled)}


@app.post("/api/product-sync-sources")
def create_or_replace_product_sync_source(source: ProductSyncSourceCreate):
    return upsert_product_sync_source(source)


@app.patch("/api/product-sync-sources/{source_id}")
def patch_product_sync_source(source_id: str, update: ProductSyncSourceUpdate):
    source = update_product_sync_source(source_id, update)
    if not source:
        raise HTTPException(status_code=404, detail="Product sync source not found")
    return source


@app.post("/api/product-sync-sources/{source_id}/run", response_model=ProductSyncRunResult)
def run_single_product_sync(source_id: str):
    if not get_product_sync_source(source_id):
        raise HTTPException(status_code=404, detail="Product sync source not found")
    return run_product_sync_source(source_id)


@app.post("/api/product-sync-sources/run-all", response_model=ProductSyncRunAllResponse)
def run_all_product_sync(enabled_only: bool = Query(default=True)):
    return run_all_product_sync_sources(enabled_only=enabled_only)


@app.get("/api/product-trends")
def get_product_trends(
    product_id: Optional[str] = None,
    category: Optional[str] = None,
    source: Optional[str] = None,
):
    return {"items": list_product_trends(product_id=product_id, category=category, source=source)}


@app.get("/api/product-trend-adapters")
def get_product_trend_adapters():
    return {"items": list_adapter_info()}


@app.get("/api/import-history")
def get_import_history(
    entity_type: Optional[str] = None,
    operation: Optional[str] = None,
    limit: int = Query(default=30, ge=1, le=100),
):
    return {"items": list_import_history(entity_type=entity_type, operation=operation, limit=limit)}


@app.post("/api/product-trends")
def create_or_replace_product_trend(product_trend: ProductTrendCreate):
    return upsert_product_trend(product_trend)


@app.post("/api/product-trends/batch-import", response_model=ProductTrendBatchImportResponse)
def batch_import_product_trends(request: ProductTrendBatchImportRequest):
    try:
        result = import_product_trends_from_content(
            content=request.content,
            filename=request.filename,
            adapter_name=request.adapter,
        )
    except (ValueError, json.JSONDecodeError) as error:
        insert_import_history(
            {
                "entity_type": "trend",
                "operation": "import",
                "status": "error",
                "adapter": request.adapter or "auto",
                "filename": request.filename,
                "message": str(error),
            }
        )
        raise HTTPException(status_code=400, detail=str(error)) from error

    insert_import_history(
        {
            "entity_type": "trend",
            "operation": "import",
            "status": "success",
            "adapter": result["adapter"],
            "filename": request.filename,
            "total_count": result["total_count"],
            "ready_count": result["ready_count"],
            "error_count": result["error_count"],
            "imported_count": result["imported_count"],
            "mapped_count": result["mapped_count"],
            "generated_id_count": result["generated_trend_id_count"],
        }
    )

    return ProductTrendBatchImportResponse(**result)


@app.post("/api/product-trends/batch-preview", response_model=ProductTrendBatchPreviewResponse)
def batch_preview_product_trends(request: ProductTrendBatchImportRequest):
    try:
        result = preview_product_trends_from_content(
            content=request.content,
            filename=request.filename,
            adapter_name=request.adapter,
        )
    except (ValueError, json.JSONDecodeError) as error:
        insert_import_history(
            {
                "entity_type": "trend",
                "operation": "preview",
                "status": "error",
                "adapter": request.adapter or "auto",
                "filename": request.filename,
                "message": str(error),
            }
        )
        raise HTTPException(status_code=400, detail=str(error)) from error

    insert_import_history(
        {
            "entity_type": "trend",
            "operation": "preview",
            "status": "success",
            "adapter": result["adapter"],
            "filename": request.filename,
            "total_count": result["total_count"],
            "ready_count": result["ready_count"],
            "error_count": result["error_count"],
            "mapped_count": result["mapped_count"],
            "generated_id_count": result["generated_trend_id_count"],
        }
    )

    return ProductTrendBatchPreviewResponse(**result)


@app.patch("/api/product-trends/{trend_id}")
def patch_product_trend(trend_id: str, update: ProductTrendUpdate):
    trend = update_product_trend(
        trend_id,
        update.model_dump(exclude_unset=True),
    )
    if not trend:
        raise HTTPException(status_code=404, detail="Product trend not found")
    return trend


@app.delete("/api/product-trends/{trend_id}")
def remove_product_trend(trend_id: str):
    deleted = delete_product_trend(trend_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product trend not found")
    return {"deleted": True, "trend_id": trend_id}


@app.post("/api/products")
def create_or_replace_product(product: ProductCreate):
    return upsert_product(product)


@app.post("/api/products/batch-import", response_model=ProductBatchImportResponse)
def batch_import_products(request: ProductBatchImportRequest):
    try:
        result = import_products_from_content(
            content=request.content,
            filename=request.filename,
            adapter_name=request.adapter,
        )
    except (ValueError, json.JSONDecodeError) as error:
        insert_import_history(
            {
                "entity_type": "product",
                "operation": "import",
                "status": "error",
                "adapter": request.adapter or "auto",
                "filename": request.filename,
                "message": str(error),
            }
        )
        raise HTTPException(status_code=400, detail=str(error)) from error

    insert_import_history(
        {
            "entity_type": "product",
            "operation": "import",
            "status": "success",
            "adapter": result["adapter"],
            "filename": request.filename,
            "total_count": result["total_count"],
            "ready_count": result["ready_count"],
            "error_count": result["error_count"],
            "imported_count": result["imported_count"],
            "generated_id_count": result["generated_product_id_count"],
        }
    )

    return ProductBatchImportResponse(**result)


@app.post("/api/products/batch-preview", response_model=ProductBatchPreviewResponse)
def batch_preview_products(request: ProductBatchImportRequest):
    try:
        result = preview_products_from_content(
            content=request.content,
            filename=request.filename,
            adapter_name=request.adapter,
        )
    except (ValueError, json.JSONDecodeError) as error:
        insert_import_history(
            {
                "entity_type": "product",
                "operation": "preview",
                "status": "error",
                "adapter": request.adapter or "auto",
                "filename": request.filename,
                "message": str(error),
            }
        )
        raise HTTPException(status_code=400, detail=str(error)) from error

    insert_import_history(
        {
            "entity_type": "product",
            "operation": "preview",
            "status": "success",
            "adapter": result["adapter"],
            "filename": request.filename,
            "total_count": result["total_count"],
            "ready_count": result["ready_count"],
            "error_count": result["error_count"],
            "generated_id_count": result["generated_product_id_count"],
        }
    )

    return ProductBatchPreviewResponse(**result)


@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    product = get_product_from_db(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.patch("/api/products/{product_id}")
def patch_product(product_id: str, update: ProductUpdate):
    product = update_product(product_id, update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/api/direction-recommendations", response_model=DirectionRecommendationResponse)
def get_direction_recommendations(request: DirectionRecommendationRequest):
    user = get_user_profile(request.user_id) if request.user_id else None
    if request.user_id and not user:
        raise HTTPException(status_code=404, detail="User not found")

    directions = list_directions()
    products = list_products_from_db()
    direction_products = build_direction_products(products, list_direction_product_links())
    items = recommend_directions(directions, direction_products, request, user)
    return DirectionRecommendationResponse(user_id=request.user_id, items=items)


@app.get("/api/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    user_id: str,
    scene: str = "home",
    direction_id: Optional[str] = None,
    limit: int = Query(default=5, ge=1, le=20),
):
    user = get_user_profile(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    events = [*SEED_EVENT_LOGS, *list_runtime_events()]
    products = list_products_from_db()
    product_trends = list_product_trends()
    direction_links: list[dict] = []
    if direction_id:
        direction = get_direction(direction_id)
        if not direction:
            raise HTTPException(status_code=404, detail="Direction not found")

        direction_links = list_direction_product_links(direction_id)
        allowed_product_ids = {
            link["product_id"]
            for link in direction_links
        }
        products = [
            product
            for product in products
            if product.product_id in allowed_product_ids
        ]

    items = recommend_products(
        user=user,
        products=products,
        limit=limit,
        events=events,
        product_trends=product_trends,
        direction_links=direction_links,
    )
    request_id = f"req_{uuid4().hex[:12]}"

    recommendation_logs = []
    for rank, item in enumerate(items, start=1):
        recommendation_logs.append(
            {
                "request_id": request_id,
                "user_id": user_id,
                "product_id": item.product_id,
                "rank": rank,
                "score": item.score,
                "scene": scene,
                "recommendation_source": item.recommendation_source,
                "reason_tags": item.reason_tags,
                "explanation": item.explanation,
                "explanation_provider": item.explanation_provider,
            }
        )
    insert_recommendation_logs(recommendation_logs)

    return RecommendationResponse(
        request_id=request_id,
        user_id=user_id,
        scene=scene,
        direction_id=direction_id,
        items=items,
    )


@app.post("/api/events")
def create_event(event: UserEventCreate):
    event_count = insert_user_event(event)
    return {"status": "accepted", "event_count": event_count}


@app.get("/api/events/summary")
def get_event_summary():
    runtime_event_count = count_user_events()
    return {
        "seed_event_count": len(SEED_EVENT_LOGS),
        "runtime_event_count": runtime_event_count,
        "total_event_count": len(SEED_EVENT_LOGS) + runtime_event_count,
    }


@app.post("/api/explanation-feedback")
def create_explanation_feedback(feedback: ExplanationFeedbackCreate):
    feedback_count = insert_explanation_feedback(feedback)
    return {"status": "accepted", "feedback_count": feedback_count}


@app.get("/api/analytics/summary")
def get_analytics_summary():
    return build_analytics_summary(list_products_from_db(), len(SEED_EVENT_LOGS))
