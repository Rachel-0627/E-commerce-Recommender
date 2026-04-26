# 电商商品推荐 + AI解释系统

这是一个面向电商平台的个性化商品推荐与 AI 推荐解释 MVP 项目。

当前第一阶段目标：

- 明确产品需求和核心业务流程
- 建立基础数据模型
- 搭建后端 API 骨架
- 提供可演示的模拟推荐结果
- 为后续 ItemCF、用户画像、LLM 解释和反馈闭环预留接口

## 当前模块

```text
backend/
  app/
    main.py                  FastAPI 入口
    models.py                API 数据模型
    sample_data.py           模拟用户、商品和行为数据
    services/
      recommendation.py      推荐逻辑 MVP
      explanation.py         推荐解释逻辑 MVP
frontend/
  index.html                 商品推荐页面
  styles.css                 页面样式
  app.js                     推荐接口联调和反馈提交
docs/
  product-requirements.md    第一阶段产品需求
  architecture.md            MVP 架构设计
  database-schema.md         数据库表设计
```

## 本地运行后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

启动后访问：

- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/health
- 推荐接口：http://127.0.0.1:8000/api/recommendations?user_id=u_001&scene=home&limit=5
- 商品详情：http://127.0.0.1:8000/api/products/p_001
- 趋势数据：http://127.0.0.1:8000/api/product-trends
- 行为数据摘要：http://127.0.0.1:8000/api/events/summary
- 推荐效果统计：http://127.0.0.1:8000/api/analytics/summary
- LLM 状态：http://127.0.0.1:8000/api/llm/status

## 生成模拟行为数据

```bash
python3 scripts/generate_sample_events.py
```

脚本会生成 `data/events.json`，后端会把这批种子行为数据和前端实时提交的行为埋点合并，用于 ItemCF 协同过滤推荐。

## 导入趋势数据

```bash
python3 scripts/import_product_trends.py
```

默认会读取：

```text
data/product_trends.json
```

也支持直接导入 CSV 导出文件，例如：

```bash
python3 scripts/import_product_trends.py data/product_trends_market_export.csv
```

可以先查看可用来源适配器：

```bash
python3 scripts/import_product_trends.py --list-adapters
```

也可以显式指定某个来源适配器：

```bash
python3 scripts/import_product_trends.py data/google_trends_export.csv --adapter google_trends
python3 scripts/import_product_trends.py data/ecommerce_rank_export.csv --adapter ecommerce_rank
```

脚本会做两件事：

- 读取 JSON 或 CSV 的趋势/销量字段
- 如果文件里没有 `product_id`，会根据 `keyword + category` 尝试自动映射到现有商品

当前内置适配器：

- `generic`：通用调研表、手工整理榜单
- `google_trends`：搜索热度导出
- `ecommerce_rank`：电商榜单/热销榜导出

这批趋势数据会写入 SQLite 的 `product_trends` 表，并在推荐打分中提供 `trend_score` 信号。当前仓库内的趋势数据仍然是本地演示用样例，后续可以替换成真实调研或外部采集结果。

## 导入商品来源数据

```bash
python3 scripts/import_products.py
```

默认会读取：

```text
data/product_source_catalog.json
```

也支持直接导入 CSV 商品清单：

```bash
python3 scripts/import_products.py data/product_catalog_market_export.csv --adapter ecommerce_catalog
```

也可以运行已配置的自动同步来源：

```bash
python3 scripts/sync_products.py
```

如果只想跑某一个同步来源：

```bash
python3 scripts/sync_products.py --source-id sync_catalog_local
```

可以先查看可用商品来源适配器：

```bash
python3 scripts/import_products.py --list-adapters
```

当前内置适配器：

- `generic`：通用商品 JSON/CSV 清单
- `ecommerce_catalog`：电商商品导出
- `bestseller_rank`：热销榜商品导出
- `amazon_bestsellers`：Amazon Best Sellers 风格导出
- `shopify_products`：Shopify 商品导出
- `jd_catalog`：京东商品导出

导入后的商品会写入 SQLite 的 `products` 表，并保留 `source`、`external_id`、`popularity_score`、`sales_score` 这些来源字段。

## 自动同步商品资源

自动同步来源接口：

```text
GET   /api/product-sync-sources
POST  /api/product-sync-sources
PATCH /api/product-sync-sources/{source_id}
POST  /api/product-sync-sources/{source_id}/run
POST  /api/product-sync-sources/run-all
```

当前同步来源支持两类位置：

- `file`：本地文件路径，比如 `data/product_catalog_market_export.csv`
- `url`：远程 URL，运行时会尝试拉取 CSV / JSON 内容再导入

项目启动后会自动种入两条本地样例同步来源，方便演示“可重复执行的商品同步”流程。

