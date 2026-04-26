import json
import sqlite3
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from app.models import (
    Direction,
    DirectionProductLink,
    DirectionUpdate,
    ExplanationFeedbackCreate,
    ImportHistoryItem,
    Product,
    ProductSyncSource,
    ProductSyncSourceUpdate,
    ProductTrend,
    ProductUpdate,
    UserEventCreate,
    UserProfile,
    UserProfileUpdate,
)


DB_PATH = Path(__file__).resolve().parents[3] / "data" / "app.sqlite3"


def init_db() -> None:
    DB_PATH.parent.mkdir(exist_ok=True)

    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS user_events (
              event_id TEXT PRIMARY KEY,
              user_id TEXT NOT NULL,
              product_id TEXT NOT NULL,
              event_type TEXT NOT NULL,
              scene TEXT NOT NULL,
              request_id TEXT,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS users (
              user_id TEXT PRIMARY KEY,
              username TEXT NOT NULL,
              long_term_interests TEXT NOT NULL,
              recent_interests TEXT NOT NULL,
              brand_preference TEXT NOT NULL,
              price_min REAL NOT NULL,
              price_max REAL NOT NULL,
              negative_tags TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
              updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS products (
              product_id TEXT PRIMARY KEY,
              title TEXT NOT NULL,
              category TEXT NOT NULL,
              brand TEXT NOT NULL,
              price REAL NOT NULL,
              description TEXT NOT NULL,
              features TEXT NOT NULL,
              image_url TEXT NOT NULL,
              stock INTEGER NOT NULL,
              rating REAL NOT NULL,
              source TEXT NOT NULL DEFAULT 'manual',
              external_id TEXT,
              popularity_score REAL NOT NULL DEFAULT 0,
              sales_score REAL NOT NULL DEFAULT 0,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
              updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS product_trends (
              trend_id TEXT PRIMARY KEY,
              product_id TEXT,
              source TEXT NOT NULL,
              keyword TEXT NOT NULL,
              category TEXT NOT NULL,
              trend_score REAL NOT NULL,
              sales_score REAL NOT NULL DEFAULT 0,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
              updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS product_sync_sources (
              source_id TEXT PRIMARY KEY,
              name TEXT NOT NULL,
              source_type TEXT NOT NULL,
              location TEXT NOT NULL,
              adapter TEXT,
              enabled INTEGER NOT NULL DEFAULT 1,
              notes TEXT,
              last_status TEXT,
              last_message TEXT,
              last_synced_at TEXT,
              last_imported_count INTEGER NOT NULL DEFAULT 0,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
              updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS directions (
              direction_id TEXT PRIMARY KEY,
              title TEXT NOT NULL,
              category TEXT NOT NULL,
              description TEXT NOT NULL,
              target_scene TEXT NOT NULL,
              budget_min REAL NOT NULL,
              budget_max REAL NOT NULL,
              difficulty_level TEXT NOT NULL,
              target_interests TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
              updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS direction_products (
              direction_id TEXT NOT NULL,
              product_id TEXT NOT NULL,
              product_role TEXT NOT NULL,
              priority INTEGER NOT NULL,
              PRIMARY KEY (direction_id, product_id)
            );

            CREATE TABLE IF NOT EXISTS recommendation_logs (
              log_id TEXT PRIMARY KEY,
              request_id TEXT NOT NULL,
              user_id TEXT NOT NULL,
              product_id TEXT NOT NULL,
              rank_position INTEGER NOT NULL,
              score REAL NOT NULL,
              scene TEXT NOT NULL,
              recommendation_source TEXT NOT NULL,
              reason_tags TEXT NOT NULL,
              explanation TEXT NOT NULL,
              explanation_provider TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS explanation_feedback (
              feedback_id TEXT PRIMARY KEY,
              user_id TEXT NOT NULL,
              product_id TEXT NOT NULL,
              explanation_id TEXT,
              feedback_type TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS import_history (
              log_id TEXT PRIMARY KEY,
              entity_type TEXT NOT NULL,
              operation TEXT NOT NULL,
              status TEXT NOT NULL,
              adapter TEXT,
              filename TEXT,
              total_count INTEGER NOT NULL DEFAULT 0,
              ready_count INTEGER NOT NULL DEFAULT 0,
              error_count INTEGER NOT NULL DEFAULT 0,
              imported_count INTEGER NOT NULL DEFAULT 0,
              mapped_count INTEGER NOT NULL DEFAULT 0,
              generated_id_count INTEGER NOT NULL DEFAULT 0,
              message TEXT,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_user_events_user_id ON user_events(user_id);
            CREATE INDEX IF NOT EXISTS idx_user_events_request_id ON user_events(request_id);
            CREATE INDEX IF NOT EXISTS idx_recommendation_logs_request_id ON recommendation_logs(request_id);
            CREATE INDEX IF NOT EXISTS idx_recommendation_logs_product_id ON recommendation_logs(product_id);
            CREATE INDEX IF NOT EXISTS idx_explanation_feedback_explanation_id ON explanation_feedback(explanation_id);
            CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
            CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
            CREATE INDEX IF NOT EXISTS idx_product_trends_product_id ON product_trends(product_id);
            CREATE INDEX IF NOT EXISTS idx_product_trends_category ON product_trends(category);
            CREATE INDEX IF NOT EXISTS idx_product_sync_sources_enabled ON product_sync_sources(enabled);
            CREATE INDEX IF NOT EXISTS idx_directions_category ON directions(category);
            CREATE INDEX IF NOT EXISTS idx_direction_products_direction_id ON direction_products(direction_id);
            CREATE INDEX IF NOT EXISTS idx_import_history_entity_type ON import_history(entity_type);
            CREATE INDEX IF NOT EXISTS idx_import_history_operation ON import_history(operation);
            """
        )
        _ensure_column(connection, "products", "source", "TEXT NOT NULL DEFAULT 'manual'")
        _ensure_column(connection, "products", "external_id", "TEXT")
        _ensure_column(connection, "products", "popularity_score", "REAL NOT NULL DEFAULT 0")
        _ensure_column(connection, "products", "sales_score", "REAL NOT NULL DEFAULT 0")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_products_source ON products(source)")


def seed_catalog(
    users: dict[str, UserProfile],
    products: list[Product],
    directions: list[Direction],
    direction_product_links: list[DirectionProductLink],
) -> None:
    with _connect() as connection:
        if _count_rows(connection, "users") == 0:
            connection.executemany(
                """
                INSERT INTO users (
                  user_id,
                  username,
                  long_term_interests,
                  recent_interests,
                  brand_preference,
                  price_min,
                  price_max,
                  negative_tags
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        user.user_id,
                        user.username,
                        _to_json(user.long_term_interests),
                        _to_json(user.recent_interests),
                        _to_json(user.brand_preference),
                        user.price_min,
                        user.price_max,
                        _to_json(user.negative_tags),
                    )
                    for user in users.values()
                ],
            )

        if _count_rows(connection, "products") == 0:
            connection.executemany(
                """
                INSERT INTO products (
                  product_id,
                  title,
                  category,
                  brand,
                  price,
                  description,
                  features,
                  image_url,
                  stock,
                  rating,
                  source,
                  external_id,
                  popularity_score,
                  sales_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        product.product_id,
                        product.title,
                        product.category,
                        product.brand,
                        product.price,
                        product.description,
                        _to_json(product.features),
                        product.image_url,
                        product.stock,
                        product.rating,
                        product.source,
                        product.external_id,
                        product.popularity_score,
                        product.sales_score,
                    )
                    for product in products
                ],
            )

        if _count_rows(connection, "directions") == 0:
            connection.executemany(
                """
                INSERT INTO directions (
                  direction_id,
                  title,
                  category,
                  description,
                  target_scene,
                  budget_min,
                  budget_max,
                  difficulty_level,
                  target_interests
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        direction.direction_id,
                        direction.title,
                        direction.category,
                        direction.description,
                        direction.target_scene,
                        direction.budget_min,
                        direction.budget_max,
                        direction.difficulty_level,
                        _to_json(direction.target_interests),
                    )
                    for direction in directions
                ],
            )

        if _count_rows(connection, "direction_products") == 0:
            connection.executemany(
                """
                INSERT INTO direction_products (
                  direction_id,
                  product_id,
                  product_role,
                  priority
                )
                VALUES (?, ?, ?, ?)
                """,
                [
                    (
                        link.direction_id,
                        link.product_id,
                        link.product_role,
                        link.priority,
                    )
                    for link in direction_product_links
                ],
            )


def seed_product_sync_sources(sources: list[ProductSyncSource]) -> None:
    with _connect() as connection:
        if _count_rows(connection, "product_sync_sources") != 0:
            return

        connection.executemany(
            """
            INSERT INTO product_sync_sources (
              source_id,
              name,
              source_type,
              location,
              adapter,
              enabled,
              notes,
              last_status,
              last_message,
              last_synced_at,
              last_imported_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    source.source_id,
                    source.name,
                    source.source_type,
                    source.location,
                    source.adapter,
                    1 if source.enabled else 0,
                    source.notes,
                    source.last_status,
                    source.last_message,
                    source.last_synced_at,
                    source.last_imported_count,
                )
                for source in sources
            ],
        )


def get_user_profile(user_id: str) -> Optional[UserProfile]:
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT user_id, username, long_term_interests, recent_interests,
                   brand_preference, price_min, price_max, negative_tags
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

    if not row:
        return None

    return _row_to_user(row)


def list_directions() -> list[Direction]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT direction_id, title, category, description, target_scene,
                   budget_min, budget_max, difficulty_level, target_interests
            FROM directions
            ORDER BY direction_id ASC
            """
        ).fetchall()

    return [_row_to_direction(row) for row in rows]


def get_direction(direction_id: str) -> Optional[Direction]:
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT direction_id, title, category, description, target_scene,
                   budget_min, budget_max, difficulty_level, target_interests
            FROM directions
            WHERE direction_id = ?
            """,
            (direction_id,),
        ).fetchone()

    if not row:
        return None

    return _row_to_direction(row)


def upsert_direction(direction: Direction) -> Direction:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO directions (
              direction_id,
              title,
              category,
              description,
              target_scene,
              budget_min,
              budget_max,
              difficulty_level,
              target_interests
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(direction_id) DO UPDATE SET
              title = excluded.title,
              category = excluded.category,
              description = excluded.description,
              target_scene = excluded.target_scene,
              budget_min = excluded.budget_min,
              budget_max = excluded.budget_max,
              difficulty_level = excluded.difficulty_level,
              target_interests = excluded.target_interests,
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                direction.direction_id,
                direction.title,
                direction.category,
                direction.description,
                direction.target_scene,
                direction.budget_min,
                direction.budget_max,
                direction.difficulty_level,
                _to_json(direction.target_interests),
            ),
        )

    saved_direction = get_direction(direction.direction_id)
    if not saved_direction:
        raise RuntimeError("Failed to save direction")
    return saved_direction


def update_direction(direction_id: str, update: DirectionUpdate) -> Optional[Direction]:
    existing_direction = get_direction(direction_id)
    if not existing_direction:
        return None

    data = existing_direction.model_dump()
    patch = update.model_dump(exclude_unset=True)
    data.update(patch)
    return upsert_direction(Direction(**data))


def list_direction_product_links(direction_id: Optional[str] = None) -> list[dict[str, Any]]:
    query = """
        SELECT direction_id, product_id, product_role, priority
        FROM direction_products
    """
    parameters: tuple = ()
    if direction_id:
        query += " WHERE direction_id = ?"
        parameters = (direction_id,)
    query += " ORDER BY direction_id ASC, priority ASC"

    with _connect() as connection:
        rows = connection.execute(query, parameters).fetchall()

    return [dict(row) for row in rows]


def replace_direction_product_links(direction_id: str, links: list[DirectionProductLink]) -> list[dict[str, Any]]:
    with _connect() as connection:
        connection.execute(
            "DELETE FROM direction_products WHERE direction_id = ?",
            (direction_id,),
        )
        connection.executemany(
            """
            INSERT INTO direction_products (
              direction_id,
              product_id,
              product_role,
              priority
            )
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    link.direction_id,
                    link.product_id,
                    link.product_role,
                    link.priority,
                )
                for link in links
            ],
        )

    return list_direction_product_links(direction_id)


def upsert_user_profile(user: UserProfile) -> UserProfile:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO users (
              user_id,
              username,
              long_term_interests,
              recent_interests,
              brand_preference,
              price_min,
              price_max,
              negative_tags
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
              username = excluded.username,
              long_term_interests = excluded.long_term_interests,
              recent_interests = excluded.recent_interests,
              brand_preference = excluded.brand_preference,
              price_min = excluded.price_min,
              price_max = excluded.price_max,
              negative_tags = excluded.negative_tags,
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                user.user_id,
                user.username,
                _to_json(user.long_term_interests),
                _to_json(user.recent_interests),
                _to_json(user.brand_preference),
                user.price_min,
                user.price_max,
                _to_json(user.negative_tags),
            ),
        )

    saved_user = get_user_profile(user.user_id)
    if not saved_user:
        raise RuntimeError("Failed to save user profile")
    return saved_user


def update_user_profile(user_id: str, update: UserProfileUpdate) -> Optional[UserProfile]:
    existing_user = get_user_profile(user_id)
    if not existing_user:
        return None

    data = existing_user.model_dump()
    patch = update.model_dump(exclude_unset=True)
    data.update(patch)
    return upsert_user_profile(UserProfile(**data))


def list_user_profiles() -> list[UserProfile]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT user_id, username, long_term_interests, recent_interests,
                   brand_preference, price_min, price_max, negative_tags
            FROM users
            ORDER BY user_id ASC
            """
        ).fetchall()

    return [_row_to_user(row) for row in rows]


def get_product(product_id: str) -> Optional[Product]:
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT product_id, title, category, brand, price, description,
                   features, image_url, stock, rating, source, external_id,
                   popularity_score, sales_score
            FROM products
            WHERE product_id = ?
            """,
            (product_id,),
        ).fetchone()

    if not row:
        return None

    return _row_to_product(row)


def list_product_sync_sources(enabled: Optional[bool] = None) -> list[ProductSyncSource]:
    query = """
        SELECT source_id, name, source_type, location, adapter, enabled, notes,
               last_status, last_message, last_synced_at, last_imported_count
        FROM product_sync_sources
    """
    parameters: tuple[Any, ...] = ()
    if enabled is not None:
        query += " WHERE enabled = ?"
        parameters = (1 if enabled else 0,)
    query += " ORDER BY source_id ASC"

    with _connect() as connection:
        rows = connection.execute(query, parameters).fetchall()

    return [_row_to_product_sync_source(row) for row in rows]


def get_product_sync_source(source_id: str) -> Optional[ProductSyncSource]:
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT source_id, name, source_type, location, adapter, enabled, notes,
                   last_status, last_message, last_synced_at, last_imported_count
            FROM product_sync_sources
            WHERE source_id = ?
            """,
            (source_id,),
        ).fetchone()

    if not row:
        return None

    return _row_to_product_sync_source(row)


def upsert_product_sync_source(source: ProductSyncSource) -> ProductSyncSource:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO product_sync_sources (
              source_id,
              name,
              source_type,
              location,
              adapter,
              enabled,
              notes,
              last_status,
              last_message,
              last_synced_at,
              last_imported_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_id) DO UPDATE SET
              name = excluded.name,
              source_type = excluded.source_type,
              location = excluded.location,
              adapter = excluded.adapter,
              enabled = excluded.enabled,
              notes = excluded.notes,
              last_status = excluded.last_status,
              last_message = excluded.last_message,
              last_synced_at = excluded.last_synced_at,
              last_imported_count = excluded.last_imported_count,
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                source.source_id,
                source.name,
                source.source_type,
                source.location,
                source.adapter,
                1 if source.enabled else 0,
                source.notes,
                source.last_status,
                source.last_message,
                source.last_synced_at,
                source.last_imported_count,
            ),
        )

    saved_source = get_product_sync_source(source.source_id)
    if not saved_source:
        raise RuntimeError("Failed to save product sync source")
    return saved_source


def update_product_sync_source(source_id: str, update: ProductSyncSourceUpdate) -> Optional[ProductSyncSource]:
    existing_source = get_product_sync_source(source_id)
    if not existing_source:
        return None

    data = existing_source.model_dump()
    data.update(update.model_dump(exclude_unset=True))
    return upsert_product_sync_source(ProductSyncSource(**data))


def get_product_trend(trend_id: str) -> Optional[ProductTrend]:
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT trend_id, product_id, source, keyword, category, trend_score, sales_score
            FROM product_trends
            WHERE trend_id = ?
            """,
            (trend_id,),
        ).fetchone()

    if not row:
        return None

    return _row_to_product_trend(row)


