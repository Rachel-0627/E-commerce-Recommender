# 数据库表设计

第一阶段先定义核心表，当前后端暂时用内存数据模拟。后续可以迁移到 PostgreSQL 或 MySQL。

## users

```sql
CREATE TABLE users (
  user_id VARCHAR(64) PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  age_range VARCHAR(50),
  gender VARCHAR(50),
  location VARCHAR(100),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## products

```sql
CREATE TABLE products (
  product_id VARCHAR(64) PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  category VARCHAR(100) NOT NULL,
  brand VARCHAR(100),
  price DECIMAL(10, 2) NOT NULL,
  description TEXT,
  features JSON,
  image_url TEXT,
  stock INT NOT NULL DEFAULT 0,
  rating DECIMAL(3, 2),
  source VARCHAR(100) NOT NULL DEFAULT 'manual',
  external_id VARCHAR(100),
  popularity_score DECIMAL(8, 2) NOT NULL DEFAULT 0,
  sales_score DECIMAL(8, 2) NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## product_trends

```sql
CREATE TABLE product_trends (
  trend_id VARCHAR(64) PRIMARY KEY,
  product_id VARCHAR(64),
  source VARCHAR(100) NOT NULL,
  keyword VARCHAR(255) NOT NULL,
  category VARCHAR(100) NOT NULL,
  trend_score DECIMAL(8, 2) NOT NULL,
  sales_score DECIMAL(8, 2) NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## product_sync_sources

```sql
CREATE TABLE product_sync_sources (
  source_id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  source_type VARCHAR(20) NOT NULL,
  location TEXT NOT NULL,
  adapter VARCHAR(100),
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  notes TEXT,
  last_status VARCHAR(20),
  last_message TEXT,
  last_synced_at TIMESTAMP,
  last_imported_count INT NOT NULL DEFAULT 0
);
```

## user_events

```sql
CREATE TABLE user_events (
  event_id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  product_id VARCHAR(64) NOT NULL,
  event_type VARCHAR(50) NOT NULL,
  scene VARCHAR(50),
  request_id VARCHAR(64),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## user_profiles

```sql
CREATE TABLE user_profiles (
  user_id VARCHAR(64) PRIMARY KEY,
  interest_tags JSON,
  recent_interests JSON,
  brand_preference JSON,
  price_min DECIMAL(10, 2),
  price_max DECIMAL(10, 2),
  negative_tags JSON,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## recommendation_logs

```sql
CREATE TABLE recommendation_logs (
  log_id VARCHAR(64) PRIMARY KEY,
  request_id VARCHAR(64) NOT NULL,
  user_id VARCHAR(64) NOT NULL,
  product_id VARCHAR(64) NOT NULL,
  rank_position INT NOT NULL,
  score DECIMAL(8, 4) NOT NULL,
  scene VARCHAR(50),
  reason_tags JSON,
  explanation TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## explanation_feedback

```sql
CREATE TABLE explanation_feedback (
  feedback_id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  product_id VARCHAR(64) NOT NULL,
  explanation_id VARCHAR(64),
  feedback_type VARCHAR(50) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## 当前 SQLite 实现

本地运行时会自动创建：

```text
data/app.sqlite3
```

当前 SQLite 已持久化：

```text
users
products
product_trends
product_sync_sources
directions
direction_products
user_events
recommendation_logs
explanation_feedback
import_history
```

其中 `users` 和 `products` 会在首次启动时从 `backend/app/sample_data.py` 种子导入。

用户和商品主数据现在也可以通过 API 写入和更新：

```text
POST /api/users
PATCH /api/users/{user_id}
POST /api/products
PATCH /api/products/{product_id}
GET /api/product-source-adapters
GET /api/product-sync-sources
POST /api/product-sync-sources
PATCH /api/product-sync-sources/{source_id}
POST /api/product-sync-sources/{source_id}/run
POST /api/product-sync-sources/run-all
POST /api/products/batch-preview
POST /api/products/batch-import
POST /api/product-trends
PATCH /api/product-trends/{trend_id}
```

方向主数据现在也可以通过 API 管理：

```text
POST /api/directions
PATCH /api/directions/{direction_id}
PUT /api/directions/{direction_id}/products
```

其中：

```text
directions         保存推荐方向
direction_products 保存方向和商品的映射关系
```

推荐日志表额外保存：

```text
recommendation_source
explanation_provider
```

这两个字段分别用于区分：

```text
itemcf / profile_rule
template / openai / template_fallback
```