## SQLite 持久化

运行后端时会自动创建本地数据库：

```text
data/app.sqlite3
```

当前持久化内容：

- `users`：用户画像
- `products`：商品主数据
- `product_trends`：商品趋势与热度信号
- `user_events`：前端实时行为埋点
- `recommendation_logs`：每次推荐返回的商品曝光日志
- `explanation_feedback`：解释反馈

启动时如果 `users` 和 `products` 为空，系统会从 `backend/app/sample_data.py` 自动导入初始数据。`data/events.json` 仍然作为 ItemCF 的种子行为数据，SQLite 负责保存业务主数据和运行时新增数据。`app.sqlite3` 是本地运行产物，已加入 `.gitignore`。

## 商品和用户管理接口

用户管理：

```text
GET   /api/users
GET   /api/users/{user_id}
POST  /api/users
PATCH /api/users/{user_id}
```

商品管理：

```text
GET   /api/products
GET   /api/products/{product_id}
POST  /api/products
PATCH /api/products/{product_id}
GET   /api/product-source-adapters
GET   /api/import-history
POST  /api/products/batch-preview
POST  /api/products/batch-import
```

`POST` 使用传入的 ID 创建或覆盖记录，`PATCH` 支持局部更新，比如只改商品库存、评分或用户近期兴趣。

其中 `GET /api/products` 支持用 `source`、`category` 做过滤。

趋势管理：

```text
GET   /api/product-trends
GET   /api/product-trend-adapters
POST  /api/product-trends/batch-preview
POST  /api/product-trends
POST  /api/product-trends/batch-import
PATCH /api/product-trends/{trend_id}
DELETE /api/product-trends/{trend_id}
```

其中 `GET /api/product-trends` 支持用 `source`、`category`、`product_id` 做过滤。
`GET /api/import-history` 支持用 `entity_type`、`operation` 和 `limit` 查看导入历史。

推荐分现在会在原有 `ItemCF + 用户画像规则` 的基础上，叠加趋势热度信号；当趋势分较高时，推荐标签里会出现“近期热度较高”。

## 方向推荐接口

方向数据与方向推荐已接入 SQLite。

方向管理：

```text
GET   /api/directions
GET   /api/directions/{direction_id}
POST  /api/directions
PATCH /api/directions/{direction_id}
GET   /api/directions/{direction_id}/products
PUT   /api/directions/{direction_id}/products
```

方向推荐：

```text
POST /api/direction-recommendations
```

方向联动商品推荐：

```text
GET /api/recommendations?user_id=u_001&scene=home&direction_id=d_running_beginner&limit=6
```

当前前端已支持点击方向卡片后，将该 `direction_id` 作为筛选条件传给商品推荐接口。
现在前端流程已经升级成两步式：

```text
方向推荐页
  -> 选择方向
  -> 进入该方向商品页
  -> 返回方向页 / 查看全部推荐
```

支持两种模式：

```text
1. 传 user_id
   -> 根据已保存的用户画像推荐方向

2. 不传 user_id，传 preferred_categories / interests / budget / existing_resources
   -> 根据当前倾向和预算推荐方向
```

## 启用 LLM 推荐解释

默认情况下，系统使用模板解释，保证本地没有 API Key 也能运行。

如需启用 OpenAI 兼容解释生成，在启动后端前设置：

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=你的_API_Key
export OPENAI_MODEL=你的模型名
```

然后重启后端：

```bash
cd backend
python3 -m uvicorn app.main:app --reload
```

如果 LLM 调用失败、未配置模型、生成内容不符合安全规则，系统会自动回退到模板解释。

## 本地运行前端

先启动后端，然后在另一个终端运行：

```bash
cd frontend
python3 -m http.server 5500
```

访问：

- 推荐页面：http://127.0.0.1:5500

页面底部现在包含“趋势来源管理”区域，可以查看：

- 已导入的趋势来源
- 每条趋势的热度分和销量分
- 是否已经映射到现有商品
- 按来源和品类筛选趋势记录
- 手动修正未映射商品，并直接保存到 SQLite
- 直接编辑热度分、销量分，或删除整条趋势记录
- 直接从页面新增一条趋势记录，并自动生成 trend_id
- 从页面上传 JSON/CSV 文件，或直接粘贴导出内容做批量导入
- 批量导入前先看预览，确认哪些行可导入、哪些行会报错、哪些行会自动映射

## 下一步

1. 接入真实数据库 PostgreSQL / MySQL
1. 引入 SQLite / PostgreSQL 持久化推荐日志和行为日志
2. 增加更完整的后台运营看板
3. 引入外部公开电商数据集做更大规模训练
4. 增加 RAG 商品知识库，降低解释幻觉