def upsert_product_trend(product_trend: ProductTrend) -> ProductTrend:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO product_trends (
              trend_id,
              product_id,
              source,
              keyword,
              category,
              trend_score,
              sales_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(trend_id) DO UPDATE SET
              product_id = excluded.product_id,
              source = excluded.source,
              keyword = excluded.keyword,
              category = excluded.category,
              trend_score = excluded.trend_score,
              sales_score = excluded.sales_score,
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                product_trend.trend_id,
                product_trend.product_id,
                product_trend.source,
                product_trend.keyword,
                product_trend.category,
                product_trend.trend_score,
                product_trend.sales_score,
            ),
        )

    saved_trend = get_product_trend(product_trend.trend_id)
    if not saved_trend:
        raise RuntimeError("Failed to save product trend")
    return saved_trend


def update_product_trend(trend_id: str, update: dict[str, Any]) -> Optional[ProductTrend]:
    existing_trend = get_product_trend(trend_id)
    if not existing_trend:
        return None

    data = existing_trend.model_dump()
    data.update(update)
    return upsert_product_trend(ProductTrend(**data))


def delete_product_trend(trend_id: str) -> bool:
    with _connect() as connection:
        result = connection.execute(
            "DELETE FROM product_trends WHERE trend_id = ?",
            (trend_id,),
        )
    return result.rowcount > 0


