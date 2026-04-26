from typing import Literal, Optional

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    user_id: str
    username: str
    long_term_interests: list[str] = Field(default_factory=list)
    recent_interests: list[str] = Field(default_factory=list)
    brand_preference: list[str] = Field(default_factory=list)
    price_min: float
    price_max: float
    negative_tags: list[str] = Field(default_factory=list)


class Product(BaseModel):
    product_id: str
    title: str
    category: str
    brand: str
    price: float
    description: str
    features: list[str] = Field(default_factory=list)
    image_url: str
    stock: int
    rating: float
    source: str = "manual"
    external_id: Optional[str] = None
    popularity_score: float = Field(default=0, ge=0)
    sales_score: float = Field(default=0, ge=0)


class UserProfileCreate(UserProfile):
    pass


class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    long_term_interests: Optional[list[str]] = None
    recent_interests: Optional[list[str]] = None
    brand_preference: Optional[list[str]] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    negative_tags: Optional[list[str]] = None


class ProductCreate(Product):
    pass


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    features: Optional[list[str]] = None
    image_url: Optional[str] = None
    stock: Optional[int] = None
    rating: Optional[float] = None
    source: Optional[str] = None
    external_id: Optional[str] = None
    popularity_score: Optional[float] = Field(default=None, ge=0)
    sales_score: Optional[float] = Field(default=None, ge=0)


class ProductSourceAdapterInfo(BaseModel):
    name: str
    description: str
    header_signatures: list[str] = Field(default_factory=list)
    field_mappings: list[dict[str, str]] = Field(default_factory=list)


class ProductBatchImportRequest(BaseModel):
    content: str
    filename: Optional[str] = None
    adapter: Optional[str] = None


class ProductImportPreviewItem(BaseModel):
    row_number: int
    status: Literal["ready", "error"]
    product_id: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    source: Optional[str] = None
    external_id: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    rating: Optional[float] = None
    popularity_score: Optional[float] = None
    sales_score: Optional[float] = None
    generated_product_id: bool = False
    error: Optional[str] = None


class ProductBatchPreviewResponse(BaseModel):
    adapter: str
    adapter_description: Optional[str] = None
    total_count: int
    ready_count: int
    error_count: int
    generated_product_id_count: int
    detected_headers: list[str] = Field(default_factory=list)
    mapped_headers: list[dict[str, str]] = Field(default_factory=list)
    unmapped_headers: list[str] = Field(default_factory=list)
    items: list[ProductImportPreviewItem] = Field(default_factory=list)


class ProductBatchImportResponse(BaseModel):
    adapter: str
    total_count: int = 0
    ready_count: int = 0
    error_count: int = 0
    imported_count: int
    generated_product_id_count: int
    items: list[Product] = Field(default_factory=list)


class ProductSyncSource(BaseModel):
    source_id: str
    name: str
    source_type: Literal["file", "url"]
    location: str
    adapter: Optional[str] = None
    enabled: bool = True
    notes: Optional[str] = None
    last_status: Optional[Literal["success", "error"]] = None
    last_message: Optional[str] = None
    last_synced_at: Optional[str] = None
    last_imported_count: int = 0


class ProductSyncSourceCreate(ProductSyncSource):
    pass


class ProductSyncSourceUpdate(BaseModel):
    name: Optional[str] = None
    source_type: Optional[Literal["file", "url"]] = None
    location: Optional[str] = None
    adapter: Optional[str] = None
    enabled: Optional[bool] = None
    notes: Optional[str] = None
    last_status: Optional[Literal["success", "error"]] = None
    last_message: Optional[str] = None
    last_synced_at: Optional[str] = None
    last_imported_count: Optional[int] = None


class ProductSyncRunResult(BaseModel):
    source_id: str
    name: str
    status: Literal["success", "error"]
    source_type: Literal["file", "url"]
    location: str
    adapter: Optional[str] = None
    imported_count: int = 0
    total_count: int = 0
    ready_count: int = 0
    error_count: int = 0
    generated_product_id_count: int = 0
    message: Optional[str] = None


class ProductSyncRunAllResponse(BaseModel):
    total_sources: int
    success_count: int
    error_count: int
    items: list[ProductSyncRunResult] = Field(default_factory=list)


class ProductTrend(BaseModel):
    trend_id: str
    product_id: Optional[str] = None
    source: str
    keyword: str
    category: str
    trend_score: float = Field(ge=0)
    sales_score: float = Field(default=0, ge=0)


class ProductTrendCreate(ProductTrend):
    pass


class ProductTrendUpdate(BaseModel):
    product_id: Optional[str] = None
    source: Optional[str] = None
    keyword: Optional[str] = None
    category: Optional[str] = None
    trend_score: Optional[float] = Field(default=None, ge=0)
    sales_score: Optional[float] = Field(default=None, ge=0)