def list_product_trends(
    product_id: Optional[str] = None,
    category: Optional[str] = None,
    source: Optional[str] = None,
) -> list[ProductTrend]:
    query = """
        SELECT trend_id, product_id, source, keyword, category, trend_score, sales_score
        FROM product_trends
    """
    clauses: list[str] = []
    parameters: list[Any] = []

    if product_id:
        clauses.append("product_id = ?")
        parameters.append(product_id)

    if category:
        clauses.append("category = ?")
        parameters.append(category)

    if source:
        clauses.append("source = ?")
        parameters.append(source)

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY trend_score DESC, sales_score DESC, trend_id ASC"

    with _connect() as connection:
        rows = connection.execute(query, tuple(parameters)).fetchall()

    return [_row_to_product_trend(row) for row in rows]


def upsert_product(product: Product) -> Product:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO products (
              product_id,
              title,
              category,
              brand,
              price,
              description,
              features,
              image_url,
              stock,
              rating,
              source,
              external_id,
              popularity_score,
              sales_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(product_id) DO UPDATE SET
              title = excluded.title,
              category = excluded.category,
              brand = excluded.brand,
              price = excluded.price,
              description = excluded.description,
              features = excluded.features,
              image_url = excluded.image_url,
              stock = excluded.stock,
              rating = excluded.rating,
              source = excluded.source,
              external_id = excluded.external_id,
              popularity_score = excluded.popularity_score,
              sales_score = excluded.sales_score,
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                product.product_id,
                product.title,
                product.category,
                product.brand,
                product.price,
                product.description,
                _to_json(product.features),
                product.image_url,
                product.stock,
                product.rating,
                product.source,
                product.external_id,
                product.popularity_score,
                product.sales_score,
            ),
        )

    saved_product = get_product(product.product_id)
    if not saved_product:
        raise RuntimeError("Failed to save product")
    return saved_product


def update_product(product_id: str, update: ProductUpdate) -> Optional[Product]:
    existing_product = get_product(product_id)
    if not existing_product:
        return None

    data = existing_product.model_dump()
    patch = update.model_dump(exclude_unset=True)
    data.update(patch)
    return upsert_product(Product(**data))


def list_products(
    source: Optional[str] = None,
    category: Optional[str] = None,
) -> list[Product]:
    query = """
        SELECT product_id, title, category, brand, price, description,
               features, image_url, stock, rating, source, external_id,
               popularity_score, sales_score
        FROM products
    """
    clauses: list[str] = []
    parameters: list[Any] = []

    if source:
        clauses.append("source = ?")
        parameters.append(source)

    if category:
        clauses.append("category = ?")
        parameters.append(category)

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY source ASC, product_id ASC"

    with _connect() as connection:
        rows = connection.execute(query, tuple(parameters)).fetchall()

    return [_row_to_product(row) for row in rows]


def insert_user_event(event: UserEventCreate) -> int:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO user_events (
              event_id,
              user_id,
              product_id,
              event_type,
              scene,
              request_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                f"evt_{uuid4().hex[:12]}",
                event.user_id,
                event.product_id,
                event.event_type,
                event.scene,
                event.request_id,
            ),
        )
        return _count_rows(connection, "user_events")