class ProductTrendAdapterInfo(BaseModel):
    name: str
    description: str
    header_signatures: list[str] = Field(default_factory=list)
    field_mappings: list[dict[str, str]] = Field(default_factory=list)


class ProductTrendBatchImportRequest(BaseModel):
    content: str
    filename: Optional[str] = None
    adapter: Optional[str] = None


class ProductTrendImportPreviewItem(BaseModel):
    row_number: int
    status: Literal["ready", "error"]
    trend_id: Optional[str] = None
    source: Optional[str] = None
    keyword: Optional[str] = None
    category: Optional[str] = None
    trend_score: Optional[float] = None
    sales_score: Optional[float] = None
    product_id: Optional[str] = None
    mapped_product_title: Optional[str] = None
    auto_mapped: bool = False
    generated_trend_id: bool = False
    error: Optional[str] = None


class ProductTrendBatchPreviewResponse(BaseModel):
    adapter: str
    adapter_description: Optional[str] = None
    total_count: int
    ready_count: int
    error_count: int
    mapped_count: int
    generated_trend_id_count: int
    detected_headers: list[str] = Field(default_factory=list)
    mapped_headers: list[dict[str, str]] = Field(default_factory=list)
    unmapped_headers: list[str] = Field(default_factory=list)
    items: list[ProductTrendImportPreviewItem] = Field(default_factory=list)


class ProductTrendBatchImportResponse(BaseModel):
    adapter: str
    total_count: int = 0
    ready_count: int = 0
    error_count: int = 0
    imported_count: int
    mapped_count: int
    generated_trend_id_count: int
    items: list[ProductTrend] = Field(default_factory=list)


class ImportHistoryItem(BaseModel):
    log_id: str
    entity_type: Literal["product", "trend"]
    operation: Literal["preview", "import"]
    status: Literal["success", "error"]
    adapter: Optional[str] = None
    filename: Optional[str] = None
    total_count: int = 0
    ready_count: int = 0
    error_count: int = 0
    imported_count: int = 0
    mapped_count: int = 0
    generated_id_count: int = 0
    message: Optional[str] = None
    created_at: Optional[str] = None


class Direction(BaseModel):
    direction_id: str
    title: str
    category: str
    description: str
    target_scene: str
    budget_min: float
    budget_max: float
    difficulty_level: str
    target_interests: list[str] = Field(default_factory=list)


class DirectionCreate(Direction):
    pass


class DirectionUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    target_scene: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    difficulty_level: Optional[str] = None
    target_interests: Optional[list[str]] = None


class DirectionProductLink(BaseModel):
    direction_id: str
    product_id: str
    product_role: str
    priority: int


class DirectionProductLinkCreate(DirectionProductLink):
    pass


class DirectionStarterProduct(BaseModel):
    product_id: str
    title: str
    category: str
    brand: str
    price: float
    product_role: str
    priority: int


class DirectionRecommendationRequest(BaseModel):
    user_id: Optional[str] = None
    interests: list[str] = Field(default_factory=list)
    preferred_categories: list[str] = Field(default_factory=list)
    existing_resources: list[str] = Field(default_factory=list)
    budget: Optional[float] = None
    limit: int = Field(default=3, ge=1, le=10)


class DirectionRecommendationItem(BaseModel):
    direction_id: str
    title: str
    category: str
    description: str
    target_scene: str
    difficulty_level: str
    budget_min: float
    budget_max: float
    score: float
    reasons: list[str]
    starter_products: list[DirectionStarterProduct] = Field(default_factory=list)


class DirectionRecommendationResponse(BaseModel):
    user_id: Optional[str] = None
    items: list[DirectionRecommendationItem]


class RecommendationItem(BaseModel):
    product_id: str
    title: str
    category: str
    brand: str
    price: float
    image_url: str
    score: float
    trend_score: float = 0
    recommendation_source: str
    direction_product_role: Optional[str] = None
    reason_tags: list[str]
    explanation: str
    explanation_provider: str


class RecommendationResponse(BaseModel):
    request_id: str
    user_id: str
    scene: str
    direction_id: Optional[str] = None
    items: list[RecommendationItem]


class UserEventCreate(BaseModel):
    user_id: str
    product_id: str
    event_type: Literal["view", "click", "favorite", "add_to_cart", "purchase", "dislike"]
    scene: str = "home"
    request_id: Optional[str] = None


class ExplanationFeedbackCreate(BaseModel):
    user_id: str
    product_id: str
    explanation_id: Optional[str] = None
    feedback_type: Literal["helpful", "not_helpful", "too_personal", "inaccurate"]