def list_runtime_events() -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT user_id, product_id, event_type, scene, request_id, created_at
            FROM user_events
            ORDER BY created_at ASC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def count_user_events() -> int:
    with _connect() as connection:
        return _count_rows(connection, "user_events")


def insert_import_history(record: dict[str, Any]) -> ImportHistoryItem:
    log_id = f"imp_{uuid4().hex[:12]}"
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO import_history (
              log_id,
              entity_type,
              operation,
              status,
              adapter,
              filename,
              total_count,
              ready_count,
              error_count,
              imported_count,
              mapped_count,
              generated_id_count,
              message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                log_id,
                record["entity_type"],
                record["operation"],
                record["status"],
                record.get("adapter"),
                record.get("filename"),
                int(record.get("total_count", 0)),
                int(record.get("ready_count", 0)),
                int(record.get("error_count", 0)),
                int(record.get("imported_count", 0)),
                int(record.get("mapped_count", 0)),
                int(record.get("generated_id_count", 0)),
                record.get("message"),
            ),
        )

    saved_item = get_import_history_item(log_id)
    if not saved_item:
        raise RuntimeError("Failed to save import history")
    return saved_item


def get_import_history_item(log_id: str) -> Optional[ImportHistoryItem]:
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT log_id, entity_type, operation, status, adapter, filename,
                   total_count, ready_count, error_count, imported_count,
                   mapped_count, generated_id_count, message, created_at
            FROM import_history
            WHERE log_id = ?
            """,
            (log_id,),
        ).fetchone()

    if not row:
        return None

    return _row_to_import_history(row)


def list_import_history(
    entity_type: Optional[str] = None,
    operation: Optional[str] = None,
    limit: int = 30,
) -> list[ImportHistoryItem]:
    query = """
        SELECT log_id, entity_type, operation, status, adapter, filename,
               total_count, ready_count, error_count, imported_count,
               mapped_count, generated_id_count, message, created_at
        FROM import_history
    """
    clauses: list[str] = []
    parameters: list[Any] = []

    if entity_type:
        clauses.append("entity_type = ?")
        parameters.append(entity_type)

    if operation:
        clauses.append("operation = ?")
        parameters.append(operation)

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY created_at DESC, log_id DESC LIMIT ?"
    parameters.append(limit)

    with _connect() as connection:
        rows = connection.execute(query, tuple(parameters)).fetchall()

    return [_row_to_import_history(row) for row in rows]


def insert_recommendation_logs(logs: list[dict[str, Any]]) -> None:
    with _connect() as connection:
        connection.executemany(
            """
            INSERT INTO recommendation_logs (
              log_id,
              request_id,
              user_id,
              product_id,
              rank_position,
              score,
              scene,
              recommendation_source,
              reason_tags,
              explanation,
              explanation_provider
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    f"rec_{uuid4().hex[:12]}",
                    log["request_id"],
                    log["user_id"],
                    log["product_id"],
                    log["rank"],
                    log["score"],
                    log["scene"],
                    log["recommendation_source"],
                    json.dumps(log["reason_tags"], ensure_ascii=False),
                    log["explanation"],
                    log["explanation_provider"],
                )
                for log in logs
            ],
        )


def insert_explanation_feedback(feedback: ExplanationFeedbackCreate) -> int:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO explanation_feedback (
              feedback_id,
              user_id,
              product_id,
              explanation_id,
              feedback_type
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                f"fb_{uuid4().hex[:12]}",
                feedback.user_id,
                feedback.product_id,
                feedback.explanation_id,
                feedback.feedback_type,
            ),
        )
        return _count_rows(connection, "explanation_feedback")


def build_analytics_summary(products: list[Product], seed_event_count: int) -> dict[str, Any]:
    product_by_id = {product.product_id: product for product in products}

    with _connect() as connection:
        event_counts = _count_group(connection, "user_events", "event_type")
        source_counts = _count_group(connection, "recommendation_logs", "recommendation_source")
        scene_counts = _count_group(connection, "recommendation_logs", "scene")
        feedback_counts = _count_group(connection, "explanation_feedback", "feedback_type")

        impression_count = _count_rows(connection, "recommendation_logs")
        recommendation_request_count = connection.execute(
            "SELECT COUNT(DISTINCT request_id) AS count FROM recommendation_logs"
        ).fetchone()["count"]
        feedback_count = _count_rows(connection, "explanation_feedback")
        runtime_event_count = _count_rows(connection, "user_events")
        top_products = _build_top_products(connection, product_by_id)

    click_count = event_counts.get("click", 0)
    add_to_cart_count = event_counts.get("add_to_cart", 0)
    helpful_count = feedback_counts.get("helpful", 0)

    return {
        "recommendation_request_count": recommendation_request_count,
        "impression_count": impression_count,
        "click_count": click_count,
        "view_count": event_counts.get("view", 0),
        "favorite_count": event_counts.get("favorite", 0),
        "add_to_cart_count": add_to_cart_count,
        "dislike_count": event_counts.get("dislike", 0),
        "ctr": _safe_rate(click_count, impression_count),
        "add_to_cart_rate": _safe_rate(add_to_cart_count, impression_count),
        "feedback_count": feedback_count,
        "helpful_feedback_count": helpful_count,
        "helpful_feedback_rate": _safe_rate(helpful_count, feedback_count),
        "recommendation_source_counts": source_counts,
        "scene_counts": scene_counts,
        "seed_event_count": seed_event_count,
        "runtime_event_count": runtime_event_count,
        "top_products": top_products,
    }


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _count_rows(connection: sqlite3.Connection, table_name: str) -> int:
    return connection.execute(f"SELECT COUNT(*) AS count FROM {table_name}").fetchone()["count"]


def _count_group(connection: sqlite3.Connection, table_name: str, column_name: str) -> dict[str, int]:
    rows = connection.execute(
        f"SELECT {column_name} AS name, COUNT(*) AS count FROM {table_name} GROUP BY {column_name}"
    ).fetchall()
    return {row["name"]: row["count"] for row in rows}


def _build_top_products(connection: sqlite3.Connection, product_by_id: dict[str, Product]) -> list[dict[str, Any]]:
    stats: dict[str, dict[str, int]] = {}

    impression_rows = connection.execute(
        """
        SELECT product_id, COUNT(*) AS impressions
        FROM recommendation_logs
        GROUP BY product_id
        """
    ).fetchall()
    for row in impression_rows:
        stats.setdefault(
            row["product_id"],
            {"impressions": 0, "clicks": 0, "add_to_cart": 0, "favorites": 0},
        )
        stats[row["product_id"]]["impressions"] = row["impressions"]

    event_rows = connection.execute(
        """
        SELECT product_id, event_type, COUNT(*) AS count
        FROM user_events
        WHERE event_type IN ('click', 'add_to_cart', 'favorite')
        GROUP BY product_id, event_type
        """
    ).fetchall()
    for row in event_rows:
        stats.setdefault(
            row["product_id"],
            {"impressions": 0, "clicks": 0, "add_to_cart": 0, "favorites": 0},
        )
        if row["event_type"] == "click":
            stats[row["product_id"]]["clicks"] = row["count"]
        elif row["event_type"] == "add_to_cart":
            stats[row["product_id"]]["add_to_cart"] = row["count"]
        elif row["event_type"] == "favorite":
            stats[row["product_id"]]["favorites"] = row["count"]

    top_products = []
    for product_id, product_stats in stats.items():
        product = product_by_id.get(product_id)
        if not product:
            continue

        top_products.append(
            {
                "product_id": product_id,
                "title": product.title,
                "impressions": product_stats["impressions"],
                "clicks": product_stats["clicks"],
                "add_to_cart": product_stats["add_to_cart"],
                "favorites": product_stats["favorites"],
                "ctr": _safe_rate(product_stats["clicks"], product_stats["impressions"]),
            }
        )

    return sorted(
        top_products,
        key=lambda item: (item["clicks"], item["add_to_cart"], item["impressions"]),
        reverse=True,
    )[:5]


def _safe_rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def _row_to_user(row: sqlite3.Row) -> UserProfile:
    return UserProfile(
        user_id=row["user_id"],
        username=row["username"],
        long_term_interests=_from_json(row["long_term_interests"]),
        recent_interests=_from_json(row["recent_interests"]),
        brand_preference=_from_json(row["brand_preference"]),
        price_min=row["price_min"],
        price_max=row["price_max"],
        negative_tags=_from_json(row["negative_tags"]),
    )


def _row_to_product(row: sqlite3.Row) -> Product:
    return Product(
        product_id=row["product_id"],
        title=row["title"],
        category=row["category"],
        brand=row["brand"],
        price=row["price"],
        description=row["description"],
        features=_from_json(row["features"]),
        image_url=row["image_url"],
        stock=row["stock"],
        rating=row["rating"],
        source=row["source"],
        external_id=row["external_id"],
        popularity_score=row["popularity_score"],
        sales_score=row["sales_score"],
    )


def _row_to_product_sync_source(row: sqlite3.Row) -> ProductSyncSource:
    return ProductSyncSource(
        source_id=row["source_id"],
        name=row["name"],
        source_type=row["source_type"],
        location=row["location"],
        adapter=row["adapter"],
        enabled=bool(row["enabled"]),
        notes=row["notes"],
        last_status=row["last_status"],
        last_message=row["last_message"],
        last_synced_at=row["last_synced_at"],
        last_imported_count=row["last_imported_count"],
    )


def _row_to_product_trend(row: sqlite3.Row) -> ProductTrend:
    return ProductTrend(
        trend_id=row["trend_id"],
        product_id=row["product_id"],
        source=row["source"],
        keyword=row["keyword"],
        category=row["category"],
        trend_score=row["trend_score"],
        sales_score=row["sales_score"],
    )


def _row_to_import_history(row: sqlite3.Row) -> ImportHistoryItem:
    return ImportHistoryItem(
        log_id=row["log_id"],
        entity_type=row["entity_type"],
        operation=row["operation"],
        status=row["status"],
        adapter=row["adapter"],
        filename=row["filename"],
        total_count=row["total_count"],
        ready_count=row["ready_count"],
        error_count=row["error_count"],
        imported_count=row["imported_count"],
        mapped_count=row["mapped_count"],
        generated_id_count=row["generated_id_count"],
        message=row["message"],
        created_at=row["created_at"],
    )


def _row_to_direction(row: sqlite3.Row) -> Direction:
    return Direction(
        direction_id=row["direction_id"],
        title=row["title"],
        category=row["category"],
        description=row["description"],
        target_scene=row["target_scene"],
        budget_min=row["budget_min"],
        budget_max=row["budget_max"],
        difficulty_level=row["difficulty_level"],
        target_interests=_from_json(row["target_interests"]),
    )


def _to_json(value: list[str]) -> str:
    return json.dumps(value, ensure_ascii=False)


def _ensure_column(connection: sqlite3.Connection, table_name: str, column_name: str, definition: str) -> None:
    existing_columns = {
        row["name"]
        for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    }
    if column_name in existing_columns:
        return
    try:
        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")
    except sqlite3.OperationalError as error:
        if "duplicate column name" not in str(error).lower():
            raise


def _from_json(value: str) -> list[str]:
    return json.loads(value)
